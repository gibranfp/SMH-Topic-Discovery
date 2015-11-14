#!/bin/bash

mkdir -p exps/exp6
mkdir -p exps/exp6/figs
mkdir -p exps/exp6/models
mkdir -p exps/exp6/topics

time python python/experiments.py\
    --model_pref exps/exp6/models/reuters_\
    --fig_pref exps/exp6/figs/reuters_\
    --topics_pref exps/exp6/topics/reuters_\
    --clus --min_cluster_size 5\
    --min_coherence 2.0\
    --cutoff 3\
    -p 3 0.13\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/reuters/reuters.train.voca\
    data/reuters/reuters.train.tf.ifs\
    data/reuters/reuters.train.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs

time python python/experiments.py\
    --model_pref exps/exp6/models/reuters30k_\
    --fig_pref exps/exp6/figs/reuters30k_\
    --topics_pref exps/exp6/topics/reuters30k_\
    --clus --min_cluster_size 5\
    --min_coherence 2.0\
    --cutoff 3\
    -p 3 0.13\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/reuters/reuters30k.train.voca\
    data/reuters/reuters30k.train.tf.ifs\
    data/reuters/reuters30k.train.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs


time python python/experiments.py\
    --model_pref exps/exp6/models/wiki100k_\
    --fig_pref exps/exp6/figs/wiki100k_\
    --topics_pref exps/exp6/topics/wiki100k_\
    --clus --min_cluster_size 5\
    --min_coherence 2.0\
    --cutoff 3\
    -p 3 0.13\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/wikipedia/wiki100k.vocab\
    data/wikipedia/wiki100k.train.tf.ifs\
    data/wikipedia/wiki100k.train.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs



time python python/experiments.py\
    --model_pref exps/exp6/models/wiki_\
    --fig_pref exps/exp6/figs/wiki_\
    --topics_pref exps/exp6/topics/wiki_\
    --clus --min_cluster_size 5\
    --min_coherence 2.0\
    --cutoff 3\
    -p 3 0.13\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/wikipedia/wiki.vocab\
    data/wikipedia/wiki.train.tf.ifs\
    data/wikipedia/wiki.train.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs


