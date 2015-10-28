#!/bin/bash

mkdir fig/test
mkdir models/test
mkdir topics/test

time python python/experiments.py\
    --model_pref models/test/nips_\
    --fig_pref fig/test/nips_\
    --topics_pref topics/test/nips_\
    --clus --min_cluster_size 10\
    --min_coherence 1.0\
    --cutoff 2\
    -p 3 0.2\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/knowceans-ilda/nips/nips.vocab\
    data/knowceans-ilda/nips/nips.tf.ifs\
    data/knowceans-ilda/nips/nips.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs

