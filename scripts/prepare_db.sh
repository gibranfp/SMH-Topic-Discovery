#!/bin/bash
#
# Script to download and preprocess the Reuters and
# Wikipedia corpora
#
ROOTPATH=`pwd`
THIRDPARTYPATH=$ROOTPATH/3rdParty
DATAPATH=$ROOTPATH/data
mkdir -p $DATAPATH
WIKIDUMPEN="http://dumps.wikimedia.org/enwiki/20161101/enwiki-20161101-pages-articles.xml.bz2"

REUTERS=false
WIKIPEDIA=false
while getopts ":abrw" opt; do
    case $opt in
        a)
            REUTERS=true
            WIKIPEDIA=true
            WIKI2TEXT=true
            ;;
        b)
            WIKI2TEXT=true
            ;;
        r)
            REUTERS=true
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

if [ ! -f $DATAPATH/stopwords_english.txt ]; then
    echo "Downloading stopwords"
    wget -qO- -O $DATAPATH/stopwords_english.txt \
         https://raw.githubusercontent.com/pan-webis-de/authorid/master/data/stopwords_english.txt
fi

if $REUTERS; then
    echo "Preparing Reuters"
    mkdir -p $DATAPATH/reuters
    echo -n "Enter path of Reuters dataset: "
    read REUTERSPATH

    echo "Genereting reference text from Reuters directory $REUTERSPATH"
    python $ROOTPATH/python/corpus/reuters2ref.py \
	     $REUTERSPATH \
	     $DATAPATH/reuters/

    for VOCSIZE in 20000 40000 60000 80000 100000
    do
        echo "Genereting BOWs (vocabulary size = $VOCSIZE) from Reuters reference"
        python $ROOTPATH/python/corpus/ref2corpus.py \
	         $DATAPATH/reuters/reuters.ref \
	         $DATAPATH/stopwords_english.txt \
	         $DATAPATH/reuters/ \
	         -c $VOCSIZE

        echo "Genereting inverted file from corpus"
        smhcmd ifindex $DATAPATH/reuters/reuters$VOCSIZE.corpus $DATAPATH/reuters/reuters$VOCSIZE.ifs
        smhcmd weights -w ids $DATAPATH/reuters/reuters$VOCSIZE.corpus $DATAPATH/reuters/reuters$VOCSIZE.ifs $DATAPATH/reuters/reuters$VOCSIZE.weights
    done
    
    echo "Done processing Reuters corpus"
fi

if $WIKI2TEXT; then
    if ! command -v nim >/dev/null 2>&1; then 
       mkdir -p $THIRDPARTYPATH

       echo "Installing Nim"
       git clone git://github.com/nim-lang/Nim.git $THIRDPARTYPATH/Nim
       cd $THIRDPARTYPATH/Nim
       git clone --depth 1 git://github.com/nim-lang/csources
       cd csources
       sh build.sh
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

    if [ ! -f $DATAPATH/wikipedia/wikien.xml.bz2 ]; then
        echo "Downloading Wikipedia dump"
        wget -qO- -O $DATAPATH/wikipedia/wikien.xml.bz2 \
             $WIKIDUMPEN
    fi
    
    echo "Uncompressing and parsing Wikipedia dump"
    bunzip2 -c $DATAPATH/wikipedia/wikien.xml.bz2 \
        | $THIRDPARTYPATH/wiki2text/wiki2text > $DATAPATH/wikipedia/enwiki.txt

    echo "Genereting reference text from wikipedia"
    python $ROOTPATH/python/corpus/wiki2ref.py \
	   $DATAPATH/wikipedia/enwiki.txt \
	   $DATAPATH/wikipedia/

    echo "Genereting BOWs from wikipedia reference"
    python $ROOTPATH/python/corpus/ref2corpus.py \
	   $DATAPATH/wikipedia/enwiki.ref \
	   $DATAPATH/stopwords_english.txt \
	   $DATAPATH/wikipedia/ \
	   -c 1000000

    echo "Genereting inverted file from corpus"
    smhcmd ifindex $DATAPATH/wikipedia/enwiki.corpus $DATAPATH/wikipedia/enwiki.ifs
    smhcmd weights -w ids $DATAPATH/wikipedia/enwiki.corpus $DATAPATH/wikipedia/enwiki.ifs $DATAPATH/wikipedia/enwiki.weights
    echo "Done processing Wikipedia corpus"
fi
