#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Sampled MinHash clustering
# ----------------------------------------------------------------------
# Ivan V. Meza
# 2015/IIMAS, México
# ----------------------------------------------------------------------

import sys
sys.path.append('python')
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
from lsh import lsh
import time
timestr = time.strftime("%Y%m%d-%H%M%S")
from time import time
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn.datasets import fetch_mldata
from utils import *

verbose = lambda *a: None
# MAIN program
if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser("Mines")
    p.add_argument("CORPUS",
                help="Corpus file")
    p.add_argument("-p","--params",default=[(3,0.2)],
                action="append", dest="params",type=float,nargs=2,
                help="(Size of the tuple, S*| number of tuples)")
    p.add_argument("-l","--number_tuples",default=False,
                action="store_true", dest="l",
                help="Turn on second value op pair as parameter l, otherwise s*")
    p.add_argument("--cutoff",default=None,type=int,
        action="store", dest='cutoff',help="Cutoff of topics [Off]")
    p.add_argument("--clus_method",default=False,
        action="store", dest='clus_method',help="Cluster method [kmeans, ]")
    p.add_argument("--nclus",default=100,type=int,
        action="store", dest='nclus',help="Number of cluster if apply [100]")
    p.add_argument("--min_cluster_size",default=3,type=int,
            action="store", dest='min_cluster_size',help="Minimum size of cluster for default clustering[3]")
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
    p.add_argument("-f", "--forse",                                          
            action="store_true", dest="force",                           
            help="Forse to reload [Off]") 
    p.add_argument("-v", "--verbose",                                          
            action="store_true", dest="verbose",                           
            help="Verbose mode [Off]") 

    # Setting up command line
    opts = p.parse_args()                                                      
                                                                                       
    if opts.verbose:                                                           
        def verbose(*args):                                                    
            print "".join([str(a) for a in args])  


    #LOADING CORPUS
    digits = fetch_mldata('MNIST original', data_home="data/mnist")
    data = digits.data[:60000]
    datai = data.astype(int)
    dataf = data.astype(float)/255.0
    n_samples, n_features = datai.shape
    labels = digits.target[:60000]

    k_size = len(np.unique(labels))
    max_freq=np.amax(data)
    
    # Loading corpus
    if opts.force or not os.path.exists(opts.CORPUS+".freq.corpus"):
        verbose("Creating listdb file (int)")
        with open(opts.CORPUS+".freq.corpus",'w') as f:
            for datum in datai:
                datum=["{0}:{1}".format(i,int(x))
                            for i,x in enumerate(datum) if x>0]
                line="{0} {1}\n".format(len(datum)," ".join(datum))
                f.write(line)
            f.close()

    corpus_l1lsh = lsh.lsh_load(opts.CORPUS+".freq.corpus",scheme="l1lsh")
    corpus_l1lsh.ldb.dim=784

    verbose("Categories: ",k_size) 
    verbose("Samples   : ",n_samples) 
    verbose("Features  : ",n_features) 

    if len(opts.params)>1:
        opts.params.pop(0)

    if not opts.l:                                                             
        params=[(int(r),s2l(s,r),s) for r,s in opts.params]                    
    else:                                                                      
        params=[(int(r),int(l),0) for r,l in opts.params]                      
        sorted(params)                                                         
                                                                               
    for r,l,s in params:    
        print "======================================= experiment for",r,l,s
        if s>0:
            print "Experiment tuples (r) {0}, Number of tuples (l) {1}, S* {2}".format(r,l,s)
        else:
            print "Experiment tuples (r) {0}, Number of tuples (l) {1}".format(r,l)

        print "Number of samples", corpus_l1lsh.size()
        print "Clustering topics... L1LSH"
        clus=corpus_l1lsh.mine(r,l,int(max_freq))
        print "\nNumber of cluster discovered:",clus.size()
        if opts.cutoff:
            print "Cutting off topics..."
            clus.cutoff(min=opts.cutoff)
        print "\nNumber of clusters:",clus.size()
        if clus.size()<k_size:
            continue
 
        sizes=[]
        documents={}
        for c in clus.ldb:
            sizes.append(c.size)
            for d in range(c.size):
                d=c[d].item
                try:
                    documents[d]+=1
                except KeyError:
                    documents[d]=1

        print "-Total documents",np.sum(sizes)
        print "-Maximum documents",np.max(sizes)
        print "-Minimux documents",np.min(sizes)
        print "-Coverage documents", len(documents)


        print "Number of cut off clusters:",clus.size()
        clus=clus.cluster_mhlink(thres=opts.thres,min_cluster_size=opts.min_cluster_size)
        print "\nNumber of clusters:",clus.size()
        if clus.size()<k_size:
            continue
        sizes=[]
        documents={}
        for c in clus.ldb:
            sizes.append(c.size)
            for d in range(c.size):
                d=c[d].item
                try:
                    documents[d]+=1
                except KeyError:
                    documents[d]=1



        print "Total documents",np.sum(sizes)
        print "Maximum documents",np.max(sizes)
        print "Minimux documents",np.min(sizes)
        print "Coverage documents", len(documents)

        verbose("Calculating centers")
        centers=centers_from_docsets_labels(corpus_l1lsh, clus,  range(clus.size()))
        verbose("Number of centers: ",len(centers))
        labels_=predict(centers,datai)
        bench_k_means(labels,labels_,"LSH'(%d,%d)"%(r,l),corpus_l1lsh)
       
        kmeans = KMeans(init='k-means++',                                      
                        n_clusters=k_size,                                   
                        n_init=10)                                             
        kmeans.fit(centers)                                                    
        predictions=kmeans.predict(datai)
        bench_k_means(labels,predictions,"L1LSH-kmeans'(%d,%d)"%(r,l),corpus_l1lsh)

