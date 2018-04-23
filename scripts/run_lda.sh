#!/bin/bash
#
# Script to discover topics with LDA from the NIPS, 20 Newsgroups and Reuters corpora.
#
# It receives directory for SMH experiments as argument
mkdir -p $1/20newsgroups
mkdir -p $1/reuters

for K in 200 400
do
    echo "Discovering $K topics using LDA"
    python python/discovery/lda_topic_discovery.py \
        --number_of_topics K \
        data/20newsgroups/20newsgroups20000.corpus \
        data/20newsgroups/20newsgroups20000.vocab \
        $1/20newsgroups/

    echo "Discovering $K topics using LDA"
    python python/discovery/lda_topic_discovery.py \
        --number_of_topics K \
        data/reuters/reuters100000.corpus \
        data/reuters/reuters100000.vocab \
        $1/reuters/
done
