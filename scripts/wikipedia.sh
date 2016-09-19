#!/bin/bash

mkdir -p exps/wikipedia
mkdir -p exps/wikipedia/figs
mkdir -p exps/wikipedia/models
mkdir -p exps/wikipedia/topics

time python python/experiments.py\
    --model_pref exps/wikipedia/models/wikies100k_\
    --fig_pref exps/wikipedia/figs/wikies100k_\
    --topics_pref exps/wikipedia/topics/wikies100k_\
    --clus --min_cluster_size 5\
    --min_coherence 0.0\
    --cutoff 5\
    -l\
    -p 2 200\
    -p 2 250\
    -p 2 300\
    -p 2 350\
    -p 2 400\
    -p 2 450\
    -p 2 500\
    --voca-corpus data/wikipedia/wikies.vocab\
    --voca-topics data/wikipedia/wikies100k.vocab\
    data/wikipedia/wikies100k.train.tf.ifs\
    data/wikipedia/wikies100k.train.tf.ifs\
    data/wikipedia/wikies.test.tf.ifs


