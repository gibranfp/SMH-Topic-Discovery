#!/bin/bash
#
# Script to discover topics with SMH using different co-occurrence thresholds (0.04, 0.06, 0.08 and 0.10)
#
# It receives directory for SMH experiments as argument
mkdir -p $1/20newsgroups
mkdir -p $1/reuters/cooccurrence_threshold
mkdir -p $1/wikipedia

for C in 0.04 0.06 0.08 0.10
do
    echo "Discovering topics from 20 Newsgroups with SMH (co-occurrence threshold = $C)"
    python python/discovery/smh_topic_discovery.py \
        --tuple_size 2 \
        --cooccurrence_threshold $C \
        --corpus data/20newsgroups/20newsgroups20000.corpus \
        --overlap 0.90 \
        --min_set_size 3 \
        data/20newsgroups/20newsgroups20000.ifs \
        data/20newsgroups/20newsgroups20000.vocab \
        $1/20newsgroups/

    echo "Discovering topics from Reuters with SMH (co-occurrence threshold = $C)"
    python python/discovery/smh_topic_discovery.py \
        --tuple_size 2 \
        --cooccurrence_threshold $C \
        --corpus data/reuters/reuters100000.corpus \
        --overlap 0.90 \
        --min_set_size 3 \
        data/reuters/reuters100000.ifs \
        data/reuters/reuters100000.vocab \
        $1/reuters/cooccurrence_threshold/

    echo "Discovering topics from English Wikipedia with SMH (co-occurrence threshold = $C)"
    python python/discovery/smh_topic_discovery.py \
        --tuple_size 2 \
        --cooccurrence_threshold $C \
        --corpus data/wikipedia/enwiki1000000.corpus \
        --overlap 0.90 \
        --min_set_size 3 \
        data/wikipedia/enwiki1000000.ifs \
        data/wikipedia/enwiki1000000.vocab \
        $1/wikipedia/

    echo "Discovering topics from Spanish Wikipedia with SMH (co-occurrence threshold = $C)"
    python python/discovery/smh_topic_discovery.py \
        --tuple_size 2 \
        --cooccurrence_threshold $C \
        --corpus data/wikipedia/eswiki1000000.corpus \
        --overlap 0.90 \
        --min_set_size 3 \
        data/wikipedia/eswiki1000000.ifs \
        data/wikipedia/eswiki1000000.vocab \
        $1/wikipedia/
done
