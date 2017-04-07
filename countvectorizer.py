from pyspark.sql import SparkSession
from pyspark.ml.feature import CountVectorizer

def main():
    spark = SparkSession.builder \
        .appName("Spark CV-job ad matching") \
        .config("spark.some.config.option", "some-value") \
        .master("local[*]") \
        .getOrCreate()

    # Input data: Each row is a bag of words with a ID.
    df = spark.createDataFrame([
        (0, "a b c".split(" ")),
        (1, "a b b c a d".split(" "))
    ], ["id", "words"])

    # fit a CountVectorizerModel from the corpus.
    cv = CountVectorizer(inputCol="words", outputCol="features", vocabSize=3, minDF=2.0)

    model = cv.fit(df)

    result = model.transform(df)
    result.show(truncate=False)

if __name__ == '__main__':
    main()
