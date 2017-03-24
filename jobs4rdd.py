# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path
import sys
import codecs
path = os.getcwd() + '/jobs/'
jobid = 0
for filename in os.listdir(path):
    fullpath = path + filename
    contents = Path(fullpath).read_text().strip()
    try:
        jeysan = json.loads(contents)
        # oldway = os.getcwd() + '/jobs4rdd/' + filename
        #
        # with codecs.open(, mode="w+") as text_file:
        #     text_file.write(json.dumps(jeysan, ensure_ascii=False) + "\n")
        jeysan["jobId"] = jobid
        jobid += 1
        with open('alljobs4rdd/alljobs.jsonl', mode="a") as text_file:
            text_file.write(json.dumps(jeysan, ensure_ascii=False) + u"\n")

    except ValueError:
        print(filename)
        continue
