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


time python python/experiments.py\
    --model_pref exps/exp3/models/20ng5k_\
    --fig_pref exps/exp3/figs/20ng5k_\
    --topics_pref exps/exp3/topics/20ng5k_\
    --clus --min_cluster_size 5\
    --min_coherence 2.0\
    --cutoff 3\
    -p 3 0.2\
    -p 3 0.18\
    -p 3 0.15\
    -p 3 0.13\
    -p 3 0.10\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/20newsgroups/20ng5k.train.voca\
    data/20newsgroups/20ng5k.train.bin.ifs\
    data/20newsgroups/20ng5k.train.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs


time python python/experiments.py\
    --model_pref exps/exp3/models/20ng10k_\
    --fig_pref exps/exp3/figs/20ng10k_\
    --topics_pref exps/exp3/topics/20ng10k_\
    --clus --min_cluster_size 5\
    --min_coherence 2.0\
    --cutoff 3\
    -p 3 0.2\
    -p 3 0.18\
    -p 3 0.15\
    -p 3 0.13\
    -p 3 0.10\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/20newsgroups/20ng10k.train.voca\
    data/20newsgroups/20ng10k.train.bin.ifs\
    data/20newsgroups/20ng10k.train.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs

time python python/experiments.py\
    --model_pref exps/exp3/models/20ng_\
    --fig_pref exps/exp3/figs/20ng_\
    --topics_pref exps/exp3/topics/20ng_\
    --clus --min_cluster_size 5\
    --min_coherence 2.0\
    --cutoff 3\
    -p 3 0.2\
    -p 3 0.18\
    -p 3 0.15\
    -p 3 0.13\
    -p 3 0.10\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/20newsgroups/20ng.train.voca\
    data/20newsgroups/20ng.train.bin.ifs\
    data/20newsgroups/20ng.train.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs

time python python/experiments.py\
    --model_pref exps/exp3/models/reuters_\
    --fig_pref exps/exp3/figs/reuters_\
    --topics_pref exps/exp3/topics/reuters_\
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
    data/reuters/reuters30k.train.bin.ifs\
    data/reuters/reuters30k.train.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs







