#!/bin/bash

# Tokenize Sentences
../../../moses_decoder/scripts/tokenizer/tokenizer.perl -l es < religious/Bible.shi > religious/Bible.tok.shi
../../../moses_decoder/scripts/tokenizer/tokenizer.perl -l es < religious/Bible.spa > religious/Bible.tok.spa

# Generate Vocabulary, Sentence, and Concurrence Files
../../../giza-pp/GIZA++-v2/plain2snt.out religious/Bible.tok.shi religious/Bible.tok.spa
../../../giza-pp/GIZA++-v2/snt2cooc.out religious/Bible.tok.spa religious/Bible.tok.shi religious/Bible.tok.spa_Bible.tok.shi.snt > religious/Bible_Corp.cooc

# Align Words in Sentences
../../../giza-pp/GIZA++-v2/GIZA++ -S religious/Bible.tok.spa.vcb -T religious/Bible.tok.shi.vcb -C religious/Bible.tok.spa_Bible.tok.shi.snt -o Bible_Words -outputpath religious/word_alignment