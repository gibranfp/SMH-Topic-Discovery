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


def line2words(line):
    return [w for w in punct.findall(line.lower()) 
                if len(w)>0]
 

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
    p.add_argument("--odir",default=None,
            action="store", dest="odir",
            help="Output dir for documents [None]")
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
    for line in open(opts.WIKI):
        if re_header.match(line):
            if opts.max and len(idx)==opts.max:
                break
            corpus.update(doc)
            doc= Counter()
            idx.append(line[2:-2])
            doc.update(line2words(line[2:-2]))
        else:
            doc.update(line2words(line))
    corpus.update(doc)
    
    verbose("Total number of documents",len(idx)) 
    verbose("Vocabulary size",len(corpus)) 
    verbose("Total number of words",sum(corpus.values())) 

    # Creating splits
    if len(opts.splits)>0:
        if not sum([float(y) for x,y in opts.splits ]) == 100.0:
            p.error("Split options defined but it does not adds to 100%")
        random.shuffle(idx)
        splits={}
        dist=[]
        splits=[]
        ini=0
        for x,y in opts.splits:
            y=int(y)
            splits.append(("."+x,idx[ini:ini+int(y*0.01*len(idx))]))
            ini+=int(y*0.01*len(idx))
    else:
        splits=[("",idx)]

    print(splits)
    sys.exit()
    cwords={}
    cdocs={}

    voca={}
    # Consolidating the results
    for name in splitnames:
        cwords[name]=Counter([])
        cdocs[name]=Counter([])
        for cws_,cds_ in mapres:
            try:
                cwords[name].update(cws_[name])
                cdocs[name].update(cds_[name])
            except KeyError:
                pass

        voca_=[(y,x) for (x,y) in enumerate([w for w,c in cwords[name].most_common() if
          c>opts.cutoff])]
        voca[name]=dict(voca_)

        # Saving voca
        if opts.odir:
            vocafile=open("{0}/{1}{2}.voca".format(opts.odir,opts.corpus,name),"w")
        else:
            vocafile=open("{0}{1}.voca".format(opts.corpus,name),"w")


        # Printing voca files
        for word,id in voca_:
            print >> vocafile, "{0} = {1} = {2} {3}".format(word,id,cwords[name][word],cdocs[name][word])
        
    if opts.odir:
        pathcorpus="{0}/{1}".format(opts.odir,opts.corpus)
    else:
        pathcorpus="{0}".format(opts.corpus)

        mapres=imap(docszip,[(n,x,voca[mainvoca],pathcorpus,sws,splits,splitnames) for n,x in enumerate(listing)])

    
    docs,zips=zip(*mapres)
    docs_=sum(docs)
    zips_=sum(zips)

    for name in splitnames:
        ucorpusfile="{0}{1}.corpus".format(pathcorpus,name)
        with open(ucorpusfile, 'w') as outfile:
            for n,x in enumerate(listing):
                corpusfile="{0}{1}.corpus.{2}".format(pathcorpus,name,n)
                with open(corpusfile) as infile:
                    for line in infile:
                        outfile.write(line)
                os.remove(corpusfile)


        uidxfile="{0}{1}.idx".format(pathcorpus,name)
        with open(uidxfile, 'w') as outfile:
            for n,x in enumerate(listing):
                idxfile="{0}{1}.idx.{2}".format(pathcorpus,name,n)
                with open(idxfile) as infile:
                    for line in infile:
                        outfile.write(line)
                os.remove(idxfile)

    
    vocafile.close() 
        

        


       
        

