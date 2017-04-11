from pymongo import MongoClient
import os
from pathlib import Path
def main():
    client = MongoClient('localhost', 27017)
    db = client['thesis-database']
    #tfidf-cv-category
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
                    obj = {"cvid": cvid, "catid": catid, "skillName": skillName, \
                    "similarity": similarity}
                    collection.insert_one(obj)
    #tfidf-job-category
    #tfidf-job-cv
    #tfidf2-cv-category
    #tfidf2-job-category
    #tfidf2-job-cv
    #countvectorizer-cv-category
    #countvectorizer-job-category
    #countvectorizer-job-cv
    #word2vec-cv-category
    #word2vec-cv-category
    #word2vec-job-cv

if __name__ == '__main__':
    main()
