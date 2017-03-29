# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path
import sys
import codecs
def main():
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
