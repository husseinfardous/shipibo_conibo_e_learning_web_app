import sys

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
    if len(v.strip().split()) < 13:
        shi_sentences.append(k)
        spa_sentences.append(v)

with open(target_shi_file_name, "w") as target_shi_file:
    for shi_sentence in shi_sentences:
        target_shi_file.write(shi_sentence)

with open(target_spa_file_name, "w") as target_spa_file:
    for spa_sentence in spa_sentences:
        target_spa_file.write(spa_sentence)