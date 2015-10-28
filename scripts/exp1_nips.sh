#!/bin/bash

mkdir exps/exp1
mkdir exps/exp1/figs
mkdir exps/exp1/models
mkdir exps/exp1/topics

time python python/experiments.py\
    --model_pref exps/exp1/models/nips_1_\
    --fig_pref exps/exp1/figs/nips_1_\
    --topics_pref exps/exp1/topics/nips_1_\
    --clus --min_cluster_size 5\
    --min_coherence 2.0\
    --cutoff 2\
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
    --topics_pref exps/exp1/topics/nips_2_\
    --clus --min_cluster_size 5\
    --min_coherence 2.0\
    --cutoff 2\
    -p 3 0.13\
    -p 4 0.13\
    -p 5 0.13\
    -p 6 0.13\
    -p 7 0.13\
    -p 8 0.13\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/knowceans-ilda/nips/nips.vocab\
    data/knowceans-ilda/nips/nips.tf.ifs\
    data/knowceans-ilda/nips/nips.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs


