
#Small script that collects all job ads in one file
import os
from pathlib import Path
import json

def main():
    try:
        os.remove('jobs-collected')
    except OSError:
        pass

    path = os.getcwd() + '/jobs/'
    jobid = 0
    for filename in os.listdir(path):
        fullpath = path + filename
        contents = Path(fullpath).read_text().strip()
        try:
            jeysan = json.loads(contents)
            jeysan["jobId"] = jobid
            jobid += 1
            with open('jobs-collected', mode="a") as text_file:
                text_file.write(jeysan['description'] + u"\n")
        except ValueError:
            print('value error' + filename)
            continue
        except KeyError:
            print('key error' + filename)




if __name__ == '__main__':
    main()
