#!/bin/bash
#
# Script to download and preprocess the Reuters and
# Wikipedia corpora
#
ROOTPATH=`pwd`
THIRDPARTYPATH=$ROOTPATH/3rdParty
DATAPATH=$ROOTPATH/data
mkdir -p $DATAPATH
WIKIDUMPEN="https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2"

NIPS=false
TWENTYNG=false
REUTERS=false
WIKIPEDIA=false
while getopts ":abrw" opt; do
    case $opt in
        a)
            NIPS=true
            TWENTYNG=true
            REUTERS=true
            WIKIPEDIA=true
            WIKI2TEXT=true
            ;;
        b)
            WIKI2TEXT=true
            ;;
        n)
            NIPS=true
            ;;
        t)
            TWENTYNG=true
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

if $NIPS; then
        echo "Downloading NIPS corpus"
        wget -qO- -O $DATAPATH/tmp.zip \
            http://arbylon.net/projects/nips/nips-20110223.zip
        unzip $DATAPATH/tmp.zip -d $DATAPATH/
        rm $DATAPATH/tmp.zip

        echo "Genereting inverted file from corpus"
        smhcmd ifindex $DATAPATH/knowceans-ilda/nips/nips.corpus $DATAPATH/knowceans-ilda/nips/nips.ifs
        
        echo "Done processing NIPS corpus"
fi

if $TWENTYNG; then
    mkdir -p $DATAPATH/20newsgroups

    echo "Generating 20 newsgroups reference text"
    python python/corpus/20ng2ref.py $DATAPATH/20newsgroups

    echo "Generating BOWs from 20 newsgroups reference text"
    python python/corpus/ref2corpus.py $DATAPATH/20newsgroups/20newsgroups.ref \
        $DATAPATH/stopwords_english.txt \
        $DATAPATH/20newsgroups/ \
        -c 40000
    
    echo "Genereting inverted file from corpus"
    smhcmd ifindex $DATAPATH/20newsgroups/20newsgroups40000.corpus $DATAPATH/20newsgroups/20newsgroups40000.ifs
    
    echo "Done processing 20 newsgroups corpus"
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

    echo "Using Wikipedia as reference for computing NPMI scores"
    mkdir -p $DATAPATH/ref
    cp $DATAPATH/wikipedia/enwiki.ref $DATAPATH/ref/
    
    echo "Done processing Wikipedia corpus"
fi
