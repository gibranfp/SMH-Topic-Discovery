#!/bin/bash

mkdir -p exps/exp5
mkdir -p exps/exp5/figs
mkdir -p exps/exp5/models
mkdir -p exps/exp5/topics

time python python/experiments_clus.py\
    --model_pref exps/exp5/models/nips_clus\
    --fig_pref exps/exp5/figs/nips_clus\
    --topics_pref exps/exp5/topics/nips_clus\
    --clus --min_cluster_size 5\
    --nclus 99\
    --min_coherence 2.0\
    --cutoff 3\
    -l \
    -p 3 692\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/knowceans-ilda/nips/nips1k.vocab\
    data/knowceans-ilda/nips/nips1k.tf.ifs\
    data/knowceans-ilda/nips/nips1k.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs


#time python python/experiments.py\
#    --model_pref exps/exp5/models/nips_minibatch\
#    --fig_pref exps/exp5/figs/nips_minibatch\
#    --topics_pref exps/exp5/topics/nips_minibatch\
#    --clus --min_cluster_size 5\
#    --clus_method minibatch --nclus 276\
#    --min_coherence 2.0\
#    --cutoff 3\
#    -p 3 0.15\
#    --voca-corpus data/wikipedia/wiki.vocab\
#    --voca-topics data/knowceans-ilda/nips/nips.vocab\
#    data/knowceans-ilda/nips/nips.tf.ifs\
#    data/knowceans-ilda/nips/nips.tf.ifs\
#    data/wikipedia/wiki.test.tf.ifs
#
#time python python/experiments.py\
#    --model_pref exps/exp5/models/nips_spectral\
#    --fig_pref exps/exp5/figs/nips_spectral\
#    --topics_pref exps/exp5/topics/nips_spectral\
#    --clus --min_cluster_size 5\
#    --clus_method spectral --nclus 276\
#    --min_coherence 2.0\
#    --cutoff 3\
#    -p 3 0.15\
#    --voca-corpus data/wikipedia/wiki.vocab\
#    --voca-topics data/knowceans-ilda/nips/nips.vocab\
#    data/knowceans-ilda/nips/nips.tf.ifs\
#    data/knowceans-ilda/nips/nips.tf.ifs\
#    data/wikipedia/wiki.test.tf.ifs
#
