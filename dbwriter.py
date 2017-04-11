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

def main():
    client = MongoClient('localhost', 27017)
    db = client['thesis-database']

    # tfidf_cv_category(db)
    # tfidf_job_category(db)
    # tfidf_job_cv(db)
    # tfidf2_cv_category(db)
    # tfidf2_job_category(db)


    #tfidf2-job-cv
    #countvectorizer-cv-category
    #countvectorizer-job-category
    #countvectorizer-job-cv
    #word2vec-cv-category
    #word2vec-cv-category
    #word2vec-job-cv

if __name__ == '__main__':
    main()
