import os
import json
from pathlib import Path
import sys
import operator
def main():
    filepath = 'fpjobs-with-blacklist/'
    fp_obj = {}
    for filename in os.listdir(filepath):
        if filename[-3:] == "csv":
            fullpath = os.getcwd() + '/' + filepath + filename
            with open(fullpath) as f:
                for line in f:
                    words = line.strip().split(",")[0].split(" ")
                    freq = line.strip().split(",")[1]
                    if len(words) == 1:
                        fp_obj[words[0]] = int(freq)
                    else:
                        for word in words:
                            fp_obj.pop(word, None)
                        fp_obj[" ".join(words)] = int(freq)
    out_file = 'fpreduced.txt'
    if len(sys.argv) > 1:
        out_file = sys.argv[1]
    my_file = Path(out_file)
    if my_file.is_file():
        os.remove(out_file)
    fp_sorted = sorted(fp_obj.items(), key=operator.itemgetter(1))[::-1]
    with open(out_file, mode="a") as text_file:
        for key, value in fp_sorted:
            text_file.write(key + " " + str(value) + u"\n")

if __name__ == '__main__':
    main()
