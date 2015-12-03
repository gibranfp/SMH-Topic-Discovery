#!/bin/bash

mkdir -p exps/exp6
mkdir -p exps/exp6/figs
mkdir -p exps/exp6/models
mkdir -p exps/exp6/topics

time python python/experiments.py\
    --model_pref exps/exp6/models/wiki100k_\
    --fig_pref exps/exp6/figs/wiki100k_\
    --topics_pref exps/exp6/topics/wiki100k_\
    --clus --min_cluster_size 5\
    --min_coherence 2.0\
    --cutoff 3\
    -p 3 0.2\
    -p 3 0.18\
    -p 3 0.15\
    -p 3 0.13\
    -p 3 0.10\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/wikipedia/wiki100k.vocab\
    data/wikipedia/wiki100k.train.tf.ifs\
    data/wikipedia/wiki100k.train.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs


