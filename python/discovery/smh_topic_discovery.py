#!/usr/bin/env python
# -*- coding: utf-8
#
# Gibran Fuentes-Pineda <gibranfp@unam.mx>
# IIMAS, UNAM
# 2017
#
# -------------------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -------------------------------------------------------------------------
"""
Intarface for topic discovery using Sampled Min-Hashing.
"""
import argparse
import sys
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.cluster import MiniBatchKMeans, KMeans, SpectralClustering
from smh import smh
from math import log
import time
import os

def load_vocabulary(vocpath):
    """
    Reads a vocabulary and stores it in a dictionary
    """
    vocabulary = {}
    with open(vocpath, 'r') as f:
        content = f.readlines()
        for line in content:
            tokens = line.split(' = ')
            vocabulary[int(tokens[1])] = tokens[0]

    return vocabulary

def models_to_topics(models, vocpath):
    """
    Reads a vocabulary and stores it in a dictionary
    """
    topics = []
    vocabulary = load_vocabulary(vocpath)
    for m in models.ldb:
        terms = []
        for j in m:
            terms.append(vocabulary[j.item])
        topics.append(terms)

    return topics

def save_topics(filepath, topics, top = None):
    """
    Saves topics to a file
    """
    with open(filepath, 'w') as f:
        for t in topics:
            if top:
                f.write(' '.join(t[:top]).encode('utf8'))
            else:
                f.write(' '.join(t).encode('utf8'))
            f.write('\n'.encode('utf8'))

def save_time(filepath, total_time):
    """
    Saves time to a file
    """
    with open(filepath, 'w') as f:
        f.write(str(total_time))

class SMHTopicDiscovery(BaseEstimator):
    """
    SMH-based topic discovery.
    """
    def __init__(self,
                 tuple_size = 3,
                 n_tuples = 692,
                 wcc = None,
                 overlap = 0.7,
                 min_mined_size = 5,
                 clustering = 'mhlink',
                 min_cluster_size = 5,
                 number_of_clusters = 100):
        self.tuple_size = tuple_size
        self.overlap = overlap
        self.min_mined_size = min_mined_size
        self.clustering = clustering
        self.min_cluster_size = min_cluster_size
        self.number_of_clusters = number_of_clusters

        if wcc:
            self.wcc = wcc
            self.n_tuples = int(log(0.5) / log(1.0 - pow(wcc, tuple_size)))
        elif n_tuples:
            self.n_tuples = n_tuples

        clustering_option = {
            'minibatch' : MiniBatchKMeans(n_clusters = number_of_clusters),
            'kmeans' : KMeans(n_clusters = number_of_clusters,),
            'spectral' : MiniBatchKMeans(n_clusters = number_of_clusters)
        }
        if self.clustering != 'mhlink':
            self.algorithm = clustering_option.get(self.clustering, None)
            if not self.algorithm:
                print clustering, "is not a valid clustering algorithm. Using MinibatchKmeans."
                self.algorithm = clustering_option['minibatch']

    def fit(self,
            X,
            weights = None,
            corpus = None):
        """
        Discovers topics from a text corpus.
        """
        mined = X.mine(tuple_size = self.tuple_size,
                       num_tuples = self.n_tuples,
                       weights = weights,
                       expand = corpus)
        mined.cutoff(min = self.min_mined_size)

        if self.clustering == 'mhlink':
            self.models = mined.cluster_mhlink(thres = self.overlap,
                                               min_cluster_size = self.min_cluster_size)
        else:
            self.models = mined.cluster_sklearn(self.algorithm)

def discover_topics(ifspath,
                    vocpath,
                    savedir,
                    tuple_size = 3,
                    wcc = 0.12,
                    n_tuples = None,
                    min_mined_size = 5,
                    overlap = 0.7,
                    weightspath = None,
                    corpuspath = None,
                    clustering = 'mhlink',
                    min_cluster_size = 5,
                    number_of_clusters = 100,
                    top_terms_numbers = [10]):
    """
    Discovers topics and evaluates model using topic coherence
    """
    print "Loading inverted file from ", ifspath
    ifs = smh.smh_load(ifspath)

    corpus = None
    if corpuspath:
        print "Loading corpus from ", corpuspath
        corpus = smh.smh_load(corpuspath)

    weights = None
    if weightspath:
        print "Loading weights from ", weightspath
        weights = smh.Weights(weightspath)

    model = SMHTopicDiscovery(tuple_size = tuple_size,
                              n_tuples = n_tuples,
                              wcc = wcc,
                              min_mined_size = min_mined_size,
                              overlap = overlap,
                              min_cluster_size = min_cluster_size,
                              clustering = clustering,
                              number_of_clusters = number_of_clusters)

    print "Discovering topics with smh (", clustering, ")"
    start_time = time.time()
    model.fit(ifs, weights = weights, corpus = corpus)
    end_time = time.time()
    total_time = end_time - start_time
              
    print "Generating topics (lists of terms) from models"
    topics = models_to_topics(model.models, vocpath)

    corpusname = os.path.splitext(os.path.basename(ifspath))[0]
    mine_config = '_r' + str(tuple_size) + '_l' +  str(model.n_tuples) + '_w' + str(wcc)
    mine_config = mine_config + '_s' + str(min_mined_size)
    if clustering == 'mhlink':
        cluster_config = '_mhlink_o' + str(overlap) + '_m' +  str(min_cluster_size)
    else:
        cluster_config = '_' + clustering + '_k' + str(number_of_clusters)
        
    modelfile = savedir + '/smh' + mine_config + cluster_config + corpusname + '.models'
    print "Saving resulting models to", modelfile
    model.models.save(modelfile)

    # save topics with different top terms numbers
    for top in top_terms_numbers:
        if top:
            top_str = '_top' + str(top)
        else:
            top_str = '_full'
           
        topicfile = savedir + '/smh' + mine_config + cluster_config + corpusname + top_str + '.topics'
        print "Saving the terms of the topic to", topicfile
        save_topics(topicfile, topics, top = top)

    timefile = savedir + '/smh' + mine_config + cluster_config + corpusname + '.time'
    print "Saving times to", timefile
    save_time(timefile, total_time)

def main():
    try:
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser(
        description="Evaluates Sampled Min-Hashing in topic discovery")
        parser.add_argument("ifs", type=str,
                            help="Inverted file of corpus (database of ID lists)")
        parser.add_argument("vocabulary", type=str,
                            help="Vocabulary file for corpus")
        parser.add_argument("dir", type=str,
                            help="Directory where the models, topics and times are to be saved")
        parser.add_argument("--corpus", type=str, default=None,
                            help="Corpus file (database of ID lists)")
        parser.add_argument("--clustering", type=str, default='mhlink',
                            help="Clustering algorithm to use")
        parser.add_argument("--overlap", type=float, default=0.7,
                            help="Overlap threshold for MHLink")
        parser.add_argument("--min_mined_size", type=int, default=4,
                            help="Minimum size of mined co-occurring term lists")
        parser.add_argument("--min_cluster_size", type=int, default=5,
                            help="Minimum size of clusters")
        parser.add_argument("--n_tuples", type=int, default=None,
                            help="Number of tuples")
        parser.add_argument("--number_of_clusters", type=int, default=100,
                            help="Number of clusters when clustering algorithm is not MHLink")
        parser.add_argument("--top", type=int, default=[5, 10, 15, 20, None], nargs='*',
                            help="Configuration number to try")
        parser.add_argument("--tuple_size", type=int, default=3,
                            help="Size of tuples")
        parser.add_argument("--wcc", type=float, default=0.12,
                            help="Weighted co-occurrence coefficient threshold")
        parser.add_argument("--weights", type=str, default = None,
                            help="Weights file (list of document weights)")

        args = parser.parse_args()
        
        discover_topics(args.ifs,
                        args.vocabulary,
                        args.dir,
                        tuple_size = args.tuple_size,
                        wcc = args.wcc,
                        n_tuples = args.n_tuples,
                        min_mined_size = args.min_mined_size,
                        overlap = args.overlap,
                        weightspath = args.weights,
                        corpuspath = args.corpus,
                        clustering = args.clustering,
                        min_cluster_size = args.min_cluster_size,
                        number_of_clusters = args.number_of_clusters,
                        top_terms_numbers = args.top)
        
    except SystemExit:
        print "for help use --help"
        sys.exit(2)

if __name__ == "__main__":
    main()
