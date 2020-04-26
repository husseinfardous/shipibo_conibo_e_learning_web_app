import sys
import csv

src_file_name = sys.argv[1]
target_shi_file_name = sys.argv[2]
target_spa_file_name = sys.argv[3]

shi_sentences = []
spa_sentences = []

with open(src_file_name, "r", newline="", encoding="latin-1") as src_file:

    corpus_reader = csv.reader(src_file)

    for row in corpus_reader:
        shi_sentences.append(row[2].capitalize() + ".")
        spa_sentences.append(row[3].capitalize() + ".")

with open(target_shi_file_name, "w") as target_shi_file:
    for shi_sentence in shi_sentences:
        target_shi_file.write(shi_sentence + "\n")

with open(target_spa_file_name, "w") as target_spa_file:
    for spa_sentence in spa_sentences:
        target_spa_file.write(spa_sentence + "\n")