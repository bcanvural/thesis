from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2Vec, Tokenizer, StopWordsRemover
from pyspark.sql.functions import *

def calculate_distance(vec1, vec2):
    from scipy.spatial import distance
    return float(distance.euclidean(vec1, vec2))

def main():
    spark = SparkSession.builder \
        .appName("Spark CV-job ad matching") \
        .config("spark.some.config.option", "some-value") \
        .master("local[*]") \
        .getOrCreate()

    VECTOR_SIZE = 100

    df_jobs = spark.read.json("alljobs4rdd/alljobs.jsonl").filter("description is not NULL")
    df_jobs.registerTempTable("jobs")
    df_cvs = spark.read.json("allcvs4rdd/allcvs.jsonl")
    df_cvs.registerTempTable("cvs")
    df_categories = spark.read.json("allcategories4rdd/allcategories.jsonl")
    df_categories.registerTempTable("categories")

    joined = spark.sql("SELECT description AS text, jobId AS id, 'job' AS type FROM jobs UNION ALL \
               SELECT description AS text, cvid AS id, 'cv' AS type FROM cvs UNION ALL \
               SELECT skillText AS text, id AS id, 'categories' AS type FROM categories")

    tokenizer = Tokenizer(inputCol="text", outputCol="words")
    tokenized = tokenizer.transform(joined)

    remover = StopWordsRemover(inputCol="words", outputCol="filtered")
    removed = remover.transform(tokenized)

    word2Vec = Word2Vec(vectorSize=VECTOR_SIZE, minCount=0, inputCol="filtered", outputCol="result")
    model = word2Vec.fit(removed)
    result = model.transform(removed)

    result.registerTempTable("resultTable")
    jobs = spark.sql("SELECT result AS jobsVec, id AS jobId FROM resultTable WHERE type = 'job'")
    cvs = spark.sql("SELECT result AS cvsVec, id AS cvid FROM resultTable WHERE type = 'cv'")
    categories = spark.sql("SELECT result AS categoriesVec, cat.id, cat.skillName FROM resultTable AS rt\
    LEFT JOIN categories AS cat ON rt.id = cat.id WHERE type = 'categories'")

    #Calculate job-cv similarity START
    crossJoined_job_cv = jobs.crossJoin(cvs)
    calculated_job_cv = crossJoined_job_cv.rdd.map(lambda x: (x.jobId, x.cvid, calculate_distance(x.jobsVec, x.cvsVec)))\
    .toDF(["jobid", "cvid", "distance"]).orderBy(asc("jobid")).coalesce(2)
    calculated_job_cv.write.csv('Calculated/word2vec/job-cv')
    #Calculate job-cv similarity END

    #Calculate cv-category similarity START
    crossJoined_cv_cat = cvs.crossJoin(categories)
    calculated_cv_cat = crossJoined_cv_cat.rdd.map(lambda x: (x.cvid, x.id, x.skillName, calculate_distance(x.cvsVec, x.categoriesVec)))\
    .toDF(["cvid", "category_id", "skillName", "distance"]).orderBy(asc("cvid"), asc("distance")).coalesce(2)
    calculated_cv_cat.write.csv('Calculated/word2vec/cv-category')
    #Calculate cv-category similarity END

    #Job-category START
    crossJoined_job_cat = jobs.select("jobId", "jobsVec").crossJoin(categories.select("id", "skillName", "categoriesVec"))
    calculatedDF_job_cat = crossJoined_job_cat.rdd\
    .map(lambda x: (x.jobId, x.id, x.skillName, calculate_distance(x.jobsVec, x.categoriesVec)))\
    .toDF(["jobid", "catid", "skillName", "distance"])
    ordered_job_cat = calculatedDF_job_cat.orderBy( asc("distance")).coalesce(2)
    ordered_job_cat.write.csv('Calculated/word2vec/job-category')
    #Job-category END

if __name__ == '__main__':
    main()
