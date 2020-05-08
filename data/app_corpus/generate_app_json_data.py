import sys
import string
import subprocess
import re
import json

import chana.pos_tagger
import chana.ner
import chana.syllabificator as syllabificator
import stanza

src_shi_file_name = sys.argv[1]
src_spa_file_name = sys.argv[2]
src_shi_tok_file_name = sys.argv[3]
src_spa_tok_file_name = sys.argv[4]
src_viterbi_alignment_file_name = sys.argv[5]
target_file_name = sys.argv[6]

app_json_data = {}

entry_id = 0

with open(src_shi_file_name, "r") as src_shi_file, open(src_spa_file_name, "r") as src_spa_file:
    for shi_sentence, spa_sentence in zip(src_shi_file, src_spa_file):
        app_json_data[str(entry_id)] = {"id": entry_id, "shi_sentence": shi_sentence.strip().capitalize(), "spa_sentence": spa_sentence.strip().capitalize()}
        entry_id += 1
entry_id = 0

with open(src_shi_tok_file_name, "r") as src_shi_tok_file, open(src_spa_tok_file_name, "r") as src_spa_tok_file:
    for shi_tok_sentence, spa_tok_sentence in zip(src_shi_tok_file, src_spa_tok_file):
        app_json_data[str(entry_id)]["shi_tok_sentence"] = shi_tok_sentence.strip()
        app_json_data[str(entry_id)]["spa_tok_sentence"] = spa_tok_sentence.strip()
        entry_id += 1

sentence_count = len(app_json_data)

pos_tagger = chana.pos_tagger.ShipiboPosTagger()
named_entity_recognizer = chana.ner.ShipiboNER()
stanza_pipeline = stanza.Pipeline("es")

for entry_id_str in app_json_data:
    
    shi_tok_sentence = app_json_data[entry_id_str]["shi_tok_sentence"]

    # POS Tagging: Shipibo-Conibo Sentence
    app_json_data[entry_id_str]["shi_pos_tags"] = pos_tagger.pos_tag(shi_tok_sentence)

    # Named Entity Recognition: Shipibo-Conibo Sentence
    app_json_data[entry_id_str]["shi_named_entities"] = dict(zip(shi_tok_sentence.split(), named_entity_recognizer.crf_tag(shi_tok_sentence)))

    # Syllabification: Shipibo-Conibo Sentence
    shi_word_syllables = ""
    for word in shi_tok_sentence.split():
        for syllable in syllabificator.syllabify(word):
            shi_word_syllables += syllable + "-"
        shi_word_syllables = shi_word_syllables[:-1] + " "
    shi_word_syllables = shi_word_syllables[:-1]
    app_json_data[entry_id_str]["shi_word_syllables"] = dict(zip(shi_tok_sentence.split(), shi_word_syllables.split()))

    # POS Tagging: Spanish Sentence
    stanza_doc = stanza_pipeline(app_json_data[entry_id_str]["spa_tok_sentence"])
    app_json_data[entry_id_str]["spa_pos_tags"] = [spa_word.upos for spa_tok_sentence in stanza_doc.sentences for spa_word in spa_tok_sentence.words]

    # Morphological Segmentation: Shipibo-Conibo Sentence

    command = ["echo", shi_tok_sentence]
    process_1 = subprocess.Popen(command, stdout=subprocess.PIPE, cwd="../../../morph_analyzer_shi/foma_files/")
    process_2 = subprocess.Popen(["xargs", "-n1"], stdin=process_1.stdout, stdout=subprocess.PIPE, cwd="../../../morph_analyzer_shi/foma_files/")
    process_3 = subprocess.Popen(["flookup", "morph_shk.fst"], stdin=process_2.stdout, stdout=subprocess.PIPE, cwd="../../../morph_analyzer_shi/foma_files/")
    output, error = process_3.communicate()

    if error == None:
        
        shi_sent_morph_segments = output.decode("utf-8").split("\n\n")

        shi_sentence_length = len(shi_tok_sentence.split())

        shi_morph_grps_indices = []
        shi_morph_idx = 0

        shi_word_morphemes = ""

        for word_index in range(shi_sentence_length):

            if "+?" not in shi_sent_morph_segments[word_index]:
            
                word_morph_segments = shi_sent_morph_segments[word_index].split("\n")

                pos_tag_found = False
                
                for word_morph_segment in word_morph_segments:
                    
                    if app_json_data[entry_id_str]["shi_pos_tags"][word_index] in word_morph_segment:
                        
                        word_morphemes = word_morph_segment.split("\t")[1].split()[1:]
                        
                        word_morphemes_str = ""
                        shi_morph_grp_indices = []
                        for word_morpheme in word_morphemes:
                            word_morphemes_str += word_morpheme.split("[")[0] + " "
                            shi_morph_grp_indices.append(shi_morph_idx)
                            shi_morph_idx += 1
                        word_morphemes_str = word_morphemes_str[:-1]
                        shi_morph_grps_indices.append(shi_morph_grp_indices)

                        pos_tag_found = True
                        
                        shi_word_morphemes += word_morphemes_str + " "

                        break

                if not pos_tag_found:

                    word_morphemes = word_morph_segments[0].split("\t")[1].split()[1:]
                        
                    word_morphemes_str = ""
                    shi_morph_grp_indices = []
                    for word_morpheme in word_morphemes:
                        word_morphemes_str += word_morpheme.split("[")[0] + " "
                        shi_morph_grp_indices.append(shi_morph_idx)
                        shi_morph_idx += 1
                    word_morphemes_str = word_morphemes_str[:-1]
                    shi_morph_grps_indices.append(shi_morph_grp_indices)

                    shi_word_morphemes += word_morphemes_str + " "

            else:
                shi_morph_grps_indices.append([shi_morph_idx])
                shi_morph_idx += 1
                shi_word_morphemes += shi_tok_sentence.split()[word_index] + " "

        shi_word_morphemes = shi_word_morphemes[:-1]

        app_json_data[entry_id_str]["shi_morph_grps_indices"] = shi_morph_grps_indices
        app_json_data[entry_id_str]["shi_word_morphemes"] = shi_word_morphemes

        print(str(app_json_data[entry_id_str]["id"] + 1) + "/" + str(sentence_count) + "\t" + json.dumps(app_json_data[entry_id_str], ensure_ascii=False) + "\n")

# Words/Morphemes Alignment: Shipibo-Conibo and Spanish Sentences

viterbi_alignment_lines = []

with open(src_viterbi_alignment_file_name, "r") as src_viterbi_alignment_file:
    viterbi_alignment_lines = src_viterbi_alignment_file.readlines()

index = 0

for i in range(2, len(viterbi_alignment_lines), 3):

    spa_words = [x for x in re.findall(r"[\w]+|[?!.,;:¿¡]", viterbi_alignment_lines[i]) if not x.isdigit()]

    shi_morph_grps_indices = [x.strip().split() for x in re.findall(r"\{(.*?)\}", viterbi_alignment_lines[i])]

    alignment = {}
    for spa_word, shi_morph_grp_indices in dict(zip(spa_words, shi_morph_grps_indices)).items():
        if spa_word != "NULL" and spa_word not in string.punctuation and spa_word != "¿" and spa_word != "¡" and shi_morph_grp_indices:
            alignment[spa_word] = [int(x) - 1 for x in shi_morph_grp_indices]

    app_json_data[str(index)]["alignment"] = alignment

    index += 1

with open(target_file_name, "w") as target_file:
    json.dump(app_json_data, target_file, ensure_ascii=False)