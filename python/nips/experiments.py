#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Sampled MinHash demo with images
# ----------------------------------------------------------------------
# Gibran Fuentes-Pineda, Ivan V. Meza
# 2015/IIMAS, México
# ----------------------------------------------------------------------

import sys
sys.path.append('python')
import numpy as np
import pylab as pl
from smh import smh
import math
from eval.coherence import coherence, utils

def s2l(s,r):
    return int(math.log(0.5)/math.log(1-math.pow(s,r)))


# MAIN program
if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser("Mines")
    p.add_argument("-p","--params",default=[(3,120)],
                action="append", dest="params",type=float,nargs=2,
                help="(Size of the tuple, S*| number of tuples)")
    p.add_argument("-l","--number_tuples",default=False,
                action="store_true", dest="l",
                help="Turn on second value op pair as parameter l, otherwise s*")
    p.add_argument("--output_pref",default=None,type=str,
        action="store", dest='outputpref',help="Prefix of output files")
    p.add_argument("--cutoff",default=None,type=int,
        action="store", dest='cutoff',help="Cutoff of topics [Off]")
    p.add_argument("--clus",default=False,
        action="store_true", dest='clus',help="Cluster topics [Off]")
    p.add_argument("--thres",default=0.7,
            action="store", dest='thres',
            help="Threshold for clustering")
    p.add_argument("--voca-topics",default=False,
            action="store", dest="vtopics",
            help="Vocabulary of topics")
    p.add_argument("--voca-corpus",default=False,
            action="store", dest="vcorpus",
            help="Vocabulary of corpus")
    p.add_argument("ifs",default=None,
        action="store", help="Inverted file structure of documents")
    p.add_argument("corpus",default=None,
        action="store", help="Inverted file structure of documents with term frequencies")


    opts = p.parse_args()

    if len(opts.params)>1:
        opts.params.pop(0)

    topic2corpus=None
    if (opts.vcorpus and not opts.vtopics) or (not opts.vcorpus and opts.vtopics):
        print "Both have to be given the vocabulary of the corpus an topics"
        sys.exit(0)
    else:
        if opts.vcorpus:
            topic2corpus=utils.t2c(opts.vtopics,opts.vcorpus)

    print "Loading file ifs:",opts.ifs
    ifs=smh.smh_load(opts.ifs)

    print "Loading testing corpus:",opts.corpus
    corpus=smh.smh_load(opts.corpus)

    if not opts.l:
        params=[(int(r),s2l(s,r),s) for r,s in opts.params]
    else:
        params=[(int(r),int(l),0) for r,l in opts.params]
    sorted(params)

    cs=[]

    for r,l,s in params:
        if s>0:
            print "Experiment tuples (r)",r,", Number of tuples (l)",l,", S*",s
        else:
            print "Experiment tuples (r)",r,"Number of tuples (l)",l
        print "Mining topics..."
        m=ifs.mine(r,l)
        print "Size of original mined topics:",m.size()
        if opts.cutoff:
            m.cutoff(min=opts.cutoff)
            print "Size of cutted off mined topics:",m.size()
        if opts.clus:
            c=m.cluster_mhlink(3,255,thres=opts.thres)
            print "Size of clustered topics:",c.size()
            m=c

        # EVAL coherence
        co=coherence(m,corpus,topic2corpus)
        if opts.outputpref:
            print "Saving resulting model to",opts.outputpref
            m.save(opts.outputpref+"r_{0}_l_{1}.topics".format(r,l))

        cs.append(((r,l),[c for t,c in co]))
        
        # Histograms of coherence
        vals=[c for t,c in co]
        h=pl.hist(vals)
        if s>0:
            pl.title("r={0},l={1},S*={2} (Avg. {3})".format(r,l,s,sum(vals)/len(vals)))
        else:
            pl.title("r={0},l={1} (Avg. {2})".format(r,l,sum(vals)/len(vals)))
        pl.show()
        print "Average coherence:",sum(vals)/len(vals)

      
    # Draw boxplot sizes
    ax = pl.subplot(111)
    pl.boxplot([d for x,d in cs])
    pl.xticks(range(1,len(cs)+1),["r={0},l={1}".format(x[0],x[1]) for x,d in
        cs],rotation="vertical")
    #pl.ylim((ax.get_ylim()[],0))
    pl.show()

  


