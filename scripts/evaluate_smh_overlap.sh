#!/bin/bash
#
# Script to evaluate SMH on topic discovery with different overlap thresholds (0.5, 0.6, 0.7, 0.8, 0.9 and 1.00)
#
mkdir -p $1

for OVERLAP in 0.5 0.6 0.7 0.8 0.9 1.0 
do
python python/discovery/smh_topic_discovery.py \
    --tuple_size 2 \
    --cooccurrence_threshold 0.04 \
    --corpus data/reuters/min_docterms0/reuters100000.corpus \
    --overlap $OVERLAP \
    --min_set_size 3 \
    data/reuters/min_docterms0/reuters100000.ifs \
    data/reuters/min_docterms0/reuters100000.vocab \
    $1/
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
