import sys

src_file_name = sys.argv[1]
target_shi_file_name = sys.argv[2]
target_spa_file_name = sys.argv[3]

shi_sentences = []
spa_sentences = []

with open(src_file_name, "r") as src_file:
    
    for line in src_file:
        
        shi_spa_sentences = []

        shi_spa_sentences_temp = line.strip()[1:-1].split(",")[3:]
        for sentence in shi_spa_sentences_temp:
            shi_spa_sentences.append(sentence.strip().strip('\"'))
        
        if shi_spa_sentences[0].endswith("?") or shi_spa_sentences[0].endswith("."):
            shi_sentences.append(shi_spa_sentences[0].lower())
        else:
            shi_sentences.append(shi_spa_sentences[0].lower() + ".")

        if shi_spa_sentences[1].endswith("?") or shi_spa_sentences[1].endswith("."):
            spa_sentences.append(shi_spa_sentences[1].lower())
        else:
            spa_sentences.append(shi_spa_sentences[1].lower() + ".")

with open(target_shi_file_name, "w") as target_shi_file:
    for shi_sentence in shi_sentences:
        target_shi_file.write(shi_sentence + "\n")

with open(target_spa_file_name, "w") as target_spa_file:
    for spa_sentence in spa_sentences:
        target_spa_file.write(spa_sentence + "\n")