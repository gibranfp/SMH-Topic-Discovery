#!/bin/bash

mkdir -p experiments_kbsystems/different_s/models
mkdir -p experiments_kbsystems/different_s/topics
mkdir -p experiments_kbsystems/different_s/figs

time python python/experiments.py \
    --model_pref experiments_kbsystems/different_s/models/nips_ \
    --fig_pref experiments_kbsystems/different_s/figs/nips_ \
    --topics_pref experiments_kbsystems/different_s/topics/nips_ \
    --clus --min_cluster_size 5 \
    --min_coherence 0.0 \
    --cutoff 3 \
    -p 3 0.20 \
    -p 3 0.18 \
    -p 3 0.16 \
    -p 3 0.14 \
    -p 3 0.12 \
    -p 3 0.10 \
    --voca-corpus data/wikipedia/wikien.vocab \
    --voca-topics data/knowceans-ilda/nips/nips_wikivoca.vocab \
    data/knowceans-ilda/nips/nips.tf.ifs \
    data/knowceans-ilda/nips/nips.tf.ifs \
    data/wikipedia/wiki.test.tf.ifs

mkdir -p experiments_kbsystems/different_r/models
mkdir -p experiments_kbsystems/different_r/topics
mkdir -p experiments_kbsystems/different_r/figs

time python python/experiments.py \
    --model_pref experiments_kbsystems/different_r/models/nips_ \
    --fig_pref experiments_kbsystems/different_r/figs/nips_ \
    --topics_pref experiments_kbsystems/different_r/topics/nips_ \
    --clus --min_cluster_size 5 \
    --min_coherence 2.0 \
    --cutoff 3 \
    -p 2 0.2 \
    -p 3 0.2 \
    -p 4 0.2 \
    -p 5 0.2 \
    -p 6 0.2 \
    --voca-corpus data/wikipedia/wiki.vocab \
    --voca-topics data/knowceans-ilda/nips/nips.vocab \
    data/knowceans-ilda/nips/nips.tf.ifs \
    data/knowceans-ilda/nips/nips.tf.ifs \
    data/wikipedia/wiki.test.tf.ifs
