#!/bin/bash
#
# Script to evaluate LDA topics on document classification.
#
mkdir -p experiments/topic_discovery/lda/

# On Reuters corpus
FILES=`ls data/reuters/*.corpus`
## With 100, 200, 300 and 400 topics
for SIZE in {100..100..100}
do
    for F in $FILES
    do
        filename=$(basename $F)
        filename="${filename%.*}"
        python python/discovery/lda_topic_discovery.py \
            --number_of_topics $SIZE \
            $F \
            $(dirname $F)/$filename.vocab \
            experiments/topic_discovery/lda/ 
    done
done
