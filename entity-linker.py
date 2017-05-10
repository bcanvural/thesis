#Extract entities from jobs
from pyspark.sql import SparkSession
import json
from pyspark.mllib.fpm import FPGrowthModel, FPGrowth
from pyspark.sql.functions import *

def blacklist(rowlist):
    blacklist = ['Free will', 'You Will (song)', 'Skill', 'Experience', 'The Mail on Sunday', 'Understanding', 'Western (genre)',\
    'Team', 'Business', 'Employment', 'Solution', 'Customer', 'Tool', 'Insight', 'Organization', 'Complexity',\
    'We Are (Ana Johnsson song)', 'Will and testament', 'The A-Team', 'Natural environment', 'Equal opportunity',\
    'World Health Organization', 'Childbirth', 'Please (U2 song)', 'Expert']
    return [x for x in rowlist if x not in blacklist]


def get_entities(text, jobid):
    print(jobid)
    import urllib.request
    import urllib.parse
    q_dict = {'lang': 'en', 'gcube-token': '25f9426f-8476-4aae-a512-f364bb8fd9e2-843339462', 'text': text}
    url = "https://tagme.d4science.org/tagme/tag?{0}".format(urllib.parse.urlencode(q_dict))
    try:
        json_obj = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
    except:
        return ['HTML ERROR', jobid]
    entity_set = set()
    for annotation in json_obj['annotations']:
        try:
            entity_set.add(annotation['title'])
        except KeyError:
            continue
    return list(entity_set)


def main():
    spark = SparkSession.builder \
        .appName("Spark CV-job ad matching") \
        .config("spark.some.config.option", "some-value") \
        .master("local[*]") \
        .getOrCreate()

    # df_jobs = spark.read.json("alljobs4rdd/alljobs.jsonl").filter("description is not NULL").cache() #jobs from 2016 summer
    df_jobs = spark.read.json("newjobs4rdd/newjobs.jsonl").filter("description is not NULL").cache() #jobs from 2016 December
    entities = df_jobs.rdd.map(lambda row: blacklist(get_entities(row.description, row.jobid))).cache()
    entities.saveAsTextFile('Entities-newjobs')
    model = FPGrowth.train(entities, minSupport=0.1, numPartitions=1)
    finalDF = model.freqItemsets().map(lambda row: (' // '.join(row.items) ,row.freq)).toDF(["items", "freq"]).orderBy(desc("freq")).coalesce(1)
    finalDF.rdd.saveAsTextFile('FP-Entities-newjobs-with-blacklist-all')

if __name__ == '__main__':
    main()
