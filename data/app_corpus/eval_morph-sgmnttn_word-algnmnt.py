import sys
import csv
import subprocess

import chana.pos_tagger

src_shi_spa_file_name = sys.argv[1]

shi_sentences = []

actual_shi_morph_sentences = []

morph_sgmnttn_correct = 0
morph_sgmnttn_incorrect = 0

pos_tagger = chana.pos_tagger.ShipiboPosTagger()

with open(src_shi_spa_file_name, "r", newline="") as src_shi_spa_file:
    
    corpus_reader = csv.reader(src_shi_spa_file)
    
    next(src_shi_spa_file)
    
    for row in corpus_reader:
        shi_sentences.append(row[0].strip().lower().translate(row[0].strip().lower().maketrans("", "", r"[?!.,;:¿¡]")))
        actual_shi_morph_sentences.append(row[2].strip().lower().translate(row[2].strip().lower().maketrans("", "", r"[?!.,;:¿¡]")))

for sentence_index, sentence in enumerate(shi_sentences):

    sentence_pos_tags = pos_tagger.pos_tag(sentence)

    command = ["echo", sentence]
    process_1 = subprocess.Popen(command, stdout=subprocess.PIPE, cwd="../../../morph_analyzer_shi/foma_files/")
    process_2 = subprocess.Popen(["xargs", "-n1"], stdin=process_1.stdout, stdout=subprocess.PIPE, cwd="../../../morph_analyzer_shi/foma_files/")
    process_3 = subprocess.Popen(["flookup", "morph_shk.fst"], stdin=process_2.stdout, stdout=subprocess.PIPE, cwd="../../../morph_analyzer_shi/foma_files/")
    output, error = process_3.communicate()

    if error == None:

        sent_morph_segments = output.decode("utf-8").split("\n\n")

        sentence_length = len(sentence.split())

        new_sentence = ""

        for word_index in range(sentence_length):

            if "+?" not in sent_morph_segments[word_index]:

                word_morph_segments = sent_morph_segments[word_index].split("\n")

                pos_tag_found = False

                for word_morph_segment in word_morph_segments:

                    if sentence_pos_tags[word_index] in word_morph_segment:

                        morphemes = word_morph_segment.split("\t")[1].split()[1:]

                        morphemes_str = ""
                        for morpheme in morphemes:
                            morphemes_str += morpheme.split("[")[0] + "-"
                        morphemes_str = morphemes_str[:-1]

                        if morphemes_str == actual_shi_morph_sentences[sentence_index].split()[word_index]:
                            morph_sgmnttn_correct += 1
                        else:
                            morph_sgmnttn_incorrect += 1

                        pos_tag_found = True

                        new_sentence += morphemes_str + " "

                        break

                if not pos_tag_found:

                    morphemes = word_morph_segments[0].split("\t")[1].split()[1:]

                    morphemes_str = ""
                    for morpheme in morphemes:
                        morphemes_str += morpheme.split("[")[0] + "-"
                    morphemes_str = morphemes_str[:-1]

                    if morphemes_str == actual_shi_morph_sentences[sentence_index].split()[word_index]:
                        morph_sgmnttn_correct += 1
                    else:
                        morph_sgmnttn_incorrect += 1

                    new_sentence += morphemes_str + " "

            else:

                if sentence.split()[word_index] == actual_shi_morph_sentences[sentence_index].split()[word_index]:
                    morph_sgmnttn_correct += 1
                else:
                    morph_sgmnttn_incorrect += 1

                new_sentence += sentence.split()[word_index] + " "

        new_sentence = new_sentence[:-1]

        print(str(sentence_index + 1) + "/" + str(len(shi_sentences)) + "\t" + new_sentence + "\n")

print("Morphological Segmentation Accuracy: " + str(round(morph_sgmnttn_correct / (morph_sgmnttn_correct + morph_sgmnttn_incorrect), 4) * 100) + "%")