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

        if row[2].endswith("?") or row[2].endswith("."):
            shi_sentences.append(row[2].lower())
        else:
            shi_sentences.append(row[2].lower() + ".")

        if row[3].endswith("?") or row[3].endswith("."):
            spa_sentences.append(row[3].lower())
        else:
            spa_sentences.append(row[3].lower() + ".")

with open(target_shi_file_name, "w") as target_shi_file:
    for shi_sentence in shi_sentences:
        target_shi_file.write(shi_sentence + "\n")

with open(target_spa_file_name, "w") as target_spa_file:
    for spa_sentence in spa_sentences:
        target_spa_file.write(spa_sentence + "\n")