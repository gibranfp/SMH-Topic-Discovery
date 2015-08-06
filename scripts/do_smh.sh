#!/bin/bash
#
# Script to perform Sampled Min-Hashing on a given dataset
#
REL_CMDPATH=`dirname $0`
ABS_CMDPATH=`pwd`

if [[ $REL_CMDPATH == "." ]]
then
    REL_CMDPATH=""
fi

ABS_CMDPATH=$ABS_CMDPATH/$REL_CMDPATH

DATAPATH=`dirname $ABS_CMDPATH`
DATAPATH=$DATAPATH/data/knowceans-ilda/nips

smhcmd ifindex $DATAPATH/nips.corpus $DATAPATH/ifindex.txt
smhcmd mine $DATAPATH/ifindex.txt $DATAPATH/mined.txt
smhcmd prune $DATAPATH/ifindex.txt $DATAPATH/mined.txt $DATAPATH/pruned.txt
smhcmd cluster $DATAPATH/pruned.txt $DATAPATH/topics.txt
