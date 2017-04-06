#Python file to fetch specific jobs, cvs, categories
from pathlib import Path
import sys
import json
import os
def process(jeysan, property_name):
    if property_name == "all":
        print(json.dumps(jeysan))
        os._exit(0)
    else:
        try:
            print(jeysan[property_name])
            os._exit(0)
        except:
            print("invalid property name")
            os._exit(1)

def main():
    if len(sys.argv) != 4:
        print('Usage: python3 fetch.py type id json_property_name')
        os._exit(1)
    job_type = sys.argv[1] #0 for job, 1 for cv, 2 for category
    resource_id = sys.argv[2]
    property_name = sys.argv[3] #can also be 'all'
    try:
        id_string, fullpath = "", ""
        if(job_type == '0'):
            id_string = "jobId"
            fullpath = 'alljobs4rdd/alljobs.jsonl'
        elif(job_type == '1'):
            id_string = "cvid"
            fullpath = 'allcvs4rdd/allcvs.jsonl'
        elif(job_type == '2'):
            id_string = "id"
            fullpath = 'allcategories4rdd/allcategories.jsonl'
        else:
            print('invalid job type')
            os._exit(1)
        contents = Path(fullpath).read_text().strip()
        line_arr = contents.split('\n')
        for line in line_arr:
            try:
                jeysan = json.loads(line)
                if jeysan[id_string] == int(resource_id):
                    process(jeysan, property_name)
            except ValueError:
                print('ValueError')
                continue
    except BaseException as e:
        print('exceptionda')
        print(str(e))
        os._exit(1)

if __name__ == '__main__':
    main()
