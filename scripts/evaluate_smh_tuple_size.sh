#!/bin/bash
#
# Script to evaluate SMH on topic discovery with different tuple sizes (2, 3 and 4)
#
mkdir -p $1

for TUPLE_SIZE in 2 3 4
do
    echo "Discovering topics with SMH (tuple size = $TUPLE_SIZE)"
    python python/discovery/smh_topic_discovery.py \
        --tuple_size $TUPLE_SIZE \
        --cooccurrence_threshold 0.08 \
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
