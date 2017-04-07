from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2Vec, Tokenizer, StopWordsRemover
from pyspark.sql.functions import *

def calculate_distance(vec1, vec2):
    return float(vec1.squared_distance(vec2))

def main():
    spark = SparkSession.builder \
        .appName("Spark CV-job ad matching") \
        .config("spark.some.config.option", "some-value") \
        .master("local[*]") \
        .getOrCreate()

    df_jobs = spark.read.json("alljobs4rdd/alljobs.jsonl").filter("description is not NULL")
    df_jobs.registerTempTable("jobs")
    df_cvs = spark.read.json("allcvs4rdd/allcvs.jsonl")
    df_cvs.registerTempTable("cvs")
    df_categories = spark.read.json("allcategories4rdd/allcategories.jsonl")
    df_categories.registerTempTable("categories")

    joined = spark.sql("SELECT description as text, jobId as id, 'job' as type, 'temp' as skillName FROM jobs UNION ALL \
               SELECT description as text, cvid as id, 'cv' as type, 'temp' as skillName FROM cvs UNION ALL \
               SELECT skillText as text, id as id, 'categories' as type, skillName FROM categories")

    tokenizer = Tokenizer(inputCol="text", outputCol="words")
    tokenized = tokenizer.transform(joined)

    remover = StopWordsRemover(inputCol="words", outputCol="filtered")
    removed = remover.transform(tokenized)

    word2Vec = Word2Vec(vectorSize=100, minCount=0, inputCol="filtered", outputCol="result")
    model = word2Vec.fit(removed)
    result = model.transform(removed)

    result.registerTempTable("resultTable")
    jobs = spark.sql("SELECT text, result as jobsVec, id as jobId from resultTable WHERE type = 'job'")
    cvs = spark.sql("SELECT text, result as cvsVec, id as cvid from resultTable WHERE type = 'cv'")
    categories = spark.sql("SELECT text, result as categoriesVec, id, skillName from resultTable WHERE type = 'categories'")

    #Calculate job-cv similarity START
    crossJoined_job_cv = jobs.crossJoin(cvs)
    calculated_job_cv = crossJoined_job_cv.rdd.map(lambda x: (x.jobId, x.cvid, calculate_distance(x.jobsVec, x.cvsVec)))\
    .toDF(["jobid", "cvid", "distance"]).orderBy(asc("distance")).collect()
    spark.sparkContext.parallelize(calculated_job_cv).saveAsTextFile('word2vec-calculated')
    #Calculate job-cv similarity END

    #Calculate cv-category similarity START
    crossJoined_cv_cat = cvs.crossJoin(categories)
    calculated_cv_cat = crossJoined_cv_cat.rdd.map(lambda x: (x.cvid, x.id, x.skillName, calculate_distance(x.cvsVec, x.categoriesVec)))\
    .toDF(["cvid", "category_id", "skillName", "distance"]).orderBy(asc("cvid"), asc("distance")).collect()
    spark.sparkContext.parallelize(calculated_cv_cat).saveAsTextFile('category-word2vec-calculated')
    #Calculate cv-category similarity END

if __name__ == '__main__':
    main()
