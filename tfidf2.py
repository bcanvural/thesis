#
# TF-IDF among job ads, CVs, categories (all together)
#
from pyspark.sql import SparkSession
from pyspark.ml.feature import HashingTF, IDF, Tokenizer, StopWordsRemover
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

    NUM_FEATURES = 2048

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

    hashingTF = HashingTF(inputCol="filtered", outputCol="rawFeatures", numFeatures=NUM_FEATURES)
    featurizedData = hashingTF.transform(removed)

    idf = IDF(inputCol="rawFeatures", outputCol="features")
    idfModel = idf.fit(featurizedData)
    rescaledData = idfModel.transform(featurizedData)

    rescaledData.registerTempTable("resultTable")
    jobs = spark.sql("SELECT text, features, id as jobId from resultTable WHERE type = 'job'")
    cvs = spark.sql("SELECT text, features as featuresCV, id as cvid from resultTable WHERE type = 'cv'")
    categories = spark.sql("SELECT text, features as featuresCAT, id, skillName from resultTable WHERE type = 'categories'")

    #Calculate job-cv similarity START
    crossJoined = jobs.select("jobId", "features").crossJoin(cvs.select("cvid", "featuresCV"))
    calculatedDF = crossJoined.rdd.map(lambda x: (x.jobId, x.cvid, calculate_cosine_similarity(x.features, x.featuresCV)))\
    .toDF(["jobid", "cvid", "similarity"])
    ordered_list = calculatedDF.orderBy(desc("similarity")).collect()
    spark.sparkContext.parallelize(ordered_list).saveAsTextFile('cosine-calculated-tfidf2')
    #Calculate job-cv similarity END

    #Calculate cv-category similarity START
    crossJoined_cat_cv = cvs.select("cvid", "featuresCV").crossJoin(categories.select("id", "skillName", "featuresCAT"))
    calculatedDF_cat_cv = crossJoined_cat_cv.rdd\
    .map(lambda x: (x.cvid, x.id, x.skillName, calculate_cosine_similarity(x.featuresCV, x.featuresCAT)))\
    .toDF(["cvid", "catid", "skillName", "similarity"])
    ordered_list_cat_cv = calculatedDF_cat_cv.orderBy(asc("cvid"), desc("similarity")).collect()
    spark.sparkContext.parallelize(ordered_list_cat_cv).saveAsTextFile('category-cosine-calculated-tfidf2')
    #Calculate cv-category similarity END

if __name__ == '__main__':
    main()
