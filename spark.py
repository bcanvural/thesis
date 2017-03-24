from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.mllib.util import Vectors
from pyspark.sql import Row
from pyspark.ml.classification import NaiveBayes, OneVsRest
from pyspark.ml.feature import StringIndexer
def parseFeatures(jobId, features):
    return Row(label=jobId, features=features)

def main() :
    spark = SparkSession.builder \
        .appName("Spark CV-job ad matching") \
        .config("spark.some.config.option", "some-value") \
        .master("local[4]") \
        .getOrCreate()

    df = spark.read.json("alljobs4rdd/alljobs.jsonl")
    # Displays the content of the DataFrame to stdout
    filtered = df.filter("description is not NULL")
    # filtered.select("jobId","description").write.format("com.databricks.spark.csv").save("out")

    #TF-IDF featurization START
    tokenizer = Tokenizer(inputCol="description", outputCol="words")
    wordsData = tokenizer.transform(filtered)

    #numfeatures should be an exponent of 2
    hashingTF = HashingTF(inputCol="words", outputCol="rawFeatures", numFeatures=32)
    featurizedData = hashingTF.transform(wordsData)
    # alternatively, CountVectorizer can also be used to get term frequency vectors

    idf = IDF(inputCol="rawFeatures", outputCol="features")
    idfModel = idf.fit(featurizedData)
    rescaledData = idfModel.transform(featurizedData)

    #rescaledData.select("jobId", "features").rdd.map(lambda x: (x[0], Vectors.stringify(x[1]))).saveAsTextFile("out")

    #TF-IDF featurization END

    #Naive-Bayes Classifier START
    rowDF = rescaledData.rdd.map(lambda x: parseFeatures(x.jobId, x.features)).toDF()

    # indexer =  StringIndexer(inputCol="label", outputCol="indexed")
    # indexer_model = indexer.fit(rowDF)
    # indexed = indexer_model.transform(rowDF)

    # indexed.select("indexed", "features").rdd.map(lambda x: (x[0], Vectors.stringify(x[1]))).saveAsTextFile("out")

    nb = NaiveBayes(smoothing=1.0, modelType="multinomial")
    ovr = OneVsRest(classifier=nb)
    ovr_model = ovr.fit(rowDF)

    #Naive-Bayes Classifier END





if __name__ == '__main__':
    main()
