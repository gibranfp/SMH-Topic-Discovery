#!/bin/bash

mkdir -p exps/exp1
mkdir -p exps/exp1/figs
mkdir -p exps/exp1/models
mkdir -p exps/exp1/topics

time python python/experiments.py\
    --model_pref exps/exp1/models/nips_1_\
    --fig_pref exps/exp1/figs/nips_1_\
    --topics_pref exps/exp1/topics/nips_1_\
    --clus --min_cluster_size 5\
    --min_coherence 2.0\
    --cutoff 3\
    -p 3 0.2\
    -p 3 0.18\
    -p 3 0.15\
    -p 3 0.13\
    -p 3 0.10\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/knowceans-ilda/nips/nips.vocab\
    data/knowceans-ilda/nips/nips.tf.ifs\
    data/knowceans-ilda/nips/nips.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs


time python python/experiments.py\
    --model_pref exps/exp1/models/nips_2_\
    --fig_pref exps/exp1/figs/nips_2_\
    --33333333333333333333333333333333333333    --clus --min_cluster_size 5\
    --min_coherence 2.0\
    --cutoff 3\
    -p 3 0.2\
    -p 4 0.2\
    -p 5 0.2\
    -p 6 0.2\
    --voca-topics data/knowceans-ilda/nips/nips.vocab\
    data/knowceans-ilda/nips/nips.tf.ifs\
    data/knowceans-ilda/nips/nips.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs


