#!/bin/bash
#
# Script to evaluate SMH  on topic discovery
#
mkdir -p $1

# On Reuters corpus
FILES=`ls $2/*$3.ifs`
for THRES in `seq $4 $5 $6`
do
    for F in $FILES
    do
        filepath="${F%.*}"
        filename=$(basename $F)
        filename="${filename%.*}"
        python python/discovery/smh_topic_discovery.py \
            --tuple_size $7 \
            --cooccurrence_threshold $THRES \
            --corpus $filepath.corpus \
            --overlap $8 \
            --min_set_size $9 \
            $F \
            $filepath.vocab \
            $1
    done
done
