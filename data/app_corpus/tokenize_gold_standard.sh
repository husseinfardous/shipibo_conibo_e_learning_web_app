#!/bin/bash

# Tokenize Sentences
../../../moses_decoder/scripts/tokenizer/tokenizer.perl -l es < gold_standard/Morph-Sgmnttn_Word-Algnmnt.shi > gold_standard/Morph-Sgmnttn_Word-Algnmnt.tok.shi
../../../moses_decoder/scripts/tokenizer/tokenizer.perl -l es < gold_standard/Morph-Sgmnttn_Word-Algnmnt.spa > gold_standard/Morph-Sgmnttn_Word-Algnmnt.tok.spa