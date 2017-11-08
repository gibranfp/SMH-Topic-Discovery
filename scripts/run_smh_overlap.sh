#!/bin/bash
#
# Script to discover topics with SMH using different overlap thresholds (0.5, 0.6, 0.7, 0.8, 0.9 and 1.00)
#
# It receives directory for SMH experiments as argument
mkdir -p $1/reuters/overlap

for OVERLAP in 0.5 0.6 0.7 0.8 0.9 1.0 
do
python python/discovery/smh_topic_discovery.py \
    --tuple_size 2 \
    --cooccurrence_threshold 0.04 \
    --corpus data/reuters/reuters100000.corpus \
    --overlap $OVERLAP \
    --min_set_size 3 \
    data/reuters/reuters100000.ifs \
    data/reuters/reuters100000.vocab \
    $1/reuters/overlap/
done
