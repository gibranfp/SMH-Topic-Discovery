#!/bin/bash

mkdir fig/exp1
mkdir models/exp1
mkdir topics/exp1

time python python/experiments.py\
    --model_pref models/exp1/nips_\
    --fig_pref fig/exp1/nips_\
    --topics_pref topics/exp1/nips_\
    --clus --min_cluster_size 10 --cutoff 2\
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
    --model_pref models/exp1/20ng_\
    --fig_pref fig/exp1/20ng_\
    --topics_pref topics/exp1/20ng_\
    --clus --min_cluster_size 10 --cutoff 2\
    -p 3 0.2\
    -p 3 0.18\
    -p 3 0.15\
    -p 3 0.13\
    -p 3 0.10\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/20newsgroups/20ng.train.voca\
    data/20newsgroups/20ng.train.tf.ifs\
    data/20newsgroups/20ng.train.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs

