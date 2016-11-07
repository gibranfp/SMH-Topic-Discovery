#!/bin/bash

# echo "Creating inverted file for the NIPS corpus"
# # inverted file with term frecuency
# smhcmd ifindex \
#     data/knowceans-ilda/nips/nips.corpus \
#     data/knowceans-ilda/nips/nips.tf.ifs

# # inverted file with logarithmic term frequency
# smhcmd ifindex -w 1 \
#     data/knowceans-ilda/nips/nips.corpus \
#     data/knowceans-ilda/nips/nips.logtf.ifs

# # binary inverted file
# smhcmd ifindex -w 2\
#     data/knowceans-ilda/nips/nips.corpus \
#     data/knowceans-ilda/nips/nips.bin.ifs

# # IDS weighting
# smhcmd weights -w ids \
#     data/knowceans-ilda/nips/nips.corpus \
#     data/knowceans-ilda/nips/nips.tf.ifs \
#     data/knowceans-ilda/nips/nips.ids.weights


# echo "Limiting vocabulary to wikien.vocab"
# python python/cutoffvoca.py \
#     --voca data/wikipedia/wikien.vocab\
#     data/knowceans-ilda/nips/nips.vocab\
#     data/knowceans-ilda/nips/nips.corpus\
#     data/knowceans-ilda/nips/nips_wikivocab.vocab\
#     data/knowceans-ilda/nips/nips_wikivocab.corpus

# # inverted file with term frecuency
# smhcmd ifindex \
#     data/knowceans-ilda/nips/nips_wikivocab.corpus \
#     data/knowceans-ilda/nips/nips_wikivocab.tf.ifs

# # inverted file with logarithmic term frequency
# smhcmd ifindex -w 1 \
#     data/knowceans-ilda/nips/nips_wikivocab.corpus \
#     data/knowceans-ilda/nips/nips_wikivocab.logtf.ifs

# # binary inverted file
# smhcmd ifindex -w 2\
#     data/knowceans-ilda/nips/nips_wikivocab.corpus \
#     data/knowceans-ilda/nips/nips_wikivocab.bin.ifs

# # IDS weighting
# smhcmd weights -w ids \
#     data/knowceans-ilda/nips/nips_wikivocab.corpus \
#     data/knowceans-ilda/nips/nips_wikivocab.tf.ifs \
#     data/knowceans-ilda/nips/nips_wikivocab.ids.weights

# nips_vocab_sizes=(2000 4000 6000 8000 10000 12000)
# for size in ${nips_vocab_sizes[@]}; do
#     echo "NIPS corpus with vocabulary reduced to $size"
#     python python/cutoffvoca.py --max $size \
#            --voca data/wikipedia/wikien.vocab\
#            data/knowceans-ilda/nips/nips.vocab\
#            data/knowceans-ilda/nips/nips.corpus\
#            data/knowceans-ilda/nips/nips$size.vocab\
#            data/knowceans-ilda/nips/nips$size.corpus

#     # inverted file with term frecuency
#     smhcmd ifindex \
#            data/knowceans-ilda/nips/nips$size.corpus \
#            data/knowceans-ilda/nips/nips$size.tf.ifs

#     # inverted file with logarithmic term frequency
#     smhcmd ifindex -w 1 \
#            data/knowceans-ilda/nips/nips$size.corpus \
#            data/knowceans-ilda/nips/nips$size.logtf.ifs

#     # binary inverted file
#     smhcmd ifindex -w 2\
#            data/knowceans-ilda/nips/nips$size.corpus \
#            data/knowceans-ilda/nips/nips$size.bin.ifs

#     # IDS weighting
#     smhcmd weights -w ids \
#            data/knowceans-ilda/nips/nips$size.corpus \
#            data/knowceans-ilda/nips/nips$size.tf.ifs \
#            data/knowceans-ilda/nips/nips$size.ids.weights
# done

# echo "Creating inverted file for the 20 newsgroups corpus"
# # inverted file with term frecuency
# smhcmd ifindex \
#     data/20newsgroups/20newsgroups.corpus \
#     data/20newsgroups/20newsgroups.tf.ifs

# # inverted file with logarithmic term frequency
# smhcmd ifindex -w 1 \
#     data/20newsgroups/20newsgroups.corpus \
#     data/20newsgroups/20newsgroups.logtf.ifs

# # binary inverted file
# smhcmd ifindex -w 2\
#     data/20newsgroups/20newsgroups.corpus \
#     data/20newsgroups/20newsgroups.bin.ifs

# # IDS weighting
# smhcmd weights -w ids \
#     data/20newsgroups/20newsgroups.corpus \
#     data/20newsgroups/20newsgroups.tf.ifs \
#     data/20newsgroups/20newsgroups.ids.weights


# echo "Limiting vocabulary to wikien.vocab"
# python python/cutoffvoca.py \
#     --voca data/wikipedia/wikien.vocab\
#     data/20newsgroups/20newsgroups.vocab\
#     data/20newsgroups/20newsgroups.corpus\
#     data/20newsgroups/20newsgroups_wikivocab.vocab\
#     data/20newsgroups/20newsgroups_wikivocab.corpus

# # inverted file with term frecuency
# smhcmd ifindex \
#     data/20newsgroups/20newsgroups_wikivocab.corpus \
#     data/20newsgroups/20newsgroups_wikivocab.tf.ifs

# # inverted file with logarithmic term frequency
# smhcmd ifindex -w 1 \
#     data/20newsgroups/20newsgroups_wikivocab.corpus \
#     data/20newsgroups/20newsgroups_wikivocab.logtf.ifs

# # binary inverted file
# smhcmd ifindex -w 2\
#     data/20newsgroups/20newsgroups_wikivocab.corpus \
#     data/20newsgroups/20newsgroups_wikivocab.bin.ifs

# # IDS weighting
# smhcmd weights -w ids \
#     data/20newsgroups/20newsgroups_wikivocab.corpus \
#     data/20newsgroups/20newsgroups_wikivocab.tf.ifs \
#     data/20newsgroups/20newsgroups_wikivocab.ids.weights

# twenty_newsgroups_vocab_sizes=(2000 4000 6000 8000 10000 12000 14000 16000 18000)
# for size in ${twenty_newsgroups_vocab_sizes[@]}; do
#     echo "20 newsgroups corpus with vocabulary reduced to $size"
#     python python/cutoffvoca.py --max $size \
#            --voca data/wikipedia/wikien.vocab\
#            data/20newsgroups/20newsgroups.vocab\
#            data/20newsgroups/20newsgroups.corpus\
#            data/20newsgroups/20newsgroups$size.vocab\
#            data/20newsgroups/20newsgroups$size.corpus

#     # inverted file with term frecuency
#     smhcmd ifindex \
#            data/20newsgroups/20newsgroups$size.corpus \
#            data/20newsgroups/20newsgroups$size.tf.ifs

#     # inverted file with logarithmic term frequency
#     smhcmd ifindex -w 1 \
#            data/20newsgroups/20newsgroups$size.corpus \
#            data/20newsgroups/20newsgroups$size.logtf.ifs

#     # binary inverted file
#     smhcmd ifindex -w 2\
#            data/20newsgroups/20newsgroups$size.corpus \
#            data/20newsgroups/20newsgroups$size.bin.ifs

#     # IDS weighting
#     smhcmd weights -w ids \
#            data/20newsgroups/20newsgroups$size.corpus \
#            data/20newsgroups/20newsgroups$size.tf.ifs \
#            data/20newsgroups/20newsgroups$size.ids.weights
# done

echo "Creating inverted file for the Reuters corpus"
# inverted file with term frecuency
smhcmd ifindex \
    data/reuters/reuters.train.corpus \
    data/reuters/reuters.train.tf.ifs

# inverted file with logarithmic term frequency
smhcmd ifindex -w 1 \
    data/reuters/reuters.train.corpus \
    data/reuters/reuters.train.logtf.ifs

# binary inverted file
smhcmd ifindex -w 2\
    data/reuters/reuters.train.corpus \
    data/reuters/reuters.train.bin.ifs

# IDS weighting
smhcmd weights -w ids \
    data/reuters/reuters.train.corpus \
    data/reuters/reuters.train.tf.ifs \
    data/reuters/reuters.train.ids.weights


echo "Limiting vocabulary to wikien.vocab"
python python/cutoffvoca.py \
    --voca data/wikipedia/wikien.vocab\
    data/reuters/reuters.train.vocab\
    data/reuters/reuters.train.corpus\
    data/reuters/reuters_wikivocab.vocab\
    data/reuters/reuters_wikivocab.corpus

# inverted file with term frecuency
smhcmd ifindex \
    data/reuters/reuters_wikivocab.corpus \
    data/reuters/reuters_wikivocab.tf.ifs

# inverted file with logarithmic term frequency
smhcmd ifindex -w 1 \
    data/reuters/reuters_wikivocab.corpus \
    data/reuters/reuters_wikivocab.logtf.ifs

# binary inverted file
smhcmd ifindex -w 2\
    data/reuters/reuters_wikivocab.corpus \
    data/reuters/reuters_wikivocab.bin.ifs

# IDS weighting
smhcmd weights -w ids \
    data/reuters/reuters_wikivocab.corpus \
    data/reuters/reuters_wikivocab.tf.ifs \
    data/reuters/reuters_wikivocab.ids.weights

twenty_newsgroups_vocab_sizes=(10000 20000 30000 40000 50000 60000 70000 80000 90000 100000)
for size in ${twenty_newsgroups_vocab_sizes[@]}; do
    echo "20 newsgroups corpus with vocabulary reduced to $size"
    python python/cutoffvoca.py --max $size \
           --voca data/wikipedia/wikien.vocab\
           data/reuters/reuters.train.vocab\
           data/reuters/reuters.train.corpus\
           data/reuters/reuters$size.train.vocab\
           data/reuters/reuters$size.train.corpus

    # inverted file with term frecuency
    smhcmd ifindex \
           data/reuters/reuters$size.train.corpus \
           data/reuters/reuters$size.train.tf.ifs

    # inverted file with logarithmic term frequency
    smhcmd ifindex -w 1 \
           data/reuters/reuters$size.train.corpus \
           data/reuters/reuters$size.train.logtf.ifs

    # binary inverted file
    smhcmd ifindex -w 2\
           data/reuters/reuters$size.train.corpus \
           data/reuters/reuters$size.train.bin.ifs

    # IDS weighting
    smhcmd weights -w ids \
           data/reuters/reuters$size.train.corpus \
           data/reuters/reuters$size.train.tf.ifs \
           data/reuters/reuters$size.train.ids.weights
done


# echo "Woking with wiki"
# smhcmd ifindex -w 2\
#     data/wikipedia/wikien.train.corpus\
#     data/wikipedia/wikien.train.bin.ifs

# smhcmd ifindex\
#     data/wikipedia/wikien.train.corpus\
#     data/wikipedia/wikien.train.tf.ifs

# smhcmd weights\
#     data/wikipedia/wikien.train.corpus\
#     data/wikipedia/wikien.train.tf.ifs\
#     data/wikipedia/wikien.train.weights


# echo "Woking with wiki (100000)"
# python python/cutoffvoca.py --max 100000\
#     data/wikipedia/wikien.vocab\
#     data/wikipedia/wikien.train.corpus\
#     data/wikipedia/wikien100k.vocab\
#     data/wikipedia/wikien100k.train.corpus 

# smhcmd ifindex -w 2\
#     data/wikipedia/wikien100k.train.corpus\
#     data/wikipedia/wikien100k.train.bin.ifs

# smhcmd ifindex\
#     data/wikipedia/wikien100k.train.corpus\
#     data/wikipedia/wikien100k.train.tf.ifs

# smhcmd weights\
#     data/wikipedia/wikien100k.train.corpus\
#     data/wikipedia/wikien100k.train.tf.ifs\
#     data/wikipedia/wikien100k.train.weights


# echo "Woking with wiki"
# smhcmd ifindex -w 2\
#     data/wikipedia/wikies.train.corpus\
#     data/wikipedia/wikies.train.bin.ifs

# smhcmd ifindex\
#     data/wikipedia/wikies.train.corpus\
#     data/wikipedia/wikies.train.tf.ifs

# smhcmd weights\
#     data/wikipedia/wikies.train.corpus\
#     data/wikipedia/wikies.train.tf.ifs\
#     data/wikipedia/wikies.train.weights


# echo "Woking with wiki (100000)"
# python python/cutoffvoca.py --max 100000\
#     data/wikipedia/wikies.vocab\
#     data/wikipedia/wikies.train.corpus\
#     data/wikipedia/wikies100k.vocab\
#     data/wikipedia/wikies100k.train.corpus 

# smhcmd ifindex -w 2\
#     data/wikipedia/wikies100k.train.corpus\
#     data/wikipedia/wikies100k.train.bin.ifs

# smhcmd ifindex\
#     data/wikipedia/wikies100k.train.corpus\
#     data/wikipedia/wikies100k.train.tf.ifs

# smhcmd weights\
#     data/wikipedia/wikies100k.train.corpus\
#     data/wikipedia/wikies100k.train.tf.ifs\
#     data/wikipedia/wikies100k.train.weights


