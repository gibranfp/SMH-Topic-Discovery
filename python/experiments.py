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
    p.add_argument("--fig_pref",default=None,type=str,
        action="store", dest='fig_pref',help="Prefix for figures ")
    p.add_argument("--model_pref",default=None,type=str,
        action="store", dest='model_pref',help="Prefix of output files")
    p.add_argument("--topics_pref",default=None,type=str,
        action="store", dest='topics_pref',help="Prefix for topics as a text")
    p.add_argument("--cutoff",default=None,type=int,
        action="store", dest='cutoff',help="Cutoff of topics [Off]")
    p.add_argument("--clus",default=False,
        action="store_true", dest='clus',help="Cluster topics [Off]")
    p.add_argument("--clus_method",default=False,
        action="store", dest='clus_method',help="Cluster method [kmeans, ]")
    p.add_argument("--nclus",default=100,type=int,
        action="store", dest='nclus',help="Number of cluster if apply [100]")
    p.add_argument("--min_cluster_size",default=3,type=int,
            action="store", dest='min_cluster_size',help="Minimum size of cluster for default clustering[3]")
    p.add_argument("--min_coherence",default=2.0,type=float,
            action="store", dest='min_coherence',
            help="Minimum coherence on training[2.0]")
    p.add_argument("--thres",default=0.7,type=float,
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
    p.add_argument("train_corpus",default=None,
        action="store", help="Inverted file structure of documents with term frequencies for coherence filtering")
    p.add_argument("test_corpus",default=None,
        action="store", help="Inverted file structure of documents with term frequencies for coherence evaluation")



    print "======================================= Starting point"
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

    weights=None
    if opts.weights:
        print "Loading weights:",opts.weights
        weights=smh.Weights(opts.weights)

    expand=None
    if opts.expand:
        print "Loading corpus for expansion:",opts.expand
        expand=smh.smh_load(opts.expand)
        if not (expand.ldb.size==ifs.ldb.dim and expand.ldb.dim==ifs.ldb.size):
            print "ifs", ifs.ldb.size, ifs.ldb.dim, "corpus", expand.ldb.size, expand.ldb.dim
            print "Error with files inverted file and corpus"
            sys.exit(1)


    if not opts.l:
        params=[(int(r),s2l(s,r),s) for r,s in opts.params]
    else:
        params=[(int(r),int(l),0) for r,l in opts.params]
    sorted(params)

    cs=[]

    # Filter wiht coherence
    print "Loading coherence filtering corpus:",opts.train_corpus
    corpus_train=smh.smh_load(opts.train_corpus)

    print "Loading coherence for testing:",opts.test_corpus
    corpus_test=smh.smh_load(opts.test_corpus)

    for r,l,s in params:
        print "======================================= experiment for",r,l,s
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
            m.save("test.txt")
            final = time.clock() - start
            total+=final
            print "Size of cutted off mined topics:",m.size()
            print "Cutting off time:",final
        if opts.clus:
            print "Clustering topics..."
            if not opts.clus_method or opts.clus_method=='default':
                start = time.clock()
                c=m.cluster_mhlink(thres=opts.thres,min_cluster_size=opts.min_cluster_size)
            elif opts.clus_method=='kmeans':
                from sklearn.cluster import KMeans
                print "Using k-means"
                start = time.clock()
                kmeans = KMeans(init='k-means++',
                        n_clusters=opts.nclus,n_init=10,verbose=True)
                c=m.cluster_sklearn(kmeans)
            elif opts.clus_method=='minibatch':
                from sklearn.cluster import MiniBatchKMeans
                print "Using minibatch k-means"
                start = time.clock()
                minibatchkmeans =MiniBatchKMeans(init='k-means++',n_clusters=opts.nclus)
                c=m.cluster_sklearn(minibatchkmeans)
            elif opts.clus_method=='spectral':
                from sklearn.cluster import SpectralClustering
                print "Using spectral"
                start = time.clock()
                spectral = SpectralClustering(n_clusters=opts.nclus,eigen_solver="arpack")
                c=m.cluster_sklearn(spectral)


            final = time.clock() - start
            total+=final
            print "Size of clustered topics:",c.size()
            print "Clustering time off time:",final
            if c.size() > 0:
                m=c
            else:
                print "No topics clustered"
                continue

        # Filter wiht coherence
        print "Filtering by coherence..."
        print "Original number of topics",m.size()
        print "Calculating coherence on training..."
        m_,co=coherence(m,corpus_train,None,min_coherence=opts.min_coherence)
        print "Resulting number of topics",m_.size()
        vals=[c for t,c in co]
        print "Average coherence on training:",sum(vals)/len(vals)
        print "Calculating coherence on testing..."
        tmp_,co=coherence(m_,corpus_test,topic2corpus,min_coherence=-1)
        co=[(c,t) for t,c in co ]
        co.sort()
        co.reverse()
        cs.append(((r,l),co))
      
        if opts.model_pref:
            filename=opts.model_pref+"r_{0}_l_{1}.topics".format(r,l)
            print "Saving resulting model to",filename
            m_.save(filename)
        

        # Histograms of coherence
        vals=[c for c,t in co]
        if opts.fig_pref:
            h=pl.hist(vals)
            if s>0:
                pl.title("r={0},l={1},S*={2} (Avg. {3})".format(r,l,s,sum(vals)/len(vals)))
                fn=opts.fig_pref+"{0}_{1}_{2}.pdf".format(r,l,s)
            else:
                pl.title("r={0},l={1} (Avg. {2})".format(r,l,sum(vals)/len(vals)))
                fn=opts.fig_pref+"{0}_{1}.pdf".format(r,l)
            print "Saving fig",fn
            pl.savefig(fn,format='PDF')
            pl.clf()
        if opts.vtopics:
            print "======"
            print "First 10 topics (higher coherence)"
            for c,t in co[:10]:
                t=m_.ldb[t]
                ws=[voca[w.item] for w in t]
                print c,", ".join(ws)
            if len(co)>10:
                print "Last 10 topics (lowest coherence)"
                for c,t in co[-10:]:
                    t=m_.ldb[t]
                    ws=[voca[w.item] for w in t]
                    print c,", ".join(ws)
            print "======"
        if opts.topics_pref:
            filename=opts.topics_pref+"r_{0}_l_{1}.topics".format(r,l)
            print "Saving topics to",filename
            with open(filename ,'w') as ft:
                print "Total tópicos", len(co)
                for c,t in co:
                    t=m_.ldb[t]
                    ws=[voca[w.item] for w in t]
                    print >> ft,c,", ".join(ws)
        
        print "Total amount of time:",total
        print "Average coherence:",sum(vals)/len(vals)
        print "Maximum coherence:",max(vals)
        print "Minimum coherence:",min(vals)
        print "Total of topics:",m_.size()

    if len(cs)==0:
        print "NO TOPICS FOUND"
    else:
        # Draw boxplot sizes
        if opts.fig_pref:
            ax=pl.figure()
            vals=[[co for co,i in  d] for x,d in cs]
            pl.boxplot(vals)
            pl.xticks(range(1,len(cs)+1),["r={0},l={1},n={2}".format(x[0],x[1],len(d)) for x,d in
                cs],rotation="vertical")
            #pl.ylim((ax.get_ylim()[],0))
            fn=opts.fig_pref+"boxplot.pdf"
            print "Saving fig",fn
            pl.tight_layout()
            pl.savefig(fn,format='PDF')
            pl.clf()

  


