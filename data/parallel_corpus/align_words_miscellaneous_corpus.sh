#!/bin/bash

# Tokenize Sentences
../../../moses_decoder/scripts/tokenizer/tokenizer.perl -l es < miscellaneous/Dictionary_Sentences.shi > miscellaneous/Dictionary_Sentences.tok.shi
../../../moses_decoder/scripts/tokenizer/tokenizer.perl -l es < miscellaneous/Dictionary_Sentences.spa > miscellaneous/Dictionary_Sentences.tok.spa

# Generate Vocabulary, Sentence, and Concurrence Files
../../../giza-pp/GIZA++-v2/plain2snt.out miscellaneous/Dictionary_Sentences.tok.shi miscellaneous/Dictionary_Sentences.tok.spa
../../../giza-pp/GIZA++-v2/snt2cooc.out miscellaneous/Dictionary_Sentences.tok.spa miscellaneous/Dictionary_Sentences.tok.shi miscellaneous/Dictionary_Sentences.tok.spa_Dictionary_Sentences.tok.shi.snt > miscellaneous/Dictionary_Sentences_Corp.cooc

# Align Words in Sentences
../../../giza-pp/GIZA++-v2/GIZA++ -S miscellaneous/Dictionary_Sentences.tok.spa.vcb -T miscellaneous/Dictionary_Sentences.tok.shi.vcb -C miscellaneous/Dictionary_Sentences.tok.spa_Dictionary_Sentences.tok.shi.snt -o Dictionary_Sentences_Words -outputpath miscellaneous/word_alignment