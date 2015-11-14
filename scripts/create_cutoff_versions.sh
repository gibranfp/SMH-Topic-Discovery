#!/bin/bash

echo "Working with nips"
smhcmd ifindex -w 2\
    data/knowceans-ilda/nips/nips.corpus\
    data/knowceans-ilda/nips/nips.bin.ifs

smhcmd ifindex\
    data/knowceans-ilda/nips/nips.corpus\
    data/knowceans-ilda/nips/nips.tf.ifs

smhcmd weights\
    data/knowceans-ilda/nips/nips.corpus\
    data/knowceans-ilda/nips/nips.tf.ifs\
    data/knowceans-ilda/nips/nips.tf.weights


echo "Working with nips 1k"
python python/cutoffvoca.py --max 1000\
    --voca data/wikipedia/wiki.vocab\
    data/knowceans-ilda/nips/nips.vocab\
    data/knowceans-ilda/nips/nips.corpus\
    data/knowceans-ilda/nips/nips1k.vocab\
    data/knowceans-ilda/nips/nips1k.corpus

smhcmd ifindex -w 2\
    data/knowceans-ilda/nips/nips1k.corpus\
    data/knowceans-ilda/nips/nips1k.bin.ifs

smhcmd ifindex\
    data/knowceans-ilda/nips/nips1k.corpus\
    data/knowceans-ilda/nips/nips1k.tf.ifs

smhcmd weights\
    data/knowceans-ilda/nips/nips1k.corpus\
    data/knowceans-ilda/nips/nips1k.tf.ifs\
    data/knowceans-ilda/nips/nips1k.tf.weights


echo "Woking with 20ng"
smhcmd ifindex -w 2\
    data/20newsgroups/20ng.train.corpus\
    data/20newsgroups/20ng.train.bin.ifs

smhcmd ifindex\
    data/20newsgroups/20ng.train.corpus\
    data/20newsgroups/20ng.train.tf.ifs

smhcmd weights\
    data/20newsgroups/20ng.train.corpus\
    data/20newsgroups/20ng.train.tf.ifs\
    data/20newsgroups/20ng.train.wdights

echo "Woking with 20ng (5000)"
python python/cutoffvoca.py --max 5000\
    --voca  data/wikipedia/wiki.vocab\
    data/20newsgroups/20ng.train.voca\
    data/20newsgroups/20ng.train.corpus\
    data/20newsgroups/20ng5k.train.voca\
    data/20newsgroups/20ng5k.train.corpus

smhcmd ifindex -w 2\
    data/20newsgroups/20ng5k.train.corpus\
    data/20newsgroups/20ng5k.train.bin.ifs

smhcmd ifindex\
    data/20newsgroups/20ng5k.train.corpus\
    data/20newsgroups/20ng5k.train.tf.ifs

smhcmd weights\
    data/20newsgroups/20ng5k.train.corpus\
    data/20newsgroups/20ng5k.train.tf.ifs\
    data/20newsgroups/20ng5k.train.weights

echo "Woking with 20ng (10000)"
python python/cutoffvoca.py --max 10000\
    --voca  data/wikipedia/wiki.vocab\
    data/20newsgroups/20ng.train.voca\
    data/20newsgroups/20ng.train.corpus\
    data/20newsgroups/20ng10k.train.voca\
    data/20newsgroups/20ng10k.train.corpus

smhcmd ifindex -w 2\
    data/20newsgroups/20ng10k.train.corpus\
    data/20newsgroups/20ng10k.train.bin.ifs

smhcmd ifindex\
    data/20newsgroups/20ng10k.train.corpus\
    data/20newsgroups/20ng10k.train.tf.ifs

smhcmd weights\
    data/20newsgroups/20ng10k.train.corpus\
    data/20newsgroups/20ng10k.train.tf.ifs\
    data/20newsgroups/20ng10k.train.weights


echo "Woking with reuters"
smhcmd ifindex -w 2\
    data/reuters/reuters.train.corpus\
    data/reuters/reuters.train.bin.ifs

smhcmd ifindex\
    data/reuters/reuters.train.corpus\
    data/reuters/reuters.train.tf.ifs

smhcmd weights\
    data/reuters/reuters.train.corpus\
    data/reuters/reuters.train.tf.ifs\
    data/reuters/reuters.train.weights


echo "Woking with reuters (30000)"
python python/cutoffvoca.py --max 30000\
    --voca  data/wikipedia/wiki.vocab\
    data/reuters/reuters.train.voca\
    data/reuters/reuters.train.corpus\
    data/reuters/reuters.train30k.voca\
    data/reuters/reuters.train30k.corpus

smhcmd ifindex -w 2\
    data/reuters/reuters.train30k.corpus\
    data/reuters/reuters.train30k.bin.ifs

smhcmd ifindex\
    data/reuters/reuters.train30k.corpus\
    data/reuters/reuters.train30k.tf.ifs

smhcmd weights\
    data/reuters/reuters.train30k.corpus\
    data/reuters/reuters.train30k.tf.ifs\
    data/reuters/reuters.train30k.weights



echo "Woking with wiki"
smhcmd ifindex -w 2\
    data/wikipedia/wiki.train.corpus\
    data/wikipedia/wiki.train.bin.ifs

smhcmd ifindex\
    data/wikipedia/wiki.train.corpus\
    data/wikipedia/wiki.train.tf.ifs

smhcmd weights\
    data/wikipedia/wiki.train.corpus\
    data/wikipedia/wiki.train.tf.ifs\
    data/wikipedia/wiki.train.weights


echo "Woking with wiki (100000)"
python python/cutoffvoca.py --max 100000\
    data/wikipedia/wiki.vocab\
    data/wikipedia/wiki.train.corpus\
    data/wikipedia/wiki100k.vocab\
    data/wikipedia/wiki100k.train.corpus 

smhcmd ifindex -w 2\
    data/wikipedia/wiki100k.train.corpus\
    data/wikipedia/wiki100k.train.bin.ifs

smhcmd ifindex\
    data/wikipedia/wiki100k.train.corpus\
    data/wikipedia/wiki100k.train.tf.ifs

smhcmd weights\
    data/wikipedia/wiki100k.train.corpus\
    data/wikipedia/wiki100k.train.tf.ifs\
    data/wikipedia/wiki100k.train.weights

