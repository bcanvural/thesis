import os
from pathlib import Path
import json

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def get_entities(text):
    import urllib.request
    import urllib.parse
    q_dict = {'lang': 'en', 'gcube-token': '25f9426f-8476-4aae-a512-f364bb8fd9e2-843339462', 'text': text}
    url = "https://tagme.d4science.org/tagme/tag?{0}".format(urllib.parse.urlencode(q_dict))
    try:
        json_obj = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
    except:
        return ['HTML ERROR']
    entity_set = set()
    for annotation in json_obj['annotations']:
        try:
            entity_set.add(annotation['spot'])
        except KeyError:
            continue
    return entity_set

def main():
    path = os.getcwd() + '/BioNLP-ST_2011_GE_devel'
    count = 0
    percentage_sum = 0
    for filename in os.listdir(path):
        if filename[-2:] == "a1":
            fullpath = path + '/' + filename
            fullstr = Path(fullpath).read_text().strip()
            lines = fullstr.split('\n')
            pr_set = set()
            for line in lines:
                if line and line[0] == 'T':
                    line = " ".join(line.strip().split())
                    prs = line.split()[4:]
                    protein = "".join([x for x in " ".join(prs) if len(prs) != 1 or not is_number(prs[0])])
                    if len(protein) > 0:
                        pr_set.add(protein)
            if len(pr_set) > 0:
                textfile = filename[:len(filename)-2] + 'txt'
                fullstr = Path(path+'/'+textfile).read_text().strip()
                entity_set = get_entities(fullstr)

                if entity_set == ['HTML ERROR']:
                    continue

                #lower string all
                pr_set = set([x.lower() for x in list(pr_set)])
                entity_set = set([x.lower() for x in list(entity_set)])
                #

                diff_set = pr_set.difference(entity_set)
                miss_percentage = (len(diff_set) / len(pr_set)) * 100
                with open('biomedscores.txt', mode="a") as text_file:
                        text_file.write(filename + ',' + str(100 - miss_percentage) + "\n")
                count += 1
                percentage_sum += (100 - miss_percentage)
                if miss_percentage > 50:
                    with open('biomedscores-low.txt', mode="a") as text_file:
                        text_file.write(filename + ',' + str(100 - miss_percentage) + ',' + "\n")
                        text_file.write(str(sorted(list(pr_set))) + "\n")
                        text_file.write(str(sorted(list(entity_set))) + "\n")
                        text_file.write(str(sorted(list(diff_set))) + "\n\n")
    print(percentage_sum / count)
            
if __name__ == '__main__':
    main()