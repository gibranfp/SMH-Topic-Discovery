#!/bin/bash
#
#
CORPUS_DIR=`dirname $1`
CORPUS_SIZE=`wc -l $1 | cut -f1 -d' '`
INC=`echo "$CORPUS_SIZE / 10" | bc`
SIZES=`seq $INC $INC $CORPUS_SIZE`

for S in $SIZES; do
    echo "Generating corpus of size $S: $CORPUS_DIR/reuters30k.train$S.corpus"
    head --lines=$S $1 > $CORPUS_DIR/reuters30k.train$S.corpus
    smhcmd ifindex $CORPUS_DIR/reuters30k.train$S.corpus $CORPUS_DIR/reuters30k.train$S.tf.ifs
    smhcmd ifindex -w 2 $CORPUS_DIR/reuters30k.train$S.corpus $CORPUS_DIR/reuters30k.train$S.bin.ifs
    smhcmd ifindex -w 4 $CORPUS_DIR/reuters30k.train$S.corpus $CORPUS_DIR/reuters30k.train$S.ids.ifs
    smhcmd ifindex -w 6 $CORPUS_DIR/reuters30k.train$S.corpus $CORPUS_DIR/reuters30k.train$S.tf.ids.ifs
    smhcmd weights -w ids $CORPUS_DIR/reuters30k.train$S.corpus $CORPUS_DIR/reuters30k.train$S.tf.ifs $CORPUS_DIR/reuters30k.train$S.weights
done
