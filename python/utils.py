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
import matplotlib
matplotlib.use('Agg')
import math
import time
timestr = time.strftime("%Y%m%d-%H%M%S")
from time import time
from sklearn import metrics

verbose = lambda *a: None
def centers_from_docsets_labels(listdb, docsets, labels):
   data = listdb.toarray()
   number_of_classes = np.max(labels) + 1
   centers = np.zeros((number_of_classes, data.shape[1]))
    
   sizes = np.zeros(number_of_classes)
   for i,d in enumerate(docsets.ldb):
       for j in d:
           centers[labels[i]] += data[j.item,:]
       sizes[labels[i]]+=d.size

   for i in range(number_of_classes):
        centers[i]=centers[i]/sizes[i]
   return centers

def bench_k_means(labels, labels_, name, data):
    print('%20s  %.3f   %.3f   %.3f   %.3f   %.3f'
          % ( name,
             metrics.homogeneity_score(labels,   labels_),
             metrics.completeness_score(labels,  labels_),
             metrics.v_measure_score(labels,     labels_),
             metrics.adjusted_rand_score(labels, labels_),
             metrics.adjusted_mutual_info_score(labels, labels_)))
    nbins=len(set(labels_))
    vals,bins=np.histogram(labels_,bins=nbins)
    print 20*' ','hist-min,max',np.min(vals),np.max(vals)

def s2l(s,r):
    return int(math.log(0.5)/math.log(1-math.pow(s,r)))

def predict(centers,data):
    centers_sn=(centers*centers).sum(axis=1)
    data_sn=(data*data).sum(axis=1)
    labels=np.zeros(data.shape[0])
    for sidx in range(data.shape[0]):
        min_dist=-1
        for cidx in range(centers.shape[0]):
            dist=0.0
            dist+=np.dot(data[sidx],centers[cidx])
            dist*=-2
            dist+=centers_sn[cidx]
            dist+=data_sn[sidx]
            if min_dist==-1 or dist < min_dist:
                labels[sidx]=cidx
                min_dist=dist
    return labels
    

