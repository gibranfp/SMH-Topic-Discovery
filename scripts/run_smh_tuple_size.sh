#!/bin/bash
#
# Script to discover topics with SMH using different tuple sizes (2, 3 and 4)
#
# It receives directory for SMH experiments as argument
mkdir -p $1/reuters/tuple_size

for TUPLE_SIZE in 2 3 4
do
    echo "Discovering topics with SMH (tuple size = $TUPLE_SIZE)"
    python python/discovery/smh_topic_discovery.py \
        --tuple_size $TUPLE_SIZE \
        --cooccurrence_threshold 0.08 \
        --corpus data/reuters/reuters100000.corpus \
        --overlap 0.90 \
        --min_set_size 3 \
        data/reuters/reuters100000.ifs \
        data/reuters/reuters100000.vocab \
        $1/reuters/tuple_size/
done
