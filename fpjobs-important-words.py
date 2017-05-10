#Running FP growth algorithm on "important" words per job. Important = higher value in TFIDF measure
from pyspark.sql import SparkSession, Row
from pyspark.ml.feature import  Tokenizer, StopWordsRemover, CountVectorizer, IDF
from  pyspark.mllib.linalg import SparseVector, Vectors
import numpy
from string import punctuation
from nltk.stem import WordNetLemmatizer
from pyspark.mllib.fpm import FPGrowthModel, FPGrowth
from pyspark.sql.functions import *

def strip_punctuation(arr):
    return [''.join(c for c in s if c not in punctuation) for s in arr]

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

def lemmatize(rowlist):
    wl = WordNetLemmatizer()
    return [wl.lemmatize(x) for x in rowlist if x not in ['', ' ']]

def main():
    spark = SparkSession.builder \
        .appName("Spark CV-job ad matching") \
        .config("spark.some.config.option", "some-value") \
        .master("local[*]") \
        .getOrCreate()

    df_jobs = spark.read.json("alljobs4rdd/alljobs.jsonl").filter("description is not NULL").cache()

    tokenizer = Tokenizer(inputCol="description", outputCol="words")
    tokenized = tokenizer.transform(df_jobs)

    remover = StopWordsRemover(inputCol="words", outputCol="filtered")
    removed = remover.transform(tokenized)

    stripped = removed.select('jobid', 'filtered').rdd.map(lambda x: (x[0], strip_punctuation(x[1])))\
    .map(lambda x: Row(jobid=x[1], filtered=x[0])).toDF(['jobid', 'filtered']) #dont know why indices flipped

    countVectorizer = CountVectorizer(inputCol="filtered", outputCol="rawFeatures", vocabSize=100, minDF=2.0, binary=False)
    cv_model = countVectorizer.fit(stripped)
    featurizedData = cv_model.transform(stripped)

    idf = IDF(inputCol="rawFeatures", outputCol="features")
    idfModel = idf.fit(featurizedData)
    rescaledData = idfModel.transform(featurizedData)
    vocab = cv_model.vocabulary

    indexed = rescaledData.select('jobid', 'features')\
    .rdd.map(lambda row: (row.jobid, sorted(add_indices(row.features), key=lambda x: x[0], reverse=True)))

    ordered_words = indexed.map(lambda row: (row[0], tuples2words(row[1], vocab))).toDF(["jobid", "words"])
    # final = ordered_words.map(lambda row: (row[0], " ".join(row[1]))).toDF(['jobid', 'words'])
    # final.write.csv('extsyn-importantwords')

    N_START = 0
    N_END = 15
    # ordered_words.select("words").rdd.saveAsTextFile('hehe')
    words = ordered_words.select("words").rdd.map(lambda x: list(set((lemmatize(strip_punctuation(x.words)))))[N_START:N_END])
    model = FPGrowth.train(words, minSupport=0.1, numPartitions=1)
    finalDF = model.freqItemsets().map(lambda row: (' '.join(row.items) ,row.freq)).toDF(["items", "freq"]).orderBy(desc("freq")).coalesce(1)
    finalDF.write.csv('fpjobs-important-words')


if __name__ == '__main__':
    main()
