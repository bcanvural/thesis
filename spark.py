from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.mllib.util import Vectors
from pyspark.sql import Row
from pyspark.ml.classification import NaiveBayes, OneVsRest, OneVsRestModel
from pyspark.sql.functions import udf
from pyspark.sql.types import DoubleType
from pyspark.sql.functions import *

def parseFeatures(jobId, features):
    return Row(label=jobId, features=features)

def parseFeaturesCV(features):
    return Row(featuresCV=features)

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

    df_jobs = spark.read.json("alljobs4rdd/alljobs.jsonl")
    filtered = df_jobs.filter("description is not NULL")

    # filtered.select("jobId","description").write.format("com.databricks.spark.csv").save("out")

    #TF-IDF featurization START
    tokenizer = Tokenizer(inputCol="description", outputCol="words")
    wordsData = tokenizer.transform(filtered)

    #numfeatures should be an exponent of 2
    hashingTF = HashingTF(inputCol="words", outputCol="rawFeatures", numFeatures=128)
    featurizedData = hashingTF.transform(wordsData)

    idf = IDF(inputCol="rawFeatures", outputCol="features")
    idfModel = idf.fit(featurizedData)
    rescaledData = idfModel.transform(featurizedData).cache()

    # rescaledData.select("jobId", "features").rdd.map(lambda x: (x[0], Vectors.stringify(x[1]))).saveAsTextFile("out")

    #TF-IDF featurization END

    #Naive-Bayes Classifier START
    # rowDF = rescaledData.rdd.map(lambda x: parseFeatures(x.jobId, x.features)).toDF().cache()

    #nb = NaiveBayes(smoothing=1.0, modelType="multinomial")
    #ovr = OneVsRest(classifier=nb)
    # ovr_model = ovr.fit(rowDF)
    #ovr_model.save("OneVsRestNaiveBayes.model")
    #ovr_model_loaded = OneVsRestModel.load("OneVsRestNaiveBayes")

    #Naive-Bayes Classifier END

    #Process CVs START
    df_cvs = spark.read.json("allcvs4rdd/allcvs.jsonl")
    # df_cvs.show()
    tokenizer_cvs = Tokenizer(inputCol="description", outputCol="words")
    wordsData_cvs = tokenizer_cvs.transform(df_cvs)
    #numfeatures should be an exponent of 2
    hashingTF_cvs = HashingTF(inputCol="words", outputCol="rawFeatures", numFeatures=128)
    featurizedData_cvs = hashingTF_cvs.transform(wordsData_cvs)
    idf_cvs = IDF(inputCol="rawFeatures", outputCol="featuresCV")
    idfModel_cvs = idf_cvs.fit(featurizedData_cvs)
    rescaledData_cvs = idfModel_cvs.transform(featurizedData_cvs).cache()
    # rescaledData_cvs.select("cvid", "featuresCV").rdd.map(lambda x: (x[0], Vectors.stringify(x[1]))).saveAsTextFile("outcv")

    #OneVsRest Naive Bayes experiment
    # ovr_model_loaded.transform(rescaledData_cvs.rdd.map(lambda x: parseFeaturesCV(x.features)).toDF())\
    # .rdd.map(lambda x: (x[0], Vectors.stringify(x[1])))\
    # .saveAsTextFile("outresults")

    #Process CVs END

    #Cosine Similarity START

    crossJoined = rescaledData.select("jobId", "features").crossJoin(rescaledData_cvs.select("cvid", "featuresCV")).cache()

    calculatedDF = crossJoined.rdd.map(lambda x: (x.jobId, x.cvid, calculate_cosine_similarity(x.features, x.featuresCV)))\
    .toDF(["jobid", "cvid", "similarity"])
    ordered_list = calculatedDF.orderBy(desc("similarity")).collect()
    spark.sparkContext.parallelize(ordered_list).saveAsTextFile('cosine-calculated')

    #Cosine Similarity END

    #Process Categories START
    df_categories = spark.read.json("allcategories4rdd/allcategories.jsonl")
    tokenizer_cat = Tokenizer(inputCol="skillText", outputCol="words")
    wordsData_cat = tokenizer_cat.transform(df_categories)
    #numfeatures should be an exponent of 2
    hashingTF_cat = HashingTF(inputCol="words", outputCol="rawFeatures", numFeatures=128)
    featurizedData_cat = hashingTF_cat.transform(wordsData_cat)
    idf_cat = IDF(inputCol="rawFeatures", outputCol="featuresCAT")
    idfModel_cat = idf_cat.fit(featurizedData_cat)
    rescaledData_cat = idfModel_cat.transform(featurizedData_cat).cache()

    crossJoined_cat_cv = rescaledData_cvs.crossJoin(rescaledData_cat)
    calculatedDF_cat_cv = crossJoined_cat_cv.rdd\
    .map(lambda x: (x.cvid, x.id, x.skillName, calculate_cosine_similarity(x.featuresCV, x.featuresCAT)))\
    .toDF(["cvid", "catid", "skillName", "similarity"])
    ordered_list_cat_cv = calculatedDF_cat_cv.orderBy(asc("cvid"), desc("similarity")).collect()
    spark.sparkContext.parallelize(ordered_list_cat_cv).saveAsTextFile('category-cosine-calculated')
    #Process Categories END

if __name__ == '__main__':
    main()
