#!/bin/bash

mkdir -p exps/exp5
mkdir -p exps/exp5/figs
mkdir -p exps/exp5/models
mkdir -p exps/exp5/topics

time python python/experiments.py\
    --model_pref exps/exp5/models/nips1k_kmeans\
    --fig_pref exps/exp5/figs/nips1k_kmeans\
    --topics_pref exps/exp5/topics/nips1k_kmeans\
    --clus --min_cluster_size 5\
    --clus_method kmeans --nclus 276\
    --min_coherence 2.0\
    --cutoff 3\
    -p 3 0.13\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/knowceans-ilda/nips/nips1k.vocab\
    data/knowceans-ilda/nips/nips1k.tf.ifs\
    data/knowceans-ilda/nips/nips1k.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs


time python python/experiments.py\
    --model_pref exps/exp5/models/nips1k_minibatch\
    --fig_pref exps/exp5/figs/nips1k_minibatch\
    --topics_pref exps/exp5/topics/nips1k_minibatch\
    --clus --min_cluster_size 5\
    --clus_method minibatch --nclus 276\
    --min_coherence 2.0\
    --cutoff 3\
    -p 3 0.13\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/knowceans-ilda/nips/nips1k.vocab\
    data/knowceans-ilda/nips/nips1k.tf.ifs\
    data/knowceans-ilda/nips/nips1k.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs

time python python/experiments.py\
    --model_pref exps/exp5/models/nips1k_spectral\
    --fig_pref exps/exp5/figs/nips1k_spectral\
    --topics_pref exps/exp5/topics/nips1k_spectral\
    --clus --min_cluster_size 5\
    --clus_method spectral --nclus 276\
    --min_coherence 2.0\
    --cutoff 3\
    -p 3 0.13\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/knowceans-ilda/nips/nips1k.vocab\
    data/knowceans-ilda/nips/nips1k.tf.ifs\
    data/knowceans-ilda/nips/nips1k.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs
