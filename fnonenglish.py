#Script that removes non english jobs
import os
from pathlib import Path
import json
from langdetect import detect
def main():
    path = os.getcwd() + '/jobs/'
    ne = []
    for filename in os.listdir(path):
        fullpath = path + filename
        contents = Path(fullpath).read_text().strip()
        try:
            jeysan = json.loads(contents)
            if detect(jeysan["description"]) != 'en':
                ne.append(filename)
        except ValueError:
            #print('value error' + filename)
            continue
        except KeyError:
            #print('key error' + filename)
            continue;
    print(sorted(ne))
    # for filename in ne:
    #     try:
    #         os.remove(path + filename)
    #     except OSError:
    #         continue




if __name__ == '__main__':
    main()
