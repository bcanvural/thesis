from pyspark.sql import SparkSession
from pyspark.ml.feature import  Tokenizer, StopWordsRemover, Word2VecModel, CountVectorizer, IDF
from  pyspark.mllib.linalg import SparseVector, Vectors
import numpy

def add_indices(vector):
    a = []
    idx = 0
    for x in vector.toArray():
        a.append((x, idx))
        idx += 1
    return a

def tuples2words(tuples, vocab):
    words = [vocab[x[1]] for x in tuples]
    return words

def main():
    spark = SparkSession.builder \
        .appName("Spark CV-job ad matching") \
        .config("spark.some.config.option", "some-value") \
        .master("local[*]") \
        .getOrCreate()

    df_jobs = spark.read.json("alljobs4rdd/alljobs.jsonl").filter("description is not NULL")

    tokenizer = Tokenizer(inputCol="description", outputCol="words")
    tokenized = tokenizer.transform(df_jobs)

    remover = StopWordsRemover(inputCol="words", outputCol="filtered")
    removed = remover.transform(tokenized)

    countVectorizer = CountVectorizer(inputCol="filtered", outputCol="rawFeatures", vocabSize=100, minDF=2.0, binary=False)
    cv_model = countVectorizer.fit(removed)
    featurizedData = cv_model.transform(removed)

    idf = IDF(inputCol="rawFeatures", outputCol="features")
    idfModel = idf.fit(featurizedData)
    rescaledData = idfModel.transform(featurizedData)
    vocab = cv_model.vocabulary
    model = Word2VecModel.load("word2vec-model")

    indexed = rescaledData.select('jobId', 'features')\
    .rdd.map(lambda row: (row.jobId, sorted(add_indices(row.features), key=lambda x: x[0], reverse=True)))

    ordered_words = indexed.map(lambda row: (row[0], tuples2words(row[1], vocab)))
    final = ordered_words.map(lambda row: (row[0], " ".join(row[1]))).toDF(['jobid', 'words'])
    final.write.csv('extsyn-importantwords')




    # synonyms = model.findSynonyms(sys.argv[1], 10)
    # synonyms.show(truncate=False)


if __name__ == '__main__':
    main()
