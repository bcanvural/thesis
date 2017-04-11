from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)
HOST = "127.0.0.1"
PORT = 5000

def get_max_catid():
    cmd = 'tail allcategories4rdd/allcategories.jsonl -n1'
    output = subprocess.check_output(cmd, shell=True).decode("utf-8")
    return json.loads(output)['id']
def validate_method(method):
    if method != 'tfidf' and method != 'tfidf2' and \
    method != 'word2vec' and method != 'countvectorizer':
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
        cmd = 'grep \'"jobId": ' + id + '[,}]\' alljobs4rdd/alljobs.jsonl'
        try:
            output = subprocess.check_output(cmd, shell=True).decode("utf-8")
            if output:
                return jsonify({"response": json.loads(output),"statusCode": 200})
            else:
                return jsonify({"response": {}, "statusCode": 404})
        except:
            return jsonify({"response": {}, "statusCode": 404})

@app.route('/category/<name>', methods=['GET'])
def cat_by_name(name):
    if request.method == 'GET':
        cmd = 'grep \'"skillName": "' + name + '"[,}]\' allcategories4rdd/allcategories.jsonl'
        try:
            output = subprocess.check_output(cmd, shell=True).decode("utf-8")
            if output:
                return jsonify({"response": json.loads(output),"statusCode": 200})
            else:
                return jsonify({"response": {}, "statusCode": 404})
        except:
            return jsonify({"response": {}, "statusCode": 404})

@app.route('/graph', methods=['POST'])
def graph_data():
    if request.method == 'POST':
        try:
            json_data = json.loads(request.get_data().decode('utf-8'))
            job_id = json_data['jobid']
            method = json_data['method'] #tfidf, word2vec, etc..
            validate_method(method)
            cat_id_1 = json_data['cat_id_1']
            cat_id_2 = json_data['cat_id_2']
            cat_id_3 = json_data['cat_id_3']
            cat_id_4 = json_data['cat_id_4']
            cat_id_5 = json_data['cat_id_5']
            validate_cats(cat_id_1, cat_id_2, cat_id_3, cat_id_4, cat_id_5)
            #Fetch 5 best CVs for this job
            #TODO read from DB


            return jsonify({"response": json_data,"statusCode": 200})
        except:
            return jsonify({"response": {}, "statusCode": 404})


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
