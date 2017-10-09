#!/bin/bash
#
# Script to evaluate LDA topics on topic discovery.
#
mkdir -p $1

for K in 200 400
do
    echo "Discovering $K topics using LDA"
    python python/discovery/lda_topic_discovery.py \
        --number_of_topics K \
        data/reuters/min_docterms0/reuters100000.corpus \
        data/reuters/min_docterms0/reuters100000.vocab \
        $1
done
