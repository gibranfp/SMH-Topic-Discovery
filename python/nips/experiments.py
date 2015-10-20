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
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pl
from smh import smh
import math
from eval.coherence import coherence, utils
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

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
    p.add_argument("--figdir",default="fig",type=str,
        action="store", dest='figdir',help="Output figures directory")
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
    p.add_argument("--expand",default=None,
            action="store", dest="expand",
            help="TF ifs file")
    p.add_argument("--weights",default=None,
            action="store", dest="weights",
            help="Weights file")
    p.add_argument("ifs",default=None,
        action="store", help="Inverted file structure of documents")
    p.add_argument("corpus",default=None,
        action="store", help="Inverted file structure of documents with term frequencies")


    opts = p.parse_args()

    if len(opts.params)>1:
        opts.params.pop(0)

    topic2corpus=None
    if ( opts.vcorpus and not opts.vtopics):
        print "Both vocabularies have to be given the vocabulary of the corpus and topics"
        sys.exit(0)
    else:
        if opts.vcorpus:
            topic2corpus=utils.t2c(opts.vtopics,opts.vcorpus)
    
    if opts.vtopics:
        voca=utils.i2v(opts.vtopics)


    print "Loading file ifs:",opts.ifs
    ifs=smh.smh_load(opts.ifs)

    print "Loading testing corpus:",opts.corpus
    corpus=smh.smh_load(opts.corpus)

    weights=None
    if opts.weights:
        print "Loading weights:",opts.weights
        weights=smh.Weights(opts.weights)

    expand=None
    if opts.expand:
        print "Loading corpus for expansion:",opts.expand
        expand=smh.smh_load(opts.expand)

    if not opts.l:
        params=[(int(r),s2l(s,r),s) for r,s in opts.params]
    else:
        params=[(int(r),int(l),0) for r,l in opts.params]
    sorted(params)

    cs=[]

    for r,l,s in params:
        if s>0:
            print "Experiment tuples (r) {0}, Number of tuples (l) {1}, S* {2}".format(r,l,s)
        else:
            print "Experiment tuples (r) {0}, Number of tuples (l) {1}".format(r,l)
        print "Mining topics..."
        start = time.clock()
        m=ifs.mine(r,l,weights=weights,expand=expand)
        final = time.clock() - start
        total = final
        print "Size of original mined topics:",m.size()
        print "Mining time:",final
        if opts.cutoff:
            print "Cutting off topics..."
            start = time.clock()
            m.cutoff(min=opts.cutoff)
            final = time.clock() - start
            total+=final
            print "Size of cutted off mined topics:",m.size()
            print "Cutting off time:",final
        if opts.clus:
            print "Clustering topics..."
            start = time.clock()
            c=m.cluster_mhlink(3,255,thres=opts.thres)
            final = time.clock() - start
            total+=final
            print "Size of clustered topics:",c.size()
            print "Clustering time off time:",final
            if c.size() > 0:
                m=c
            else:
                print "No topics clustered"
                continue

        # EVAL coherence
        co=coherence(m,corpus,topic2corpus)
        if opts.outputpref:
            print "Saving resulting model to",opts.outputpref
            m.save(opts.outputpref+"r_{0}_l_{1}.topics".format(r,l))
        
        co=[(c,t) for t,c in co ]
        co.sort()
        co.reverse()
        cs.append(((r,l),co))
        
        # Histograms of coherence
        vals=[c for c,t in co]
        h=pl.hist(vals)
        if s>0:
            pl.title("r={0},l={1},S*={2} (Avg. {3})".format(r,l,s,sum(vals)/len(vals)))
            fn="{0}/hist_{1}_{2}_{3}_{4}.png".format(opts.figdir,r,l,s,timestr)
        else:
            pl.title("r={0},l={1} (Avg. {2})".format(r,l,sum(vals)/len(vals)))
            fn="{0}/hist_{1}_{2}_{3}.png".format(opts.figdir,r,l,timestr)
        print "Saving fig",fn
        pl.savefig(fn)
        if opts.vtopics:
            print "First 10 topics (higher coherence)"
            for c,t in co[:10]:
                t=m.ldb[t]
                ws=[voca[w.item] for w in t]
                print c,", ".join(ws)
            if len(co)>10:
                print "Last 10 topics (lowest coherence)"
                for c,t in co[-10:]:
                    t=m.ldb[t]
                    ws=[voca[w.item] for w in t]
                    print c,", ".join(ws)
            print "Total tópicos", len(co)
        print "Total amount of time:",total
        print "Average coherence:",sum(vals)/len(vals)



    if len(cs)==0:
        print "NO TOPICS FOUND"
    else:
        # Draw boxplot sizes
        ax = pl.subplot(111)
        pl.boxplot([d for x,d in cs])
        pl.xticks(range(1,len(cs)+1),["r={0},l={1}".format(x[0],x[1]) for x,d in
            cs],rotation="vertical")
        #pl.ylim((ax.get_ylim()[],0))
        fn="{0}/boxplot_{1}.png".format(opts.figdir,timestr)
        print "Saving fig",fn
        pl.savefig(fn)

  


