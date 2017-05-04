from pymongo import MongoClient
import os
from pathlib import Path
import json
import re

def tfidf_cv_category(db):
    collection = db['tfidf-cv-category']
    path = 'Calculated/tfidf/cv-category'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    # "cvid", "catid", "skillName", "category", "distance"
                    cvid, catid, skillName, category, distance = line.strip().split(',')
                    obj = {"cvid": int(cvid), "catid": int(catid), "skillName": skillName, \
                    "category": category, "distance": float(distance)}
                    collection.insert_one(obj)

def tfidf_job_category(db):
    collection = db['tfidf-job-category']
    path = 'Calculated/tfidf/job-category'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    # "jobid", "catid", "skillName", "category", "distance"
                    jobid, catid, skillName, category, distance = line.strip().split(',')
                    obj = {"jobid": int(jobid), "catid": int(catid), "skillName": skillName, \
                    "category": category, "distance": float(distance)}
                    collection.insert_one(obj)

def tfidf_job_cv(db):
    collection = db['tfidf-job-cv']
    path = 'Calculated/tfidf/job-cv'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    #"jobid", "cvid", "distance"
                    jobid, cvid, distance = line.strip().split(',')
                    obj = {"jobid": int(jobid), "cvid": int(cvid), "distance": float(distance)}
                    collection.insert_one(obj)


def countvectorizer_cv_category(db):
    collection = db['countvectorizer-cv-category']
    path = 'Calculated/countvectorizer/cv-category'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    # "cvid", "catid", "skillName", "category", "distance"
                    cvid, catid, skillName, category, distance = line.strip().split(',')
                    obj = {"cvid": int(cvid), "catid": int(catid), "skillName": skillName, \
                    "category": category, "distance": float(distance)}
                    collection.insert_one(obj)

def countvectorizer_job_category(db):
    collection = db['countvectorizer-job-category']
    path = 'Calculated/countvectorizer/job-category'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    # "jobid", "catid", "skillName", "category", "distance"
                    jobid, catid, skillName, category, distance = line.strip().split(',')
                    obj = {"jobid": int(jobid), "catid": int(catid), "skillName": skillName, \
                    "category": category, "distance": float(distance)}
                    collection.insert_one(obj)

def countvectorizer_job_cv(db):
    collection = db['countvectorizer-job-cv']
    path = 'Calculated/countvectorizer/job-cv'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    #"jobid", "cvid", "distance"
                    jobid, cvid, distance = line.strip().split(',')
                    obj = {"jobid": int(jobid), "cvid": int(cvid), "distance": float(distance)}
                    collection.insert_one(obj)

def word2vec_cv_category(db):
    collection = db['word2vec-cv-category']
    path = 'Calculated/word2vec/cv-category'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    # "cvid", "catid", "skillName", "category", "distance"
                    cvid, catid, skillName, category, distance = line.strip().split(',')
                    obj = {"cvid": int(cvid), "catid": int(catid), "skillName": skillName, \
                    "category": category, "distance": float(distance)}
                    collection.insert_one(obj)

def word2vec_job_category(db):
    collection = db['word2vec-job-category']
    path = 'Calculated/word2vec/job-category'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    # "jobid", "catid", "skillName", "category", "distance"
                    jobid, catid, skillName, category, distance = line.strip().split(',')
                    obj = {"jobid": int(jobid), "catid": int(catid), "skillName": skillName, \
                    "category": category, "distance": float(distance)}
                    collection.insert_one(obj)

def word2vec_job_cv(db):
    collection = db['word2vec-job-cv']
    path = 'Calculated/word2vec/job-cv'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    #"jobid", "cvid", "similarity"
                    jobid, cvid, distance = line.strip().split(',')
                    obj = {"jobid": int(jobid), "cvid": int(cvid), "distance": float(distance)}
                    collection.insert_one(obj)

def write_all_jobs(db):
    collection = db['alljobs']
    q = Path('alljobs4rdd/alljobs.jsonl')
    with q.open() as f:
        for line in f:
            json_obj = json.loads(line.strip())
            try:
                obj = {"jobid": json_obj['jobId'], "description": json_obj["description"]}
                collection.insert_one(obj)
            except:
                continue

def write_all_categories(db):
    collection = db['allcategories']
    q = Path('allcategories4rdd/allcategories.jsonl')
    with q.open() as f:
        for line in f:
            json_obj = json.loads(line.strip())
            try:
                obj = {"catid": json_obj['id'], "skillName": json_obj["skillName"], \
                "skillText": json_obj['skillText'], "category": json_obj["category"]}
                collection.insert_one(obj)
            except:
                continue

def word2vec2_cv_category(db):
    collection = db['word2vec2-cv-category']
    path = 'Calculated/word2vec2/cv-category'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    # "cvid", "catid", "skillName", "category", "distance"
                    cvid, catid, skillName, category, distance = line.strip().split(',')
                    obj = {"cvid": int(cvid), "catid": int(catid), "skillName": skillName, \
                    "category": category, "distance": float(distance)}
                    collection.insert_one(obj)

def word2vec2_job_category(db):
    collection = db['word2vec2-job-category']
    path = 'Calculated/word2vec2/job-category'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    # "jobid", "catid", "skillName", "category", "distance"
                    jobid, catid, skillName, category, distance = line.strip().split(',')
                    obj = {"jobid": int(jobid), "catid": int(catid), "skillName": skillName, \
                    "category": category, "distance": float(distance)}
                    collection.insert_one(obj)

def word2vec2_job_cv(db):
    collection = db['word2vec2-job-cv']
    path = 'Calculated/word2vec2/job-cv'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    #"jobid", "cvid", "similarity"
                    jobid, cvid, distance = line.strip().split(',')
                    obj = {"jobid": int(jobid), "cvid": int(cvid), "distance": float(distance)}
                    collection.insert_one(obj)

def count_pca_cv_category(db):
        collection = db['count-pca-cv-category']
        path = 'Calculated/count-pca/cv-category'
        for filename in os.listdir(path):
            if filename[-3:] == "csv":
                fullpath = path + '/' + filename
                q = Path(fullpath)
                with q.open() as f:
                    for line in f:
                        # "cvid", "catid", "skillName", "category", "distance"
                        cvid, catid, skillName, category, distance = line.strip().split(',')
                        obj = {"cvid": int(cvid), "catid": int(catid), "skillName": skillName, \
                        "category": category, "distance": float(distance)}
                        collection.insert_one(obj)

def count_pca_job_category(db):
        collection = db['count-pca-job-category']
        path = 'Calculated/count-pca/job-category'
        for filename in os.listdir(path):
            if filename[-3:] == "csv":
                fullpath = path + '/' + filename
                q = Path(fullpath)
                with q.open() as f:
                    for line in f:
                        # "jobid", "catid", "skillName", "category", "distance"
                        jobid, catid, skillName, category, distance = line.strip().split(',')
                        obj = {"jobid": int(jobid), "catid": int(catid), "skillName": skillName, \
                        "category": category, "distance": float(distance)}
                        collection.insert_one(obj)

def count_pca_job_cv(db):
    collection = db['count-pca-job-cv']
    path = 'Calculated/count-pca/job-cv'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    #"jobid", "cvid", "similarity"
                    jobid, cvid, distance = line.strip().split(',')
                    obj = {"jobid": int(jobid), "cvid": int(cvid), "distance": float(distance)}
                    collection.insert_one(obj)

def write_all_cvs(db):
    collection = db['allcvs']
    q = Path('allcvs4rdd/allcvs.jsonl')
    with q.open() as f:
        for line in f:
            json_obj = json.loads(line.strip())
            try:
                obj = {"cvid": json_obj['cvid'], "description": json_obj["description"]}
                collection.insert_one(obj)
            except:
                continue

def write_fp_entities(db):
    collection = db['barcharts']
    q = Path('FP-Entities-with-blacklist/part-00000')
    with q.open() as f:
        for line in f:
            entitiy_str = re.search("'(.*?)'", line.strip(), re.IGNORECASE)
            freq_str = re.search("freq=([0-9]*)", line.strip())
            if entitiy_str:
                entities = entitiy_str.group(1).split(" // ") 
                obj = {"type": "fp-entities-with-blacklist", "labels": entities, "freq": int(freq_str.group(1))}
                collection.insert_one(obj)

def write_fp_entities_new_jobs(db):
    collection = db['barcharts']
    q = Path('FP-Entities-newjobs-with-blacklist-all/part-00000')
    with q.open() as f:
        for line in f:
            entitiy_str = re.search("'(.*?)'", line.strip(), re.IGNORECASE)
            freq_str = re.search("freq=([0-9]*)", line.strip())
            if entitiy_str:
                entities = entitiy_str.group(1).split(" // ") 
                obj = {"type": "fp-entities-newjobs-with-blacklist", "labels": entities, "freq": int(freq_str.group(1))}
                collection.insert_one(obj)

def write_fp_reduced(db):
    collection = db['barcharts']
    q = Path('fpreduced.txt')
    with q.open() as f:
        for line in f:
            tokens = line.strip().split()
            entities = tokens[0:len(tokens)-1]
            freq = int(tokens[len(tokens)-1])
            obj = {"type": "fpreduced", "labels": entities, "freq": freq}
            collection.insert_one(obj)

def write_fp_reduced_new_jobs(db):
    collection = db['barcharts']
    q = Path('fpreduced-newjobs.txt')
    with q.open() as f:
        for line in f:
            tokens = line.strip().split()
            entities = tokens[0:len(tokens)-1]
            freq = int(tokens[len(tokens)-1])
            obj = {"type": "fpreduced-newjobs", "labels": entities, "freq": freq}
            collection.insert_one(obj)


def main():
    client = MongoClient('localhost', 27017)
    db = client['thesis-database']

    # tfidf_cv_category(db)
    # tfidf_job_category(db)
    # tfidf_job_cv(db)

    # countvectorizer_cv_category(db)
    # countvectorizer_job_category(db)
    # countvectorizer_job_cv(db)
    # word2vec_cv_category(db)
    # word2vec_job_category(db)
    # word2vec_job_cv(db)

    # word2vec2_cv_category(db)
    # word2vec2_job_category(db)
    # word2vec2_job_cv(db)

    # count_pca_cv_category(db)
    # count_pca_job_category(db)
    # count_pca_job_cv(db)

    # write_all_jobs(db)
    # write_all_categories(db)
    # write_all_cvs(db)

    # write_fp_entities(db)
    # write_fp_entities_new_jobs(db)

    # write_fp_reduced(db)
    write_fp_reduced_new_jobs(db) 


if __name__ == '__main__':
    main()
