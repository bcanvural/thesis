#Synonyms experiment. Pass a string to see its "synonyms"
from pyspark.sql import SparkSession, Row
from pyspark.ml.feature import Word2Vec, Tokenizer, StopWordsRemover, Word2VecModel
import sys;
from string import punctuation

def strip_punctuation(arr):
    return [''.join(c for c in s if c not in punctuation) for s in arr]

def main():
    spark = SparkSession.builder \
        .appName("Spark CV-job ad matching") \
        .config("spark.some.config.option", "some-value") \
        .master("local[*]") \
        .getOrCreate()

    df_categories = spark.read.json("allcategories4rdd/allcategories.jsonl")

    tokenizer = Tokenizer(inputCol="skillText", outputCol="words")
    tokenized = tokenizer.transform(df_categories)

    remover = StopWordsRemover(inputCol="words", outputCol="filtered")
    removed = remover.transform(tokenized)

    stripped = removed.select('filtered').rdd.map(lambda x: strip_punctuation(x[0]))\
    .map(lambda x: Row(filtered=x)).toDF(['filtered'])

    # word2vec = Word2Vec(vectorSize=100, inputCol="filtered", outputCol="result")
    # model = word2vec.fit(stripped)
    #model.save("word2vec-model")
    model = Word2VecModel.load("word2vec-model")
    synonyms = model.findSynonyms(sys.argv[1], 10)
    synonyms.show(truncate=False)
    # for word, cosine_distance in synonyms:
    #     print("{}: {}".format(word, cosine_distance))

if __name__ == '__main__':
    main()
