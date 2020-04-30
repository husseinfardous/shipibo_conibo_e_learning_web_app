#!/bin/bash

# Tokenize Sentences
../../../moses_decoder/scripts/tokenizer/tokenizer.perl -l es < data/Corpus.shi > data/Corpus.tok.shi
../../../moses_decoder/scripts/tokenizer/tokenizer.perl -l es < data/Corpus.spa > data/Corpus.tok.spa