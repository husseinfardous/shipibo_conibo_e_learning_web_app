#!/bin/bash

# Generate Vocabulary, Sentence, and Concurrence Files
../../../giza-pp/GIZA++-v2/plain2snt.out gold_standard/Morph-Sgmnttn_Word-Algnmnt_Morphemes.tok.shi gold_standard/Morph-Sgmnttn_Word-Algnmnt.tok.spa
../../../giza-pp/GIZA++-v2/snt2cooc.out gold_standard/Morph-Sgmnttn_Word-Algnmnt.tok.spa gold_standard/Morph-Sgmnttn_Word-Algnmnt_Morphemes.tok.shi gold_standard/Morph-Sgmnttn_Word-Algnmnt.tok.spa_Morph-Sgmnttn_Word-Algnmnt_Morphemes.tok.shi.snt > gold_standard/Morph-Sgmnttn_Word-Algnmnt.cooc

# Align Words/Morphemes in Sentences
../../../giza-pp/GIZA++-v2/GIZA++ -S gold_standard/Morph-Sgmnttn_Word-Algnmnt.tok.spa.vcb -T gold_standard/Morph-Sgmnttn_Word-Algnmnt_Morphemes.tok.shi.vcb -C gold_standard/Morph-Sgmnttn_Word-Algnmnt.tok.spa_Morph-Sgmnttn_Word-Algnmnt_Morphemes.tok.shi.snt -o Morph-Sgmnttn_Word-Algnmnt_Words_Morphemes -outputpath gold_standard/alignment