from pyspark.sql import SparkSession, Row
import ast
from pyspark.ml.feature import CountVectorizer, IDF

def add_indices(vector):
    a = []
    idx = 0
    for x in vector:
        a.append((x, idx))
        idx += 1
    return a

def tuples2words(tuples, vocab):
    words = [vocab[x[1]] for x in tuples]
    return words

def parse_list(row):
    return ast.literal_eval(row)

def main():
    spark = SparkSession.builder \
        .appName("Spark CV-job ad matching") \
        .master("local[*]") \
        .getOrCreate()
    
    entities_str = spark.sparkContext.textFile("Entities/part-00[0-5]*")
    entities = entities_str.map(lambda row: Row(entities=parse_list(row))).toDF(["entities"])
   
    countVectorizer = CountVectorizer(inputCol="entities", outputCol="rawFeatures", vocabSize=100, minDF=2.0, binary=False)
    cv_model = countVectorizer.fit(entities)
    featurizedData = cv_model.transform(entities)

    idf = IDF(inputCol="rawFeatures", outputCol="features")
    idfModel = idf.fit(featurizedData)
    rescaledData = idfModel.transform(featurizedData)
    vocab = cv_model.vocabulary

    indexed = rescaledData.select('features').rdd.map(lambda row: sorted(add_indices(row.features), key=lambda x: x[0], reverse=True))
    ordered_words = indexed.map(lambda row: tuples2words(row, vocab)).toDF(["words"])
    ordered_words.rdd.saveAsTextFile('entity-tfidf-words')
    



if __name__ == '__main__':
    main()