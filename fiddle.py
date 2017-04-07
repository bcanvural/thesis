from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2Vec

def distance(a,b):
    from scipy.spatial import distance
    return float(distance.euclidean(a,b))

def main():
    spark = SparkSession.builder \
        .appName("Spark CV-job ad matching") \
        .config("spark.some.config.option", "some-value") \
        .master("local[*]") \
        .getOrCreate()

    # Input data: Each row is a bag of words from a sentence or document.
    documentDF = spark.createDataFrame([
        ("Hi I heard about Spark".split(" "), ),
        ("about heard I Spark Hi".split(" "), ),
        ("Logistic regression models are neat".split(" "), )
    ], ["text"])

    # Learn a mapping from words to Vectors.
    word2Vec = Word2Vec(vectorSize=3, minCount=0, inputCol="text", outputCol="result")
    model = word2Vec.fit(documentDF)

    results = model.transform(documentDF).collect()
    _, vector0 = results[0]
    _, vector1 = results[1]
    _, vector2 = results[2]

    print(distance(vector0, vector1))
    print(distance(vector0, vector2))
    print(distance(vector1, vector2))


    #
    # for row in result.collect():
    #     text, vector = row
    #     print("Text: [%s] => \nVector: %s\n" % (", ".join(text), str(vector)))

if __name__ == '__main__':
    main()
