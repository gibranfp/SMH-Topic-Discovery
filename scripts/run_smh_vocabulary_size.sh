#!/bin/bash
#
# Script to discover topics with SMH on the Reuters corpus using different vocabulary sizes (20000, 40000, 60000, 80000, 100000)
#
# It receives directory for SMH experiments as argument
mkdir -p $1/reuters/vocabulary_size

for VOCSIZE in 20000 40000 60000 80000 100000
do
python python/discovery/smh_topic_discovery.py \
    --tuple_size 2 \
    --cooccurrence_threshold 0.04 \
    --corpus data/reuters/reuters$VOCSIZE.corpus \
    --overlap 0.90 \
    --min_set_size 3 \
    data/reuters/reuters$VOCSIZE.ifs \
    data/reuters/reuters$VOCSIZE.vocab \
    $1/reuters/vocabulary_size/
done
