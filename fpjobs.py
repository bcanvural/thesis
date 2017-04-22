from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, StopWordsRemover
from pyspark.mllib.fpm import FPGrowthModel, FPGrowth
from pyspark.sql.functions import *
from nltk.stem import WordNetLemmatizer
from string import punctuation

def strip_punctuation(arr):
    return [''.join(c for c in s if c not in punctuation) for s in arr]

def blacklist(rowlist):
    blacklist = ['data', 'experience', 'team', 'work', 'science', 'scientist',\
     'new', 'working', 'looking', 'role', 'strong', 'use', 'based', 'business', \
     'help', 'well', 'across', 'within', 'understanding', 'ability', 'offer', \
     'opportunity', 'required', 'make', 'including', 'need', 'etc', 'high', 'highly',\
     'understand', 'include', 'including', 'best', 'using', 'good', \
     'join', 'job', 'year', 'also', 'large', 'skill', 'world', 'please', 'salary']
    return [x for x in rowlist if x not in blacklist]

def lemmatize(rowlist):
    wl = WordNetLemmatizer()
    return [wl.lemmatize(x) for x in rowlist if x not in ['', ' ']]

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

    words = removed.select("filtered").rdd.map(lambda x: list(set(blacklist(lemmatize(strip_punctuation(x.filtered))))))
    model = FPGrowth.train(words, minSupport=0.1, numPartitions=1)
    finalDF = model.freqItemsets().map(lambda row: (' '.join(row.items) ,row.freq)).toDF(["items", "freq"]).orderBy(desc("freq")).coalesce(1)
    finalDF.write.csv('fpjobs')

if __name__ == '__main__':
    main()
