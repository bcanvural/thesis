from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)
HOST = "127.0.0.1"
PORT = 5000

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

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
