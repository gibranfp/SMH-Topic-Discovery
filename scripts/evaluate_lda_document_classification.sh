#!/bin/bash
#
# Script to evaluate LDA topics on document classification.
#

mkdir -p experiments/document_classification/lda/
## With 100, 200, 300 and 400 topics
for SIZE in {100..400..100}
do
    python python/classification/lda_document_classification.py\
           --number_of_topics $SIZE\
           --path_to_save experiments/document_classification/lda/lda$SIZE.txt &
done
