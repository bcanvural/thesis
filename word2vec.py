from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2Vec

def main():
    spark = SparkSession.builder \
        .appName("Spark CV-job ad matching") \
        .config("spark.some.config.option", "some-value") \
        .master("local[*]") \
        .getOrCreate()


    # Input data: Each row is a bag of words from a sentence or document.
    documentDF = spark.createDataFrame([
        ("Hi I heard about Spark".split(" "), ),
        ("I wish Java could use case classes".split(" "), ),
        ("Logistic regression models are neat".split(" "), )
    ], ["text"])

    documentDF2 = spark.createDataFrame([
        ("Hi I heard about Spark".split(" "), ),
        ("I wish Java could use case classes".split(" "), )
    ], ["text"])

    # Learn a mapping from words to Vectors.
    word2Vec = Word2Vec(vectorSize=3, minCount=0, inputCol="text", outputCol="result")
    model = word2Vec.fit(documentDF)
    model2 = word2Vec.fit(documentDF2)

    result = model.transform(documentDF)
    for row in result.collect():
        text, vector = row
        print("Text: [%s] => \nVector: %s\n" % (", ".join(text), str(vector)))




if __name__ == '__main__':
    main()
