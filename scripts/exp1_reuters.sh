#!/bin/bash

mkdir -p exps/exp1
mkdir -p exps/exp1/figs
mkdir -p exps/exp1/models
mkdir -p exps/exp1/topics

time python python/experiments.py\
    --model_pref exps/exp1/models/reuters_1_\
    --fig_pref exps/exp1/figs/reuters_1_\
    --topics_pref exps/exp1/topics/reuters_1_\
    --clus --min_cluster_size 5\
    --min_coherence 2.0\
    --cutoff 3\
    -p 3 0.2\
    -p 3 0.18\
    -p 3 0.15\
    -p 3 0.13\
    -p 3 0.10\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/reuters/reuters30k.train.voca\
    data/reuters/reuters30k.train.tf.ifs\
    data/reuters/reuters30k.train.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs


time python python/experiments.py\
    --model_pref exps/exp1/models/reuters_2_\
    --fig_pref exps/exp1/figs/reuters_2_\
    --topics_pref exps/exp1/topics/reuters_2_\
    --clus --min_cluster_size 5\
    --min_coherence 2.0\
    --cutoff 3\
    -p 3 315 -l\
    -p 4 315 -l\
    -p 5 315 -l\
    -p 6 315 -l\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/reuters/reuters30k.train.voca\
    data/reuters/reuters30k.train.tf.ifs\
    data/reuters/reuters30k.train.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs


time python python/experiments.py\
    --model_pref exps/exp1/models/reuters_3_\
    --fig_pref exps/exp1/figs/reuters_3_\
    --topics_pref exps/exp1/topics/reuters_3_\
    --clus --min_cluster_size 5\
    --min_coherence 2.0\
    --cutoff 3\
    -p 3 0.18\
    -p 4 0.18\
    -p 5 0.18\
    -p 6 0.18\
    -p 7 0.18\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/reuters/reuters30k.train.voca\
    data/reuters/reuters30k.train.tf.ifs\
    data/reuters/reuters30k.train.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs


