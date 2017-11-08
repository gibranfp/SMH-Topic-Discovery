#!/bin/bash
#
# Script to create files with the top K topics from all SMH discovered topics.
#
# It receives directory for SMH experiments as argument
FILES=`find $1 -name "*_top10.topics"`
for F in $FILES
do
    dirpath=$(dirname $F)
    mkdir -p $dirpath/topK
    
    filename=$(basename $F)
    filename="${filename%.*}"
    for K in 200 400 600
    do
        echo "Getting top $K topics from $F to $1/topK/$filename.k$K.topics"
        head -n $K $F > $1/topK/$filename.k$K.topics
    done
done
