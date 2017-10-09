#!/bin/bash
#
# Script to evaluate SMH on topic discovery with different co-occurrence thresholds (0.02, 0.04, 0.06, 0.08 and 0.10)
#
mkdir -p $1

for C in 0.04 0.06 0.08 0.10 0.12
do
    echo "Discovering topics with SMH (co-occurrence threshold = $C)"
    python python/discovery/smh_topic_discovery.py \
        --tuple_size 2 \
        --cooccurrence_threshold $C \
        --corpus data/reuters/min_docterms0/reuters100000.corpus \
        --overlap 0.90 \
        --min_set_size 3 \
        data/reuters/min_docterms0/reuters100000.ifs \
        data/reuters/min_docterms0/reuters100000.vocab \
        $1
done

mkdir -p $1/topK
FILES=`ls $1/*_top10.topics`
for F in $FILES
do
    filepath="${F%.*}"
    filename=$(basename $F)
    filename="${filename%.*}"
    for K in 200 400 600 800 1000
    do
        echo "Getting top $K topics from $F to $1/topK/$filename.k$K.topics"
        head -n $K $F > $1/topK/$filename.k$K.topics
    done
done
