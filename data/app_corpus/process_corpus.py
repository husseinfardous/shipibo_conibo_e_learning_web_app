import sys
import re

src_shi_file_name_ed = sys.argv[1]
src_spa_file_name_ed = sys.argv[2]
src_shi_file_name_dict_sents = sys.argv[3]
src_spa_file_name_dict_sents = sys.argv[4]

target_shi_file_name = sys.argv[5]
target_spa_file_name = sys.argv[6]

temp_shi_sentences = []
temp_spa_sentences = []

shi_sentences = []
spa_sentences = []

with open(src_shi_file_name_ed, "r") as src_shi_file:
    temp_shi_sentences = src_shi_file.readlines()

with open(src_spa_file_name_ed, "r") as src_spa_file:
    temp_spa_sentences = src_spa_file.readlines()

with open(src_shi_file_name_dict_sents, "r") as src_shi_file:
    temp_shi_sentences += src_shi_file.readlines()

with open(src_spa_file_name_dict_sents, "r") as src_spa_file:
    temp_spa_sentences += src_spa_file.readlines()

for k, v in dict(zip(temp_shi_sentences, temp_spa_sentences)).items():
    
    if len(re.sub(" +", " ", v.strip()).split()) < 13:

        if k.strip().endswith("?") or k.strip().endswith("!") or k.strip().endswith("."):
            shi_sentences.append(re.sub(" +", " ", k.lower().strip()))
        else:
            shi_sentences.append(re.sub(" +", " ", k.lower().strip()) + ".")

        if v.strip().endswith("?") or v.strip().endswith("!") or v.strip().endswith("."):
            spa_sentences.append(re.sub(" +", " ", v.lower().strip()))
        else:
            spa_sentences.append(re.sub(" +", " ", v.lower().strip()) + ".")

with open(target_shi_file_name, "w") as target_shi_file:
    for shi_sentence in shi_sentences:
        target_shi_file.write(shi_sentence + "\n")

with open(target_spa_file_name, "w") as target_spa_file:
    for spa_sentence in spa_sentences:
        target_spa_file.write(spa_sentence + "\n")