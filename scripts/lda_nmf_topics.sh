#!/bin/bash
#
# Topic discovery based on LDA and NMF with different topic numbers (parameter K)

# creates directories
mkdir -p experiments/lda_nmf

for i in {0..7}; do
    python python/topic_discovery/lda_nmf_topic_discovery.py \
           $1 \
           $2 \
           $3 \
           -c $i
done
