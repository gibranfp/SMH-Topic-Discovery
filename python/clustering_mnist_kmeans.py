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

    if opts.force or not os.path.exists(opts.CORPUS+".weight.corpus"):
        verbose("Creating vector file (floats)")

        with open(opts.CORPUS+".weight.corpus",'w') as f:
            for datum in dataf:
                datum=["{0}:{1}".format(i,x)
                            for i,x in enumerate(datum) if x>0]
                line="{0} {1}\n".format(len(datum)," ".join(datum))
                f.write(line)
            f.close()

    corpus_l1lsh = lsh.lsh_load(opts.CORPUS+".freq.corpus",scheme="l1lsh")
    corpus_l1lsh.ldb.dim=784
    #corpus_lplsh = lsh.lsh_load(opts.CORPUS+".weight.corpus",scheme="lplsh")
    #corpus_lplsh.vdb.dim=784

    verbose("Categories: ",k_size) 
    verbose("Samples   : ",n_samples) 
    verbose("Features  : ",n_features) 

    verbose("Clustering minibatch: ",k_size)
    mini=MiniBatchKMeans(n_clusters=k_size, init='k-means++',
                             batch_size=1000)
    mini.fit(data)
    bench_k_means(labels,mini.labels_,"mb:"+str(k_size),data)

    verbose("Clustering kmeans: ",k_size)
    kmeans=MiniBatchKMeans(n_clusters=k_size, init='k-means++')
    kmeans.fit(data)
    bench_k_means(labels,kmeans.labels_,"km:"+str(k_size),data)
