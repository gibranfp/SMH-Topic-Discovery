#!/bin/bash

mkdir exps/exp4
mkdir exps/exp4/figs
mkdir exps/exp4/models
mkdir exps/exp4/topics

time python python/experiments.py\
    --model_pref exps/exp4/models/nips1k_expand\
    --fig_pref exps/exp4/figs/nips1k_expand\
    --topics_pref exps/exp4/topics/nips1k_expand\
    --clus --min_cluster_size 5\
    --min_coherence 1.0\
    --cutoff 2\
    -p 3 0.2\
    -p 3 0.18\
    -p 3 0.15\
    -p 3 0.13\
    -p 3 0.10\
    --expand data/knowceans-ilda/nips/nips1k.tf.ifs\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/knowceans-ilda/nips/nips1k.vocab\
    data/knowceans-ilda/nips/nips1k.tf.ifs\
    data/knowceans-ilda/nips/nips1k.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs

time python python/experiments.py\
    --model_pref exps/exp4/models/nips1k_expand_weights\
    --fig_pref exps/exp4/figs/nips1k_expand_weights\
    --topics_pref exps/exp4/topics/nips1k_expand_weights\
    --clus --min_cluster_size 5\
    --min_coherence 1.0\
    --cutoff 2\
    -p 3 0.2\
    -p 3 0.18\
    -p 3 0.15\
    -p 3 0.13\
    -p 3 0.10\
    --expand data/knowceans-ilda/nips/nips1k.tf.ifs\
    --weights data/knowceans-ilda/nips/nips1k.weights\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/knowceans-ilda/nips/nips1k.vocab\
    data/knowceans-ilda/nips/nips1k.tf.ifs\
    data/knowceans-ilda/nips/nips1k.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs

time python python/experiments.py\
    --model_pref exps/exp4/models/nips_expand\
    --fig_pref exps/exp4/figs/nips_expand\
    --topics_pref exps/exp4/topics/nips_expand\
    --clus --min_cluster_size 5\
    --min_coherence 1.0\
    --cutoff 2\
    -p 3 0.2\
    -p 3 0.18\
    -p 3 0.15\
    -p 3 0.13\
    -p 3 0.10\
    --expand data/knowceans-ilda/nips/nips.tf.ifs\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/knowceans-ilda/nips/nips.vocab\
    data/knowceans-ilda/nips/nips.tf.ifs\
    data/knowceans-ilda/nips/nips.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs

time python python/experiments.py\
    --model_pref exps/exp4/models/nips_expand_weights\
    --fig_pref exps/exp4/figs/nips_expand_weights\
    --topics_pref exps/exp4/topics/nips_expand_weights\
    --clus --min_cluster_size 5\
    --min_coherence 1.0\
    --cutoff 2\
    -p 3 0.2\
    -p 3 0.18\
    -p 3 0.15\
    -p 3 0.13\
    -p 3 0.10\
    --expand data/knowceans-ilda/nips/nips.tf.ifs\
    --weights data/knowceans-ilda/nips/nips.weights\
    --voca-corpus data/wikipedia/wiki.vocab\
    --voca-topics data/knowceans-ilda/nips/nips.vocab\
    data/knowceans-ilda/nips/nips.tf.ifs\
    data/knowceans-ilda/nips/nips.tf.ifs\
    data/wikipedia/wiki.test.tf.ifs
