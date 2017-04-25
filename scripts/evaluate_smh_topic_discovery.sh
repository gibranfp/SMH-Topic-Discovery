#!/bin/bash
#
# Script to evaluate SMH  on topic discovery
#
mkdir -p experiments/topic_discovery/smh/

# On Reuters corpus
FILES=`ls data/reuters/*.ifs`
# Cooccurrence thresholds from 0.1 to 0.2
for THRES in `seq 0.10 0.02 0.20`
do
    for F in $FILES
    do
        filepath="${F%.*}"
        filename=$(basename $F)
        filename="${filename%.*}"
        python python/discovery/smh_topic_discovery.py \
            --tuple_size 3\
            --cooccurrence_threshold $THRES \
            --corpus $filepath.corpus\
            $F \
            $(dirname $F)/$filename.vocab \
            experiments/topic_discovery/smh/ 
    done
done
