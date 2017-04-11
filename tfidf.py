#
# TF-IDF among job ads, TF-IDF among CVs, TF-IDF among categories (all seperate)
#
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.ml.feature import HashingTF, IDF, Tokenizer, StopWordsRemover
from pyspark.sql import Row
from pyspark.ml.classification import NaiveBayes, OneVsRest, OneVsRestModel
from pyspark.sql.functions import *

def calculate_cosine_similarity(vec_job, vec_cv):
    from scipy import spatial
    cv = vec_cv.toArray()
    jobs = vec_job.toArray()
    result = spatial.distance.cosine(cv, jobs)
    return float(result)

def main() :
    spark = SparkSession.builder \
        .appName("Spark CV-job ad matching") \
        .config("spark.some.config.option", "some-value") \
        .master("local[*]") \
        .getOrCreate()

    NUM_FEATURES = 2**8

    df_jobs = spark.read.json("alljobs4rdd/alljobs.jsonl")
    filtered = df_jobs.filter("description is not NULL")

    #TF-IDF featurization START
    tokenizer = Tokenizer(inputCol="description", outputCol="words")
    wordsData = tokenizer.transform(filtered)

    remover = StopWordsRemover(inputCol="words", outputCol="filtered")
    removed = remover.transform(wordsData)

    hashingTF = HashingTF(inputCol="filtered", outputCol="rawFeatures", numFeatures=NUM_FEATURES)
    featurizedData = hashingTF.transform(removed)

    idf = IDF(inputCol="rawFeatures", outputCol="features")
    idfModel = idf.fit(featurizedData)
    rescaledData = idfModel.transform(featurizedData).cache()

    #TF-IDF featurization END

    #Process CVs START
    df_cvs = spark.read.json("allcvs4rdd/allcvs.jsonl")

    tokenizer_cvs = Tokenizer(inputCol="description", outputCol="words")
    wordsData_cvs = tokenizer_cvs.transform(df_cvs)

    remover_cvs = StopWordsRemover(inputCol="words", outputCol="filtered")
    removed_cvs = remover_cvs.transform(wordsData_cvs)

    hashingTF_cvs = HashingTF(inputCol="filtered", outputCol="rawFeatures", numFeatures=NUM_FEATURES)
    featurizedData_cvs = hashingTF_cvs.transform(removed_cvs)

    idf_cvs = IDF(inputCol="rawFeatures", outputCol="featuresCV")
    idfModel_cvs = idf_cvs.fit(featurizedData_cvs)
    rescaledData_cvs = idfModel_cvs.transform(featurizedData_cvs).cache()

    #Process CVs END

    #Cosine Similarity START

    crossJoined = rescaledData.select("jobId", "features").crossJoin(rescaledData_cvs.select("cvid", "featuresCV")).cache()

    calculatedDF = crossJoined.rdd.map(lambda x: (x.jobId, x.cvid, calculate_cosine_similarity(x.features, x.featuresCV)))\
    .toDF(["jobid", "cvid", "similarity"])
    ordered = calculatedDF.orderBy(asc("jobid")).coalesce(2)
    ordered.write.csv('Calculated/tfidf/job-cv')

    #Cosine Similarity END

    #Process Categories START
    df_categories = spark.read.json("allcategories4rdd/allcategories.jsonl")
    tokenizer_cat = Tokenizer(inputCol="skillText", outputCol="words")
    wordsData_cat = tokenizer_cat.transform(df_categories)

    remover_cat = StopWordsRemover(inputCol="words", outputCol="filtered")
    removed_cat = remover_cat.transform(wordsData_cat)

    hashingTF_cat = HashingTF(inputCol="filtered", outputCol="rawFeatures", numFeatures=NUM_FEATURES)
    featurizedData_cat = hashingTF_cat.transform(removed_cat)

    idf_cat = IDF(inputCol="rawFeatures", outputCol="featuresCAT")
    idfModel_cat = idf_cat.fit(featurizedData_cat)
    rescaledData_cat = idfModel_cat.transform(featurizedData_cat).cache()

    crossJoined_cat_cv = rescaledData_cvs.crossJoin(rescaledData_cat)
    calculatedDF_cat_cv = crossJoined_cat_cv.rdd\
    .map(lambda x: (x.cvid, x.id, x.skillName, calculate_cosine_similarity(x.featuresCV, x.featuresCAT)))\
    .toDF(["cvid", "catid", "skillName", "similarity"])
    ordered_cat_cv = calculatedDF_cat_cv.orderBy(asc("cvid"), desc("similarity")).coalesce(2)
    ordered_cat_cv.write.csv('Calculated/tfidf/cv-category')
    #Process Categories END

    #Job-category START
    crossJoined_job_cat = rescaledData.select("jobId", "features").crossJoin(rescaledData_cat.select("id", "featuresCAT", "skillName"))
    calculatedDF_job_cat = crossJoined_job_cat.rdd \
    .map(lambda x: (x.jobId, x.id, x.skillName, calculate_cosine_similarity(x.features, x.featuresCAT))) \
    .toDF(["jobid", "catid", "skillName", "similarity"])
    ordered_job_cat = calculatedDF_job_cat.orderBy(desc("similarity")).coalesce(2)
    ordered_job_cat.write.csv('Calculated/tfidf/job-category')

    #Job-category END

if __name__ == '__main__':
    main()
