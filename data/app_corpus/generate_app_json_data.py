import sys
import string
import subprocess
import re
import json

import chana.pos_tagger
import chana.ner
import chana.syllabificator as syllabificator

src_shi_file_name = sys.argv[1]
src_spa_file_name = sys.argv[2]
src_shi_morph_file_name = sys.argv[3]
src_viterbi_alignment_file_name = sys.argv[4]
target_file_name = sys.argv[5]

app_json_data = {}

entry_id = 0
with open(src_shi_file_name, "r") as src_shi_file, open(src_spa_file_name, "r") as src_spa_file:
    for shi_sentence, spa_sentence in zip(src_shi_file, src_spa_file):
        if entry_id < 500:
            app_json_data[str(entry_id)] = {"id": entry_id, "shi_sentence": shi_sentence.strip(), "spa_sentence": spa_sentence.strip()}
            entry_id += 1
        else:
            break

sentence_count = len(app_json_data)

pos_tagger = chana.pos_tagger.ShipiboPosTagger()
named_entity_recognizer = chana.ner.ShipiboNER()

for entry_id_str in app_json_data:

    shi_sentence = app_json_data[entry_id_str]["shi_sentence"]

    tokenized_shi_sentence = shi_sentence.translate(shi_sentence.maketrans("", "", string.punctuation)).replace("¿", "").replace("¡", "")

    app_json_data[entry_id_str]["shi_pos_tags"] = pos_tagger.pos_tag(tokenized_shi_sentence)

    app_json_data[entry_id_str]["shi_named_entities"] = dict(zip(tokenized_shi_sentence.split(), named_entity_recognizer.crf_tag(tokenized_shi_sentence)))

    shi_word_syllables = ""
    for word in tokenized_shi_sentence.split():
        for syllable in syllabificator.syllabify(word):
            shi_word_syllables += syllable + "-"
        shi_word_syllables = shi_word_syllables[:-1] + " "
    shi_word_syllables = shi_word_syllables[:-1]
    app_json_data[entry_id_str]["shi_word_syllables"] = dict(zip(tokenized_shi_sentence.split(), shi_word_syllables.split()))

    command = ["echo", tokenized_shi_sentence]
    process_1 = subprocess.Popen(command, stdout=subprocess.PIPE, cwd="../../../morph_analyzer_shi/foma_files/")
    process_2 = subprocess.Popen(["xargs", "-n1"], stdin=process_1.stdout, stdout=subprocess.PIPE, cwd="../../../morph_analyzer_shi/foma_files/")
    process_3 = subprocess.Popen(["flookup", "morph_shk.fst"], stdin=process_2.stdout, stdout=subprocess.PIPE, cwd="../../../morph_analyzer_shi/foma_files/")
    output, error = process_3.communicate()

    if error == None:
        
        shi_sent_morph_segments = output.decode("utf-8").split("\n\n")

        shi_sentence_length = len(tokenized_shi_sentence.split())

        shi_word_morphemes = ""

        for word_index in range(shi_sentence_length):

            if "+?" not in shi_sent_morph_segments[word_index]:
            
                word_morph_segments = shi_sent_morph_segments[word_index].split("\n")

                pos_tag_found = False
                
                for word_morph_segment in word_morph_segments:
                    
                    if app_json_data[entry_id_str]["shi_pos_tags"][word_index] in word_morph_segment:
                        
                        word_morphemes = word_morph_segment.split("\t")[1].split()[1:]
                        
                        word_morphemes_str = ""
                        for word_morpheme in word_morphemes:
                            word_morphemes_str += word_morpheme.split("[")[0] + "-"
                        word_morphemes_str = word_morphemes_str[:-1]

                        pos_tag_found = True
                        
                        shi_word_morphemes += word_morphemes_str + " "

                        break

                if not pos_tag_found:

                    word_morphemes = word_morph_segments[0].split("\t")[1].split()[1:]
                        
                    word_morphemes_str = ""
                    for word_morpheme in word_morphemes:
                        word_morphemes_str += word_morpheme.split("[")[0] + "-"
                    word_morphemes_str = word_morphemes_str[:-1]

                    shi_word_morphemes += word_morphemes_str + " "

            else:
                shi_word_morphemes += tokenized_shi_sentence.split()[word_index] + " "

        shi_word_morphemes = shi_word_morphemes[:-1]
        app_json_data[entry_id_str]["shi_word_morphemes"] = shi_word_morphemes

        print(str(app_json_data[entry_id_str]["id"] + 1) + "/" + str(sentence_count) + "\t" + json.dumps(app_json_data[entry_id_str], ensure_ascii=False) + "\n")

shi_morph_sentences = []

with open(src_shi_morph_file_name, "r") as src_shi_morph_file:
    shi_morph_sentences = src_shi_morph_file.readlines()

viterbi_alignment_lines = []

with open(src_viterbi_alignment_file_name, "r") as src_viterbi_alignment_file:
    viterbi_alignment_lines = src_viterbi_alignment_file.readlines()

index = 0

for i in range(2, len(viterbi_alignment_lines), 3):

    if index < 500:

        spa_words = [x for x in re.findall(r'\w+', viterbi_alignment_lines[i]) if not x.isdigit()]

        shi_morphs_indices = [x.strip().split() for x in re.findall(r'\{(.*?)\}', viterbi_alignment_lines[i])]
        
        shi_morphemes = []
        
        shi_morph_sentence = shi_morph_sentences[index].strip().split()
        for j, shi_morphs_indices in enumerate(shi_morphs_indices):
            shi_morphemes.append([shi_morph_sentence[int(k) - 1] for k in shi_morphs_indices])

        alignment = {}
        for spa_word, shi_morphs in dict(zip(spa_words, shi_morphemes)).items():
            if spa_word != "NULL" and shi_morphs:
                alignment[spa_word] = shi_morphs

        reverse_alignment = {}
        for spa_word, shi_morphs in alignment.items():
            for shi_morph in shi_morphs:
                reverse_alignment[shi_morph] = spa_word

        app_json_data[str(index)]["alignment"] = reverse_alignment

        index += 1

    else:
        break

with open(target_file_name, "w") as target_file:
    json.dump(app_json_data, target_file, ensure_ascii=False)