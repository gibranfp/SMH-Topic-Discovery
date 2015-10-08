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

def coherence(topics, corpus,ntop=10,version="pmi"):
    results=[]
    for itopic,topic in enumerate(topics.ldb):
        coherence=0.0
        ntop=min(ntop,topic.size)
        for i in range(ntop):
            item_i=topic[i].item
            docs_i=corpus.ldb[item_i]
            for j in range(i+1,ntop):
                item_j=topic[j].item
                docs_j=corpus.ldb[item_j]
                if version=='original':
                    Dij=smh.sa.list_intersection_size(docs_i,docs_j)
                    coherence+=math.log((Dij*0.0001)/float(docs_j.size),10)
                elif version=="pmi":
                    docs_ij=smh.sa.list_intersection(docs_i,docs_j)
                    p_i=smh.sa.list_sum_freq(docs_i)
                    p_j=smh.sa.list_sum_freq(docs_j)
                    p_ij=smh.sa.list_sum_freq(docs_ij)
                    coherence+=math.log(float(p_ij)/float(p_i*p_j),10)
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
    p.add_argument("ifs",
            action="store",
            help="Corpus inverted file structure")
    p.add_argument("--rank",default=False,
            action="store_true", dest="rank",
            help="Rank the topics")
    
    opts = p.parse_args()

    print "Loading ifs file:",opts.ifs
    ifs=smh.smh_load(opts.ifs)

    print "Loading topics file:",opts.topics
    topics=smh.smh_load(opts.topics)

    res=coherence(topics,ifs)
    print res



                       

            



    



