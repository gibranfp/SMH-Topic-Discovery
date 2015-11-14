#!/bin/bash

mkdir exps/exp3
mkdir exps/exp3/figs
mkdir exps/exp3/models
mkdir exps/exp3/topics

time python python/experiments.py\
    --model_pref exps/exp3/models/nips1k_\
    --fig_pref exps/exp3/figs/nips1k_\
    --topics_pref exps/exp3/topics/nips1k_\
    --clus --min_cluster_size 5\
    --min_coherence 2.0\
    --cutoff 3\
    -p 3 0.2\
    -p 3 0.18\
    -p 3 0.15\
    -p 3 0.13\
    -p 3 0.10\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/knowceans-ilda/nips/nips1k.vocab\
    data/knowceans-ilda/nips/nips1k.bin.ifs\
    data/knowceans-ilda/nips/nips1k.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs

time python python/experiments.py\
    --model_pref exps/exp3/models/nips_\
    --fig_pref exps/exp3/figs/nips_\
    --topics_pref exps/exp3/topics/nips_\
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
    data/knowceans-ilda/nips/nips.bin.ifs\
    data/knowceans-ilda/nips/nips.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs


