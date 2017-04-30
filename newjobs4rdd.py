import os
import json
from pathlib import Path


def main():

    jobid = 0
    for a_dir in os.listdir('newjobs'):
        for filename in os.listdir('newjobs/'+a_dir):
            fullpath = os.getcwd() + '/newjobs/' + a_dir + '/' + filename
            try:
                fullstr = Path(fullpath).read_text().strip().replace('\n', ' ').replace('\t', ' ')
                blacklist = ['•', '━', '←', '☆', '□', '×', '*', '🌎','--', '☰', '📁',\
                 '', '>>', '[ ]', '📅', '●', '\\', '>', '🔍']
                for ch in blacklist:
                    fullstr = fullstr.replace(ch, ' ')
                fullstr = ' '.join(fullstr.split())
                jeysan = {"jobid": jobid, "description": fullstr}
                jobid += 1
                with open('newjobs4rdd/newjobs.jsonl', mode="a") as text_file:
                    text_file.write(json.dumps(jeysan, ensure_ascii=False) + u"\n")
            except:
                print(fullpath)



if __name__ == '__main__':
    main()
