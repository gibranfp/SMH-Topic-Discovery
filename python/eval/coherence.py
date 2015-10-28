#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Coherence for topic dicovery calculation.
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2015/IIMAS/UNAM
# ----------------------------------------------------------------------
#
# System libraries
import argparse
from collections import Counter
import sys
import os
import re
import math
from smh import smh
import utils

def coherence(topics, corpus,t2c=None,ntop=10,version="pmi"):
    results=[]
    for itopic,topic in enumerate(topics.ldb):
        coherence=0.0
        if topic.size == 0:
            continue
        ntop=min(ntop,topic.size)
        for i in range(ntop):
            item_i=topic[i].item
            if t2c:
                try:
                    docs_i=corpus.ldb[t2c[item_i]]
                except KeyError:
                    continue
            else:
                docs_i=corpus.ldb[item_i]
            for j in range(i+1,ntop):
                item_j=topic[j].item
                if t2c:
                    try:
                        docs_i=corpus.ldb[t2c[item_j]]
                    except KeyError:
                        continue
                docs_j=corpus.ldb[item_j]
                if version=='original':
                    Dij=smh.sa.list_intersection_size(docs_i,docs_j)
                    coherence+=math.log((Dij*0.0001)/float(docs_j.size),10)
                elif version=="pmi":
                    docs_ij=smh.sa.list_intersection(docs_i,docs_j)
                    p_i=smh.sa.list_sum_freq(docs_i)
                    p_j=smh.sa.list_sum_freq(docs_j)
                    p_ij=smh.sa.list_sum_freq(docs_ij)
                    if p_ij > 0:
                        coherence+=-1.0*math.log(float(p_ij)/float(p_i*p_j),10)
        if coherence>0:
            results.append((itopic,coherence/sum(range(ntop))))
    return results



version="%prog 0.1"

# MAIN
if __name__ == "__main__":
    # Command line options
    p = argparse.ArgumentParser("Coherence evaluation")
    p.add_argument("topics",
            action="store",
            help="Topics file")
    p.add_argument("corpus",
            action="store",
            help="Corpus inverted file structure")
    p.add_argument("--voca-topics",default=False,
            action="store", dest="vtopics",
            help="Vocabulary of topics")
    p.add_argument("--voca-corpus",default=False,
            action="store", dest="vcorpus",
            help="Vocabulary of corpus")
    
    opts = p.parse_args()
    if (opts.vcorpus and not opts.vtopics) or (not opts.vcorpus and opts.vtopics):
        print "Both have to be given the vocabulary of the corpus an topics"
        sys.exit(0)
    else:
        topic2corpus=utilss.t2c(opts.vtopics,opts.vcorpus)

    print "Loading ifs file:",opts.corpus
    corpus=smh.smh_load(opts.corpus)

    print "Loading topics file:",opts.topics
    topics=smh.smh_load(opts.topics)

    res=coherence(topics,corpus,topic2corpus)
    print res



                       

            



    



