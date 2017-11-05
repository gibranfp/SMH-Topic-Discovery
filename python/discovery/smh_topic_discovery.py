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
from smh import listdb_load, Weights, SMHDiscoverer, rng_init
from math import log
import time
import os
from topics import load_vocabulary, save_topics, save_time, get_models_docfreq, sort_topics, listdb_to_topics

class SMHTopicDiscovery(BaseEstimator):
    """
    SMH-based topic discovery.
    """
    def __init__(self,
                 tuple_size = 3,
                 number_of_tuples = None,
                 table_size = 2**20,
                 cooccurrence_threshold = 0.14, 
                 min_set_size = 3,
                 cluster_tuple_size = 3,
                 cluster_number_of_tuples = 255,
                 cluster_table_size = 2**20,
                 overlap = 0.7,
                 min_cluster_size = 3):

        self.tuple_size_ = tuple_size

        if number_of_tuples:
            self.cooccurrence_threshold_ = pow(1. -  pow(0.5, 1. / float(number_of_tuples)), 1. / float(tuple_size))
            self.number_of_tuples_ = number_of_tuples
        else:
            self.cooccurrence_threshold_ = cooccurrence_threshold
            self.number_of_tuples_ = int(log(0.5) / log(1.0 - pow(cooccurrence_threshold, tuple_size)))

        self.table_size_ = table_size
        self.min_set_size_ = min_set_size
        self.cluster_tuple_size_ = cluster_tuple_size
        self.cluster_number_of_tuples_ = cluster_number_of_tuples
        self.cluster_table_size_ = cluster_table_size
        self.overlap_ = overlap
        self.min_cluster_size_ = min_cluster_size
        self.discoverer_ = SMHDiscoverer(tuple_size = self.tuple_size_,
                                         number_of_tuples = self.number_of_tuples_,
                                         table_size = self.table_size_,
                                         cooccurrence_threshold = self.cooccurrence_threshold_, 
                                         min_set_size = self.min_set_size_,
                                         cluster_tuple_size = self.cluster_tuple_size_,
                                         cluster_number_of_tuples = self.cluster_number_of_tuples_,
                                         cluster_table_size = self.cluster_table_size_,
                                         overlap = self.overlap_,
                                         min_cluster_size = self.min_cluster_size_)
        
    def fit(self,
            X,
            weights = None,
            corpus = None):
        """
        Discovers topics from a text corpus.
        """
        self.models = self.discoverer_.fit(X,
                                           weights = weights,
                                           expand = corpus)
            
def discover_topics(ifspath,
                    vocpath,
                    savedir,
                    tuple_size = 3,
                    number_of_tuples = None,
                    table_size = 2**20,
                    cooccurrence_threshold = 0.14, 
                    min_set_size = 3,
                    weightspath = None,
                    corpuspath = None,
                    cluster_tuple_size = 3,
                    cluster_number_of_tuples = 255,
                    cluster_table_size = 2**20,
                    overlap = 0.7,
                    min_cluster_size = 3,
                    top_terms_numbers = [10],
                    seed = 12345678):
    """
    Discovers topics and evaluates model using topic coherence
    """
    rng_init(seed)

    print "Loading inverted file from", ifspath
    ifs = listdb_load(ifspath)

    print "Loading vocabulary from", vocpath
    vocabulary, docfreq = load_vocabulary(vocpath)
    
    corpus = None
    if corpuspath:
        print "Loading corpus from", corpuspath
        corpus = listdb_load(corpuspath)

    weights = None
    if weightspath:
        print "Loading weights from", weightspath
        weights = Weights(weightspath)

    model = SMHTopicDiscovery(tuple_size = tuple_size,
                              number_of_tuples = number_of_tuples,
                              table_size = table_size,
                              cooccurrence_threshold = cooccurrence_threshold, 
                              min_set_size = min_set_size,
                              cluster_tuple_size = cluster_tuple_size,
                              cluster_number_of_tuples = cluster_number_of_tuples,
                              cluster_table_size = cluster_table_size,
                              overlap = overlap,
                              min_cluster_size = min_cluster_size)

    print "Parameters set to "    
    print "   tuple_size =", tuple_size
    print "   number_of_tuples = ", number_of_tuples
    print "   table_size = ", table_size
    print "   cooccurrence_threshold = ", cooccurrence_threshold
    print "   min_set_size = ", min_set_size
    print "   cluster_tuple_size = ", cluster_tuple_size
    print "   cluster_number_of_tuples = ", cluster_number_of_tuples
    print "   cluster_table_size = ", cluster_table_size
    print "   overlap = ", overlap
    print "   min_cluster_size = ", min_cluster_size

    print "Discovering topics"    
    start_time = time.time()
    model.fit(ifs, weights = weights, corpus = corpus)
    end_time = time.time()
    total_time = end_time - start_time

    corpusname = os.path.splitext(os.path.basename(ifspath))[0]
    mine_config = '_r' + str(tuple_size) + '_l' +  str(model.number_of_tuples_)\
                  + '_w' + str(cooccurrence_threshold)
    mine_config = mine_config + '_s' + str(min_set_size)
    cluster_config = '_o' + str(overlap) + '_m' +  str(min_cluster_size)

    modelfile = savedir + '/smh' + mine_config + cluster_config + corpusname + '.models'
    print "Saving resulting models to", modelfile
    model.models.save(modelfile)

    # sort models and save them with different top terms numbers
    topicfile = savedir + '/smh' + mine_config + cluster_config + corpusname + '_unsorted.topics'
    print "Saving the terms of the topic to", topicfile
    save_topics(topicfile, listdb_to_topics(model.models, vocabulary) , top = None)

    print "Getting the document frequencies of the models"
    models_docfreq, topics = get_models_docfreq(model.models, vocabulary, docfreq)

    print "Sorting topics"
    for top in top_terms_numbers:
        sorted_topics = sort_topics(models_docfreq, topics, top = top)
        if top:
            top_str = '_top' + str(top)
        else:
            top_str = '_full'

        topicfile = savedir + '/smh' + mine_config + cluster_config + corpusname + top_str + '.topics'
        print "Saving the terms of the topic to", topicfile
        save_topics(topicfile, sorted_topics , top = top)

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
        parser.add_argument("--tuple_size", type=int, default=3,
                            help="Size of tuples")
        parser.add_argument("--number_of_tuples", type=int, default=None,
                            help="Number of tuples")
        parser.add_argument("--table_size", type=int, default=2**20,
                            help="Size of hash tables")
        parser.add_argument("--cooccurrence_threshold", type=float, default=0.14,
                            help="Weighted co-occurrence coefficient threshold")
        parser.add_argument("--min_set_size", type=int, default=3,
                           help="Minimum size of mined co-occurring term lists")
        parser.add_argument("--weights", type=str, default = None,
                            help="Weights file (list of document weights)")
        parser.add_argument("--corpus", type=str, default=None,
                            help="Corpus file (database of ID lists)")
        parser.add_argument("--cluster_tuple_size", type=int, default=3,
                            help="Size of tuples")
        parser.add_argument("--cluster_number_of_tuples", type=int, default=255,
                            help="Number of tuples")
        parser.add_argument("--cluster_table_size", type=int, default=2**20,
                            help="Size of hash tables")
        parser.add_argument("--overlap", type=float, default=0.7,
                            help="Overlap threshold for MHLink")
        parser.add_argument("--min_cluster_size", type=int, default=5,
                            help="Minimum size of clusters")
        parser.add_argument("--top", type=int, default=[10, None], nargs='*',
                            help="Configuration number to try")
        parser.add_argument("--seed", type=int, default=12345678,
                            help="Seed for random number generator")


        args = parser.parse_args()
        
        discover_topics(args.ifs,
                        args.vocabulary,
                        args.dir,
                        tuple_size = args.tuple_size,
                        number_of_tuples = args.number_of_tuples,
                        table_size = args.table_size,
                        cooccurrence_threshold = args.cooccurrence_threshold,
                        min_set_size = args.min_set_size,
                        weightspath = args.weights,
                        corpuspath = args.corpus,
                        cluster_tuple_size = args.cluster_tuple_size,
                        cluster_number_of_tuples = args.cluster_number_of_tuples,
                        cluster_table_size = args.cluster_table_size,
                        overlap = args.overlap,
                        min_cluster_size = args.min_cluster_size,
                        top_terms_numbers = args.top,
                        seed = args.seed)
        
    except SystemExit:
        print "for help use --help"
        sys.exit(2)

if __name__ == "__main__":
    main()
