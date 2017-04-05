# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path
import sys
import codecs
def main():
    path = os.getcwd() + '/Categories/'
    counter = 0
    for dirname in os.listdir(path):
        category_path = path + dirname
        for filename in os.listdir(category_path):
            if filename[-3:] == "txt":
                try:
                    fullpath = category_path + '/' + filename
                    fullstr = Path(fullpath).read_text().strip()
                    jeysan = {}
                    jeysan['category'] = dirname ;
                    jeysan['skillName'] = filename[:-3]
                    jeysan['skillText'] = fullstr
                    jeysan['id'] = counter
                    counter += 1
                    with open('allcategories4rdd/allcategories.jsonl', mode="a") as text_file:
                        text_file.write(json.dumps(jeysan, ensure_ascii=False) + u"\n")
                except:
                    print(fullpath)
                    continue

if __name__ == '__main__':
    main()
