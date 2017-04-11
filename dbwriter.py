from pymongo import MongoClient
import os
from pathlib import Path
import json

def tfidf_cv_category(db):
    collection = db['tfidf-cv-category']
    path = 'Calculated/tfidf/cv-category'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    # "cvid", "catid", "skillName", "similarity"
                    cvid, catid, skillName, similarity = line.strip().split(',')
                    obj = {"cvid": int(cvid), "catid": int(catid), "skillName": skillName, \
                    "similarity": similarity}
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
                    #"jobid", "catid", "skillName", "similarity"
                    jobid, catid, skillName, similarity = line.strip().split(',')
                    obj = {"jobid": int(jobid), "catid": int(catid), "skillName": skillName, \
                    "similarity": similarity}
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
                    #"jobid", "cvid", "similarity"
                    jobid, cvid, similarity = line.strip().split(',')
                    obj = {"jobid": int(jobid), "cvid": int(cvid), "similarity": similarity}
                    collection.insert_one(obj)

def tfidf2_cv_category(db):
    collection = db['tfidf2-cv-category']
    path = 'Calculated/tfidf2/cv-category'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    # "cvid", "catid", "skillName", "similarity"
                    cvid, catid, skillName, similarity = line.strip().split(',')
                    obj = {"cvid": int(cvid), "catid": int(catid), "skillName": skillName, \
                    "similarity": similarity}
                    collection.insert_one(obj)

def tfidf2_job_category(db):
    collection = db['tfidf2-job-category']
    path = 'Calculated/tfidf2/job-category'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    # "jobid", "catid", "skillName", "similarity"
                    jobid, catid, skillName, similarity = line.strip().split(',')
                    obj = {"jobid": int(jobid), "catid": int(catid), "skillName": skillName, \
                    "similarity": similarity}
                    collection.insert_one(obj)

def tfidf2_job_cv(db):
    collection = db['tfidf2-job-cv']
    path = 'Calculated/tfidf2/job-cv'
    for filename in os.listdir(path):
        if filename[-3:] == "csv":
            fullpath = path + '/' + filename
            q = Path(fullpath)
            with q.open() as f:
                for line in f:
                    #"jobid", "cvid", "similarity"
                    jobid, cvid, similarity = line.strip().split(',')
                    obj = {"jobid": int(jobid), "cvid": int(cvid), "similarity": similarity}
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
                    # "cvid", "catid", "skillName", "similarity"
                    cvid, catid, skillName, similarity = line.strip().split(',')
                    obj = {"cvid": int(cvid), "catid": int(catid), "skillName": skillName, \
                    "similarity": similarity}
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
                    # "jobid", "catid", "skillName", "similarity"
                    jobid, catid, skillName, similarity = line.strip().split(',')
                    obj = {"jobid": int(jobid), "catid": int(catid), "skillName": skillName, \
                    "similarity": similarity}
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
                    #"jobid", "cvid", "similarity"
                    jobid, cvid, similarity = line.strip().split(',')
                    obj = {"jobid": int(jobid), "cvid": int(cvid), "similarity": similarity}
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
                    # "cvid", "catid", "skillName", "similarity"
                    cvid, catid, skillName, distance = line.strip().split(',')
                    obj = {"cvid": int(cvid), "catid": int(catid), "skillName": skillName, \
                    "distance": distance}
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
                    # "jobid", "catid", "skillName", "similarity"
                    jobid, catid, skillName, distance = line.strip().split(',')
                    obj = {"jobid": int(jobid), "catid": int(catid), "skillName": skillName, \
                    "distance": distance}
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
                    obj = {"jobid": int(jobid), "cvid": int(cvid), "distance": distance}
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
def main():
    client = MongoClient('localhost', 27017)
    db = client['thesis-database']

    # tfidf_cv_category(db)
    # tfidf_job_category(db)
    # tfidf_job_cv(db)
    # tfidf2_cv_category(db)
    # tfidf2_job_category(db)
    # tfidf2_job_cv(db)
    # countvectorizer_cv_category(db)
    # countvectorizer_job_category(db)
    # countvectorizer_job_cv(db)
    # word2vec_cv_category(db)
    # word2vec_job_category(db)
    # word2vec_job_cv(db)
    # write_all_jobs(db)
    write_all_categories(db)

if __name__ == '__main__':
    main()
