# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path

def main():
    dir_path = "alljobs4rdd"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    jobs_file_path = "alljobs4rdd/alljobs.jsonl"
    my_file = Path(jobs_file_path)
    if my_file.is_file():
        os.remove(jobs_file_path)
    path = os.getcwd() + '/jobs/'
    jobid = 0
    for filename in os.listdir(path):
        fullpath = path + filename
        contents = Path(fullpath).read_text().strip()
        try:
            jeysan = json.loads(contents)
            jeysan["jobId"] = jobid
            jobid += 1
            with open('alljobs4rdd/alljobs.jsonl', mode="a") as text_file:
                text_file.write(json.dumps(jeysan, ensure_ascii=False) + u"\n")

        except ValueError:
            print(filename)
            continue
if __name__ == '__main__':
    main()
