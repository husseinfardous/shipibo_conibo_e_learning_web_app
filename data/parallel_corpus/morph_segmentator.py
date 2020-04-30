import sys
import re
import subprocess

import chana.pos_tagger

src_shi_file_name = sys.argv[1]
target_shi_file_name = sys.argv[2]

lines_count = 0

with open(src_shi_file_name, "r") as src_shi_file:
    lines_count = len(src_shi_file.readlines())

sentences = []

pos_tagger = chana.pos_tagger.ShipiboPosTagger()

with open(src_shi_file_name, "r") as src_shi_file:
    
    for line_index, line_content in enumerate(src_shi_file):

        sentence = re.sub(" +", " ", line_content.lower().strip()[:-1])

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
                                morphemes_str += morpheme.split("[")[0] + " "
                            morphemes_str = morphemes_str[:-1]

                            pos_tag_found = True
                            
                            new_sentence += morphemes_str + " "

                            break

                    if not pos_tag_found:

                        morphemes = word_morph_segments[0].split("\t")[1].split()[1:]
                            
                        morphemes_str = ""
                        for morpheme in morphemes:
                            morphemes_str += morpheme.split("[")[0] + " "
                        morphemes_str = morphemes_str[:-1]

                        new_sentence += morphemes_str + " "

                else:
                    new_sentence += sentence.split()[word_index] + " "

            new_sentence = new_sentence[:-1] + "."
            sentences.append(new_sentence)

            print(str(line_index + 1) + "/" + str(lines_count) + "\t" + new_sentence + "\n")

with open(target_shi_file_name, "w") as target_shi_file:
    for sentence in sentences:
        target_shi_file.write(sentence + "\n")