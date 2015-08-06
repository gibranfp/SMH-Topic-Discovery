#!/bin/bash
#
# Script to download and preprocess the oxford buildings dataset
#
REL_CMDPATH=`dirname $0`
ABS_CMDPATH=`pwd`

if [[ $REL_CMDPATH == "." ]]
then
    REL_CMDPATH=""
fi

ABS_CMDPATH=$ABS_CMDPATH/$REL_CMDPATH

DATAPATH=`dirname $ABS_CMDPATH`
DATAPATH=$DATAPATH/data

if [ ! -a $DATAPATH ]
then
    mkdir $DATAPATH
fi

curl -0Lk http://arbylon.net/projects/nips/nips-20110223.zip -o $DATAPATH/nips.zip && unzip $DATAPATH/nips.zip
unzip $DATAPATH/nips.zip -d $DATAPATH/
