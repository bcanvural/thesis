#
# TF-IDF among job ads, CVs, categories (all together)
#
from pyspark.sql import SparkSession
from pyspark.ml.feature import CountVectorizer, IDF, Tokenizer, StopWordsRemover
from pyspark.sql.functions import *

def calculate_cosine_similarity(vec_job, vec_cv):
    from scipy import spatial
    cv = vec_cv.toArray()
    jobs = vec_job.toArray()
    result = spatial.distance.cosine(cv, jobs)
    return float(result)

def main():
    spark = SparkSession.builder \
        .appName("Spark CV-job ad matching") \
        .config("spark.some.config.option", "some-value") \
        .master("local[*]") \
        .getOrCreate()

    VOCAB_SIZE = 250
    MIN_DF = 1.0

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

    countVectorizer = CountVectorizer(inputCol="filtered", outputCol="rawFeatures", vocabSize=VOCAB_SIZE, minDF=MIN_DF, binary=False)
    cv_model = countVectorizer.fit(removed)
    featurizedData = cv_model.transform(removed)

    idf = IDF(inputCol="rawFeatures", outputCol="features")
    idfModel = idf.fit(featurizedData)
    rescaledData = idfModel.transform(featurizedData)

    rescaledData.registerTempTable("resultTable")
    jobs = spark.sql("SELECT features, id AS jobId FROM resultTable WHERE type = 'job'")
    cvs = spark.sql("SELECT features AS featuresCV, id AS cvid FROM resultTable WHERE type = 'cv'")
    categories = spark.sql("SELECT features AS featuresCAT, cat.id, cat.skillName AS skillName FROM resultTable AS rt\
    LEFT JOIN categories AS cat ON rt.id = cat.id WHERE type = 'categories'")

    #Calculate job-cv similarity START
    crossJoined = jobs.select("jobId", "features").crossJoin(cvs.select("cvid", "featuresCV"))
    calculatedDF = crossJoined.rdd.map(lambda x: (x.jobId, x.cvid, calculate_cosine_similarity(x.features, x.featuresCV)))\
    .toDF(["jobid", "cvid", "similarity"])
    ordered = calculatedDF.orderBy(asc("jobid")).coalesce(2)
    ordered.write.csv('Calculated/countvectorizer/job-cv')
    #Calculate job-cv similarity END

    #Calculate cv-category similarity START
    crossJoined_cat_cv = cvs.select("cvid", "featuresCV").crossJoin(categories.select("id", "skillName", "featuresCAT"))
    calculatedDF_cat_cv = crossJoined_cat_cv.rdd\
    .map(lambda x: (x.cvid, x.id, x.skillName, calculate_cosine_similarity(x.featuresCV, x.featuresCAT)))\
    .toDF(["cvid", "catid", "skillName", "similarity"])
    ordered_cat_cv = calculatedDF_cat_cv.orderBy(asc("cvid"), desc("similarity")).coalesce(2)
    ordered_cat_cv.write.csv('Calculated/countvectorizer/cv-category')
    #Calculate cv-category similarity END

    #Job-category START
    crossJoined_job_cat = jobs.select("jobId", "features").crossJoin(categories.select("id", "skillName", "featuresCAT"))
    calculatedDF_job_cat = crossJoined_job_cat.rdd\
    .map(lambda x: (x.jobId, x.id, x.skillName, calculate_cosine_similarity(x.features, x.featuresCAT)))\
    .toDF(["jobid", "catid", "skillName", "similarity"])
    ordered_job_cat = calculatedDF_job_cat.orderBy( desc("similarity")).coalesce(2)
    ordered_job_cat.write.csv('Calculated/countvectorizer/job-category')
    #Job-category END

if __name__ == '__main__':
    main()
