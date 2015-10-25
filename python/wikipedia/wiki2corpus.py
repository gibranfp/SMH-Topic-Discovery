#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Transforms docs into itf documents
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2015/IIMAS/UNAM
# ----------------------------------------------------------------------
# wiki2corpus.py is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -------------------------------------------------------------------------

from __future__ import print_function

# System libraries
import argparse
import sys
import os
import os.path
import random
import re
random.seed()

from collections import Counter
punct=re.compile("[a-z']+")

def line2words(line,sws):
    return [w for w in punct.findall(line.lower()) 
                if len(w)>0 and not w in sws]
 

if __name__ == "__main__":
    # Command line options
    p = argparse.ArgumentParser("Creates a corpus for topic discovery")
    p.add_argument("WIKI",
            help="Wikipedia text dump")
    p.add_argument("--split",default=[],nargs=2,
            action="append", dest="splits",
            help="splits to produce and percentage [none]")
    p.add_argument("--voca",default=None,
            action="store", dest="voca",
            help="Name of main vocabulary bases on splits (otherwise first split)")
    p.add_argument("--corpus",default="wiki",
            action="store", dest="corpus",
            help="Name for corpus file [wiki]")
    p.add_argument("--odir",default='.',
            action="store", dest="odir",
            help="Output dir for documents [.]")
    p.add_argument("--stop-words",default=None,metavar="FILE",
            action="store", dest="stopwords",
            help="stopwords file [None]")
    p.add_argument("--random",default=False,
           action="store_true", dest="random",
           help="Use random seed [False]")
    p.add_argument("--cutoff",
        action="store", dest="cutoff", type=int,default=10,
        help="Cut off for frecuencies [10]")
    p.add_argument("--max",
        action="store", dest="max", type=int,default=None,
        help="Max number of documents to process [All]")
  
    p.add_argument("-v", "--verbose",
        action="store_true", dest="verbose", default=False,
        help="Verbose mode")
    opts = p.parse_args()

    if not opts.random:
        random.seed(9111978)

    # prepara función de verbose
    if opts.verbose:
        def verbose(*args):
            print(*args)
    else:   
        verbose = lambda *a: None 

    sws=[]
    # Load stopwords
    if opts.stopwords:
        for line in open(opts.stopwords):
            line=line.strip()
            if line.startswith("#"):
                continue
            sws+=[w.strip() for w in line.split(',')]
        sws=set(sws)

  
    # Extrayendo el vocabulario
    re_header = re.compile('^= ')
    corpus=Counter()
    doc=Counter()
    idx=[]
    verbose("Extracting articles")
    for line in open(opts.WIKI):
        if re_header.match(line):
            if opts.max and len(idx)==opts.max:
                break
            if not len(idx)%1000:
                print('.',end="")
            corpus.update(doc)
            doc= Counter()
            idx.append(line[2:-2].strip())
            doc.update(line2words(line[2:-2].strip(),[]))
        else:
            doc.update(line2words(line.strip(),sws))
    corpus.update(doc)
    
    verbose("Total number of documents",len(idx)) 
    verbose("Vocabulary size",len(corpus)) 
    verbose("Total number of words",sum(corpus.values())) 

    files=[]
    # Creating splits
    first_split=None
    verbose("Creating splits")
    if len(opts.splits)>0:
        if not sum([float(y) for x,y in opts.splits ]) == 100.0:
            p.error("Split options defined but it does not adds to 100%")
        random.shuffle(idx)
        splits=[]
        ini=0
        first_split=opts.splits[0][0]
        for x,y in opts.splits:
            y=int(y)
            files.append(open(os.path.join(opts.odir,opts.corpus+"."+x+".corpus"),'w'))
            splits.append(dict([ (title,(files[-1],x)) for title in idx[ini:ini+int(y*0.01*len(idx))]]))
            ini+=int(y*0.01*len(idx))
        splits.append(dict([ (title,(files[-1],x)) for title in idx[ini:]]))
    else:
        files.append(open(os.path.join(opts.odir,opts.corpus+".corpus"),'w'))
        first_split=""
        splits=[dict([(title,(files[-1],"")) for title in idx])]

    splits_={}
    for split in splits:
        splits_.update(split)
    splits=splits_


    # Extracting voca first split
    vocab=Counter()
    header=None
    ii=0
    if len(opts.splits)<=1:
        vocab=corpus
    else:
        for line in open(opts.WIKI):

            if re_header.match(line):
                if opts.max and ii==opts.max:
                    break

                if not ii%1000:
                    print('.',end="")
 
                header=line[2:-2].strip()
                if splits[header][1]==first_split:
                    vocab.update(doc)
                    doc.update(line2words(header,[]))
                doc= Counter()
                ii+=1
            else:
                if splits[header][1]==first_split:
                    doc.update(line2words(line.strip(),sws))
        if splits[header][1]==first_split:
            vocab.update(doc)

    verbose("Total number of words in vocab",sum(vocab.values()))
    vocab=[(w,n) for (w,n) in vocab.most_common() if n>opts.cutoff ]
    vocab_={}
    for (i,(w,n)) in enumerate(vocab):
        vocab_[w]=i



    ii=0
    header=None
    verbose("Creating corpus")
    for line in open(opts.WIKI):
        if re_header.match(line):
            if opts.max and ii==opts.max:
                break
            if not ii%1000:
                print('.',end="")
            if header:
                info=["{0}:{1}".format(vocab_[w],n) for w,n in doc.most_common() if vocab_.has_key(w)] 
                print(len(info)," ".join(info),file=splits[header][0])
            doc= Counter()
            ii+=1
            header=line[2:-2].strip()
            doc.update(line2words(header,[]))
        else:
            doc.update(line2words(line.strip(),sws))
    if header:
        info=["{0}:{1}".format(vocab_[w],n) for w,n in doc.most_common() if vocab_.has_key(w)] 
        print(len(info)," ".join(info),file=splits[header][0])

    for file in files:
        file.close()
    verbose("Creating vocabulary")
    vocabf=open(os.path.join(opts.odir,opts.corpus+".vocab"),"w")
    for i,(w,n) in enumerate(vocab):
        print("{0} = {1} = {2}".format(w,i,n),file=vocabf)
    vocabf.close()

