# Script that processes cv files placed under CVs/ to make them processable by Spark
# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path
import sys
import codecs
def main():
    dir_path = "allcvs4rdd"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    cvs_file_path = "allcvs4rdd/allcvs.jsonl"
    my_file = Path(cvs_file_path)
    if my_file.is_file():
        os.remove(cvs_file_path)
    path = os.getcwd() + '/CVs/'
    for filename in os.listdir(path):
        fullpath = path + filename
        contents = Path(fullpath).read_text().strip()
        try:
            jeysan = json.loads(contents)
            with open('allcvs4rdd/allcvs.jsonl', mode="a") as text_file:
                text_file.write(json.dumps(jeysan, ensure_ascii=False) + u"\n")

        except ValueError:
            print(filename)
            continue
if __name__ == '__main__':
    main()
