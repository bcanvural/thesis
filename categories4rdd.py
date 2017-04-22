# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path
import sys
import codecs
def main():
    dir_path = "allcategories4rdd"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    category_file_path = "allcategories4rdd/allcategories.jsonl"
    my_file = Path(category_file_path)
    if my_file.is_file():
        os.remove(category_file_path)
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
                    jeysan['skillName'] = filename[:-4]
                    jeysan['skillText'] = fullstr.replace('\n', ' ')
                    jeysan['id'] = counter
                    counter += 1
                    with open('allcategories4rdd/allcategories.jsonl', mode="a") as text_file:
                        text_file.write(json.dumps(jeysan, ensure_ascii=False) + u"\n")
                except:
                    print(fullpath)
                    continue

if __name__ == '__main__':
    main()
