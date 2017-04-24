from flask import Flask, request, jsonify
import subprocess
import json
from pymongo import MongoClient
from bson.json_util import loads
import re
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
HOST = "127.0.0.1"
PORT = 5000
client = MongoClient('localhost', 27017)
db = client['thesis-database']

def get_max_catid():
    return db['allcategories'].find().sort("catid", -1).limit(1)[0]["catid"]
def validate_method(method):
    if method not in ['tfidf', 'word2vec', 'countvectorizer', 'word2vec2', 'count-pca']:
        raise
def validate_cats(cat_id_1, cat_id_2, cat_id_3, cat_id_4, cat_id_5):
    #make sure they are distinct
    if len(set([cat_id_1, cat_id_2, cat_id_3, cat_id_4, cat_id_5])) != 5:
        raise
    #make sure they are in accepted range
    if max(cat_id_1, cat_id_2, cat_id_3, cat_id_4, cat_id_5) > get_max_catid():
        raise

@app.route('/job/<id>', methods=['GET'])
def job_by_id(id):
    if request.method == 'GET':
        try:
            collection = db['alljobs']
            doc = collection.find_one({"jobid":int(id)})
            if not doc:
                return jsonify({"response": {}, "statusCode": 404, "message": "Not found"})
            obj = {"jobid": doc['jobid'], "description": doc['description']}
            return jsonify({"response": obj, "statusCode": 200})
        except ValueError:
            return jsonify({"response": {}, "statusCode": 404, "message": "Value error"})
        except:
            return jsonify({"response": {}, "statusCode": 404, "message": "Generic"})
@app.route('/skill/<name>', methods=['GET'])
def cat_by_name(name):
    if request.method == 'GET':
        try:
            collection = db['allcategories']
            doc = collection.find_one({"skillName":name})
            if not doc:
                return jsonify({"response": {}, "statusCode": 404, "message": "Not found"})
            obj = {"skillName": doc['skillName'], "catid": doc['catid'], "category": doc['category']}
            return jsonify({"response": obj, "statusCode": 200})
        except:
            return jsonify({"response": {}, "statusCode": 404, "message": "Generic"})

@app.route('/skillrec', methods=['GET'])
def skillrec():
    if request.method == 'GET':
        try:
            q = request.args['q']
            regex = re.compile('^' + re.escape(q) + '.*', re.IGNORECASE)
            items = db['allcategories'].find({'skillName': { '$regex': regex }}).limit(5)
            if items.count() == 0:
                return jsonify(response=[], statusCode=404, message="Not found")
            else:
                skills_arr = []
                for item in items:
                    item.pop('skillText', None)
                    item.pop('_id', None)
                    skills_arr.append(item)
                return jsonify(response=skills_arr, statusCode=200)
        except:
            return jsonify(response=[], statusCode=404, message="Generic")

@app.route('/graph', methods=['POST'])
def graph_data():
    if request.method == 'POST':
        try:
            json_data = json.loads(request.get_data().decode('utf-8'))
            job_id = int(json_data['jobid'])
            method = json_data['method'] #tfidf, word2vec, etc..
            validate_method(method)
            cat_id_1 = int(json_data['cat_id_1'])
            cat_id_2 = int(json_data['cat_id_2'])
            cat_id_3 = int(json_data['cat_id_3'])
            cat_id_4 = int(json_data['cat_id_4'])
            cat_id_5 = int(json_data['cat_id_5'])
            validate_cats(cat_id_1, cat_id_2, cat_id_3, cat_id_4, cat_id_5)
            pagenum = int(json_data['pagenum'])
            PAGESIZE = 6
            #get job-category similarities
            job_cat_1_sim = db[method +'-job-category'].find_one({"jobid": job_id, "catid": cat_id_1})["distance"]
            job_cat_2_sim = db[method +'-job-category'].find_one({"jobid": job_id, "catid": cat_id_2})["distance"]
            job_cat_3_sim = db[method +'-job-category'].find_one({"jobid": job_id, "catid": cat_id_3})["distance"]
            job_cat_4_sim = db[method +'-job-category'].find_one({"jobid": job_id, "catid": cat_id_4})["distance"]
            job_cat_5_sim = db[method +'-job-category'].find_one({"jobid": job_id, "catid": cat_id_5})["distance"]

            job_diff_obj = {}
            job_diff_obj = {"jobid": job_id, "cat_1_diff": job_cat_1_sim, "cat_2_diff": job_cat_2_sim, "cat_3_diff": \
            job_cat_3_sim, "cat_4_diff": job_cat_4_sim, "cat_5_diff": job_cat_5_sim}

            #Fetch  best CVs for this job
            cv_differences = []
            cvs = db[method + '-job-cv'].find({"jobid": job_id}).sort("distance", 1).skip(PAGESIZE*(pagenum-1)).limit(PAGESIZE)
            if cvs.count() == 0:
                return jsonify({"response": {}, "statusCode": 404, "message": "Not found"})
            for cv in cvs:
                cv_obj = {"cvid": cv['cvid'], "job_similarity": cv["distance"]}
                cv_cat_1_sim = db[method + '-cv-category'].find_one({"cvid": cv['cvid'], "catid": cat_id_1})["distance"]
                cv_cat_2_sim = db[method + '-cv-category'].find_one({"cvid": cv['cvid'], "catid": cat_id_2})["distance"]
                cv_cat_3_sim = db[method + '-cv-category'].find_one({"cvid": cv['cvid'], "catid": cat_id_3})["distance"]
                cv_cat_4_sim = db[method + '-cv-category'].find_one({"cvid": cv['cvid'], "catid": cat_id_4})["distance"]
                cv_cat_5_sim = db[method + '-cv-category'].find_one({"cvid": cv['cvid'], "catid": cat_id_5})["distance"]

                cv_obj["cat_1_diff"] =  cv_cat_1_sim
                cv_obj["cat_2_diff"] =  cv_cat_2_sim
                cv_obj["cat_3_diff"] =  cv_cat_3_sim
                cv_obj["cat_4_diff"] =  cv_cat_4_sim
                cv_obj["cat_5_diff"] =  cv_cat_5_sim

                cv_differences.append(cv_obj)

            final_obj = {"job_diff": job_diff_obj, "cv_differences": cv_differences}
            return jsonify({"response": final_obj,"statusCode": 200})
        except KeyError:
            return jsonify({"response": {}, "statusCode": 404, "message": "Key error"})
        except ValueError:
            return jsonify({"response": {}, "statusCode": 404, "message": "Value error"})
        except:
            return jsonify({"response": {}, "statusCode": 404, "message": "Generic"})

@app.route('/edisongraph', methods=['POST'])
def edison_skills():
    if request.method == 'POST':
        try:
            json_data = json.loads(request.get_data().decode('utf-8'))
            job_id = int(json_data['jobid'])
            method = json_data['method'] #tfidf, word2vec, etc..
            validate_method(method)
            pagenum = int(json_data['pagenum'])
            PAGESIZE = 6
            #get job-category similarities


            job_cat_1_sim = db[method +'-job-category'].find({"jobid": job_id, "category": "Edison"})\
                .sort("distance", 1)\
                .skip(PAGESIZE*(pagenum-1)).limit(PAGESIZE)

            #Fetch  best CVs for this job
            cv_differences = []
            cvs = db[method + '-job-cv'].find({"jobid": job_id}).sort("distance", 1).skip(PAGESIZE*(pagenum-1)).limit(PAGESIZE)
            for cv in cvs:
                cv_obj = {"cvid": cv['cvid'], "job_similarity": cv["distance"]}
                cv_cat_sims = db[method + '-cv-category'].find({"cvid": cv['cvid'], "category": "Edison"}, {"cvid": 1, "category": 1, "_id":0, "distance": 1})


                    # cv_obj["cat_1_diff"] =  cv_cat_1_sim
                    # cv_obj["cat_2_diff"] =  cv_cat_2_sim
                    # cv_obj["cat_3_diff"] =  cv_cat_3_sim
                    # cv_obj["cat_4_diff"] =  cv_cat_4_sim
                    # cv_obj["cat_5_diff"] =  cv_cat_5_sim

                cv_differences.append(cv_obj)


        except:
            return jsonify({"response": {}, "statusCode": 404, "message": "Generic"})

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, threaded=True)
