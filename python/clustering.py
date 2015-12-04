#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Sampled MinHash clustering
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
from eval.consistency import topics_entropy_sum
import time
timestr = time.strftime("%Y%m%d-%H%M%S")
from time import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

verbose = lambda *a: None
def centers_from_docs_labels(listdb, data):
    data = listdb.tocsr()
    centers = np.zeros((10, data.shape[1]))
    for i,l in enumerate(data):
        for j in l:
            centers[i] += data[j[item],:]
        centers[i]/l.size()
    return centers


def centers_from_docsets_labels(listdb, docsets, labels):
   data = listdb.toarray()
   number_of_classes = np.max(labels) + 1
   centers = np.zeros((number_of_classes, data.shape[1]))
   
    
   sizes = np.zeros(number_of_classes)
   for i,d in enumerate(docsets.ldb):
       for j in d:
           centers[labels[i]] += data[j.item,:]
       sizes[labels[i]]+=d.size

   

   #setsizes = np.zeros(docsets.size())
   #for i,d in enumerate(docsets.ldb):
   #    setsizes[i] = d.size

   #for i in range(number_of_classes):
   #    centers[i] /= setsizes[np.where(labels==i)].sum()
   
   for i in range(number_of_classes):
        centers[i]=centers[i]/sizes[i]
   return centers



def bench_k_means(estimator, name, data):
    t0 = time()
    estimator.fit(data)
    print('% 9s   %.2fs    %i   %.3f   %.3f   %.3f   %.3f   %.3f    %.3f'
          % (name, (time() - t0), estimator.inertia_,
             metrics.homogeneity_score(labels, estimator.labels_),
             metrics.completeness_score(labels, estimator.labels_),
             metrics.v_measure_score(labels, estimator.labels_),
             metrics.adjusted_rand_score(labels, estimator.labels_),
             metrics.adjusted_mutual_info_score(labels,  estimator.labels_),
             metrics.silhouette_score(data, estimator.labels_,
                                      metric='euclidean',
                                      sample_size=sample_size)))

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
    p.add_argument("--cutoff",default=None,type=int,
        action="store", dest='cutoff',help="Cutoff of topics [Off]")
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
    p.add_argument("-v", "--verbose",                                          
            action="store_true", dest="verbose",                           
            help="Verbose mode [Off]") 


    opts = p.parse_args()                                                      
                                                                                       
    if opts.verbose:                                                           
        def verbose(*args):                                                    
            print "".join([str(a) for a in args])  


    # TODO calculate these two options
    weights=None
    expand=None

    # Loading data
    digits = load_digits()
    data = digits.data
    #data = 255*data
    data = data.astype(int)

    n_samples, n_features = data.shape
    n_digits = len(np.unique(digits.target))
    labels = digits.target

    sample_size = 300

    verbose("n_digits: %d, \t n_samples %d, \t n_features %d"
      % (n_digits, n_samples, n_features))

    bench_k_means(KMeans(init='k-means++', n_clusters=n_digits, n_init=10),
              name="k-means++", data=data)

    bench_k_means(KMeans(init='random', n_clusters=n_digits, n_init=10),
              name="random", data=data)

    pca = PCA(n_components=n_digits).fit(data)
    bench_k_means(KMeans(init=pca.components_, n_clusters=n_digits, n_init=1),
              name="PCA-based",
              data=data)

    docs=smh.ndarray_to_listdb(data)

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
        print "Mining topics..."
        m=docs.mine(r,l,weights=weights,expand=expand)
        print "Size of original mined topics:",m.size()
        if opts.cutoff:
            print "Cutting off topics..."
            m.cutoff(min=opts.cutoff)
        print "Size of cutted off mined topics:",m.size()
        from sklearn.cluster import KMeans
        print "Using k-means"
        kmeans = KMeans(init='k-means++',
                n_clusters=n_digits,n_init=10,verbose=False)
        data_=m.toarray()
        kmeans.fit(data_)

        centers=centers_from_docsets_labels(docs, m,  kmeans.labels_)
    
        predictions=[]
        for datum in data:
            candidates=[]
            for center in centers:
                candidates.append(np.dot(centers,datum))
            predictions.append(np.argmin(candidates))
        
        print('% 9s   %.2fs    %i   %.3f   %.3f   %.3f   %.3f   %.3f    '
          % ("SMH", 0, kmeans.inertia_,
             metrics.homogeneity_score(labels, predictions),
             metrics.completeness_score(labels, predictions),
             metrics.v_measure_score(labels, predictions),
             metrics.adjusted_rand_score(labels, predictions),
             metrics.adjusted_mutual_info_score(labels, predictions)))
             #metrics.silhouette_score(data, predictions,
             #                         metric='euclidean',
             #                         sample_size=sample_size)))

       
        
       

    # in this case the seeding of the centers is deterministic, hence we run the
    # kmeans algorithm only once with n_init=1
    #pca = PCA(n_components=n_digits).fit(data)
    #bench_k_means(KMeans(init=pca.components_, n_clusters=n_digits, n_init=1),
    #              name="PCA-based",
    #              data=data)
    #print(79 * '_')

    ###############################################################################
    # Visualize the results on PCA-reduced data

    #reduced_data = PCA(n_components=2).fit_transform(data)
    #kmeans = KMeans(init='k-means++', n_clusters=n_digits, n_init=10)
    #kmeans.fit(reduced_data)

    # Step size of the mesh. Decrease to increase the quality of the VQ.
    #h = .02     # point in the mesh [x_min, m_max]x[y_min, y_max].

    # Plot the decision boundary. For that, we will assign a color to each
    #x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
    #y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
    #3xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Obtain labels for each point in mesh. Use last trained model.
    #Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    #Z = Z.reshape(xx.shape)
    #plt.figure(1)
    #plt.clf()
    #plt.imshow(Z, interpolation='nearest',
    #           extent=(xx.min(), xx.max(), yy.min(), yy.max()),
    #           cmap=plt.cm.Paired,
    #           aspect='auto', origin='lower')

    #plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
    # Plot the centroids as a white X
    #centroids = kmeans.cluster_centers_
    #plt.scatter(centroids[:, 0], centroids[:, 1],
    #            marker='x', s=169, linewidths=3,
    #            color='w', zorder=10)
    #plt.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
    #          'Centroids are marked with white cross')
    #plt.xlim(x_min, x_max)
    #plt.ylim(y_min, y_max)
    #plt.xticks(())
    #plt.yticks(())
    #plt.show()
