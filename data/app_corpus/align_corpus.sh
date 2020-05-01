#!/bin/bash

# Generate Vocabulary, Sentence, and Concurrence Files
../../../giza-pp/GIZA++-v2/plain2snt.out data/Corpus_Morphemes.tok.shi data/Corpus.tok.spa
../../../giza-pp/GIZA++-v2/snt2cooc.out data/Corpus.tok.spa data/Corpus_Morphemes.tok.shi data/Corpus.tok.spa_Corpus_Morphemes.tok.shi.snt > data/Corpus.cooc

# Align Words/Morphemes in Sentences
../../../giza-pp/GIZA++-v2/GIZA++ -S data/Corpus.tok.spa.vcb -T data/Corpus_Morphemes.tok.shi.vcb -C data/Corpus.tok.spa_Corpus_Morphemes.tok.shi.snt -o Corpus_Words_Morphemes -outputpath data/alignment