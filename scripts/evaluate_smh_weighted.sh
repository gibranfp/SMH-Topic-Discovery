#!/bin/bash
#
# Script to evaluate SMH on topic discovery with different weighting schemes (binary, tf and tf-ids)
#
mkdir -p $1/binary
mkdir -p $1/tf

# binary
python python/discovery/smh_topic_discovery.py \
    --tuple_size 2 \
    --cooccurrence_threshold 0.04 \
    --overlap 0.90 \
    --min_set_size 3 \
    data/reuters/weighted/reuters100000.ifs \
    data/reuters/weighted/reuters100000.vocab \
    $1/binary/

# tf
python python/discovery/smh_topic_discovery.py \
    --tuple_size 2 \
    --cooccurrence_threshold 0.04 \
    --corpus data/reuters/weighted/reuters100000.corpus \
    --overlap 0.90 \
    --min_set_size 3 \
    data/reuters/weighted/reuters100000.ifs \
    data/reuters/weighted/reuters100000.vocab \
    $1/tf/

mkdir -p $1/binary/topK
FILES=`ls $1/binary/*_top10.topics`
for F in $FILES
do
    filepath="${F%.*}"
    filename=$(basename $F)
    filename="${filename%.*}"
    for K in 200 400 600 800 1000
    do
        echo "Getting top $K topics from $F to $1/binary/topK/$filename.k$K.topics"
        head -n $K $F > $1/binary/topK/$filename.k$K.topics
    done
done

mkdir -p $1/tf/topK
FILES=`ls $1/tf/*_top10.topics`
for F in $FILES
do
    filepath="${F%.*}"
    filename=$(basename $F)
    filename="${filename%.*}"
    for K in 200 400 600 800 1000
    do
        echo "Getting top $K topics from $F to $1/tf/topK/$filename.k$K.topics"
        head -n $K $F > $1/tf/topK/$filename.k$K.topics
    done
done
