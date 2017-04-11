from pymongo import MongoClient
import os
from pathlib import Path

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
def main():
    client = MongoClient('localhost', 27017)
    db = client['thesis-database']

    tfidf_cv_category(db)
    tfidf_job_category(db)
    tfidf_job_cv(db)
    tfidf2_cv_category(db)
    tfidf2_job_category(db)
    tfidf2_job_cv(db)
    countvectorizer_cv_category(db)
    countvectorizer_job_category(db)
    countvectorizer_job_cv(db)
    word2vec_cv_category(db)
    word2vec_job_category(db)
    word2vec_job_cv(db)

if __name__ == '__main__':
    main()
