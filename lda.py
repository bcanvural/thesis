from pyspark.sql import SparkSession
from pyspark.ml.feature import HashingTF, IDF, Tokenizer, StopWordsRemover, CountVectorizer
from nltk.stem import WordNetLemmatizer
from pyspark.ml.clustering import LDA
from string import punctuation
from nltk.stem.snowball import SnowballStemmer

def stem(rowlist):
    stemmer = SnowballStemmer("english")
    return [stemmer.stem(word) for word in rowlist if word]

def strip_punctuation(arr):
    return [''.join(c for c in s if c not in punctuation) for s in arr]

def lemmatize(rowlist):
    wl = WordNetLemmatizer()
    return [wl.lemmatize(x) for x in rowlist if x]

def main():
    spark = SparkSession.builder \
        .appName("Spark CV-job ad matching") \
        .config("spark.some.config.option", "some-value") \
        .master("local[*]") \
        .getOrCreate()

    VOCAB_SIZE = 100
    MIN_DF = 1.0
    TOPIC_NUM = 50

    df_jobs = spark.read.json("alljobs4rdd/alljobs.jsonl").filter("description is not NULL")

    tokenizer = Tokenizer(inputCol="description", outputCol="words")
    tokenized = tokenizer.transform(df_jobs)

    remover = StopWordsRemover(inputCol="words", outputCol="filtered")
    removed = remover.transform(tokenized)

    processed = removed.rdd.map(lambda row: (row.jobId, lemmatize(strip_punctuation(row.filtered)))).toDF(["jobid", "processed"])

    countVectorizer = CountVectorizer(inputCol="processed", outputCol="rawFeatures", vocabSize=VOCAB_SIZE, minDF=MIN_DF, binary=False)
    cv_model = countVectorizer.fit(processed)
    featurizedData = cv_model.transform(processed)

    lda = LDA(k=TOPIC_NUM, seed=4314, optimizer="em")
    lda.setFeaturesCol("rawFeatures")
    model = lda.fit(featurizedData)
    vocab = cv_model.vocabulary
    model.describeTopics().rdd.map(lambda row: (row.topic, [vocab[x] for x in row.termIndices])).toDF(["Topic", "words"])\
    .coalesce(1).rdd.saveAsTextFile('lda-topics-lemmatized')





if __name__ == '__main__':
    main()
