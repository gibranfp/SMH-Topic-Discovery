#!/bin/bash
#
# Script to download and preprocess the oxford buildings dataset
#
ROOTPATH=`pwd`
THIRDPARTYPATH=$ROOTPATH/3rdParty
DATAPATH=$ROOTPATH/data
mkdir -p $DATAPATH
NIPS=false
REUTERS=false
TWENTYNG=false
WIKIPEDIA=false
WIKI2TEXT=false
while getopts ":abcnrtw" opt; do
    case $opt in
        a)
            NIPS=true
            REUTERS=true
            TWENTYNG=true
            WIKIPEDIA=true
            WIKI2TEXT=true
            ;;
        b)
            WIKI2TEXT=true
            ;;
        n)
            NIPS=true
        ;;
        r)
            REUTERS=true
        ;;
        t)
            TWENTYNG=true
        ;;
        w)
            WIKIPEDIA=true
        ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;
    esac
done

if $NIPS; then
    echo "Preparing NIPS corpus"
    mkdir -p $DATAPATH
    wget -qO- -O $DATAPATH/tmp.zip http://arbylon.net/projects/nips/nips-20110223.zip && unzip $DATAPATH/tmp.zip -d $DATAPATH/ && rm $DATAPATH/tmp.zip
fi

if $REUTERS; then
    echo "Preparing Reuters"
    mkdir -p $DATAPATH/reuters
    echo -n "Enter path of Reuters dataset English Vol 1: "
    read REUTERSV1PATH
    echo -n "Enter path of Reuters dataset English Vol 2: "
    read REUTERSV2PATH
    python $ROOTPATH/python/reuters/docs2tfdocs.py --split train 80 --split test 20 --stop-words data/english.stop -p 6 -v --odir $DATAPATH/reuters ${REUTERSV1PATH} ${REUTERSV2PATH}
fi

if $TWENTYNG; then
    echo "Preparing 20 newsgroups corpus"
    mkdir -p $DATAPATH/20newsgroups
    python python/20newsgroups/20ng2corpus.py data/20newsgroups

fi

if $WIKI2TEXT; then
    if ! command -v nim >/dev/null 2>&1; then 
       mkdir -p $THIRDPARTYPATH

       echo "Installing Nim"
       git clone git://github.com/nim-lang/Nim.git $THIRDPARTYPATH/Nim
       cd $THIRDPARTYPATH/Nim
       git clone --depth 1 git://github.com/nim-lang/csources
       cd csources && sh build.sh
       cd ..
       bin/nim c koch
       ./koch boot -d:release
       export PATH=$PATH:$THIRDPARTYPATH/Nim/bin
       echo "Done installing Nim"
   fi

    echo "Installing wiki2text"
    git clone https://github.com/rspeer/wiki2text.git $THIRDPARTYPATH/wiki2text
    cd $THIRDPARTYPATH/wiki2text
    make
fi

if $WIKIPEDIA; then
    echo "Preparing Wikipedia"    
    mkdir -p $DATAPATH/wikipedia
    wget -qO- -O $DATAPATH//wikipedia/enwiki-20150702-pages-articles.xml.bz2 https://dumps.wikimedia.org/enwiki/20150702/enwiki-20150702-pages-articles.xml.bz2
    bunzip2 -c $DATAPATH/wikipedia/enwiki-20150702-pages-articles.xml.bz2 | ./$THIRDPARTYPATH/wiki2text > $DATAPATH/wikipedia/enwiki.txt
    python $ROOTPATH/python/wikipedia/wiki2corpus.py --WIKI $DATAPATH/wikipedia/enwiki.txt --split 80 20 --odir $DATAPATH/wikipedia/ --stop_words $ROOTPATH/data/stopwords_english.txt --cutoff 10 --corpus wiki
fi
