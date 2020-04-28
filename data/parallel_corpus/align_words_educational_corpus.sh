#!/bin/bash

# Tokenize Sentences
../../../moses_decoder/scripts/tokenizer/tokenizer.perl -l es < educational/Tsanas.shi > educational/Tsanas.tok.shi
../../../moses_decoder/scripts/tokenizer/tokenizer.perl -l es < educational/Tsanas.spa > educational/Tsanas.tok.spa

# Generate Vocabulary, Sentence, and Concurrence Files
../../../giza-pp/GIZA++-v2/plain2snt.out educational/Tsanas.tok.shi educational/Tsanas.tok.spa
../../../giza-pp/GIZA++-v2/snt2cooc.out educational/Tsanas.tok.spa educational/Tsanas.tok.shi educational/Tsanas.tok.spa_Tsanas.tok.shi.snt > educational/Tsanas_Corp.cooc

# Align Words in Sentences
../../../giza-pp/GIZA++-v2/GIZA++ -S educational/Tsanas.tok.spa.vcb -T educational/Tsanas.tok.shi.vcb -C educational/Tsanas.tok.spa_Tsanas.tok.shi.snt -o Tsanas_Words -outputpath educational/word_alignment