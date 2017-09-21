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
Performs document classification from document representations created from
SMH topics.
"""
from sklearn.base import BaseEstimator
from sklearn.preprocessing import normalize
from sklearn.decomposition import SparseCoder
from smh import array_to_listdb
from smh import SMHDiscoverer
from scipy.sparse.csr import csr_matrix
from math import log, pow
import numpy as np
import smh_api as sa

class SMHClassifier(BaseEstimator):
    """
    SMH-based classifier.
    """
    def __init__(self, 
                 tuple_size = 3,
                 number_of_tuples = 255,
                 table_size = 2**19,
                 cooccurrence_threshold = None, 
                 min_set_size = 3,
                 cluster_number_of_tuples = 255,
                 cluster_tuple_size = 3,
                 cluster_table_size = 2**20,
                 overlap = 0.7,
                 min_cluster_size = 3,
                 number_of_topics = 100):
        self.discoverer_ = SMHDiscoverer(tuple_size = tuple_size,
                                         number_of_tuples = number_of_tuples,
                                         table_size = table_size,
                                         cooccurrence_threshold = cooccurrence_threshold, 
                                         min_set_size = min_set_size,
                                         cluster_number_of_tuples = cluster_number_of_tuples,
                                         cluster_tuple_size = cluster_tuple_size,
                                         cluster_table_size = cluster_table_size,
                                         overlap = overlap,
                                         min_cluster_size = min_cluster_size)
        self.number_of_topics = number_of_topics
        
    def fit(self, X, weights = False, expand = True):
        """
        Discovers topics and used them as a dictionary for sparse-coding.
        """
<<<<<<< HEAD
        ifs = array_to_listdb(X.T)
        if expand:
            corpus = ifs.invert()
        else:
            corpus = None

        self.models = self.discoverer_.fit(ifs, expand = corpus)
        # codebook = self.models.toarray()
        # codebook = np.zeros((self.models.size(), self.models.dim()))
        # topic_scores = []
        # if self.number_of_topics:
        #     for i,m in enumerate(self.models.ldb):
        #         for j,t in enumerate(m):
        #             idf = log(float(corpus.size()) / listdb.ldb[t.item].size)
        #             codebook[i,j] = (0.5 *  (t.freq / m[0].freq) + 0.5) * idf
        #         topic_scores.append(codebook[i,:].mean())
        #     topic_indices = np.argsort(topic_scores)[::-1]
        #     codebook = codebook[topic_indices, :]
        #     codebook = codebook[:self.number_of_topics,:]

        # self.coder = SparseCoder(dictionary = codebook,
        #                          transform_algorithm = 'lasso_lars',
        #                          transform_alpha = 0.001,
        #                          split_sign = True,
        #                          n_jobs = 4)
=======
        models = self.smh_.fit(X, weights, expand)
        self.coder_ = SparseCoder(dictionary = normalize(models.toarray()),
                                 transform_algorithm = 'lasso_lars',
                                 split_sign = True,
                                 n_jobs = 4)
>>>>>>> bdeb95e068a7735d500bed1ffa37c8e6df67dbce
        
    def fit_transform(self, X, weights = None, expand = True):
        """
        Discovers topics and used them as a dictionary to sparse-code
        the documents.
        """
        self.fit(X, weights = weights, expand = expand)
<<<<<<< HEAD
        return self.transform(X)
        # return self.coder.fit_transform(X.todense())
=======
        return self.coder_.fit_transform(X.toarray())
>>>>>>> bdeb95e068a7735d500bed1ffa37c8e6df67dbce

    
    def transform(self, X):
        """
        Sparse-code a given set of documents from the
        discovered topics.
        """
<<<<<<< HEAD
        X_transformed = np.zeros((X.shape[0], self.models.size()))
        listdb = array_to_listdb(X)
        for i,d in enumerate(listdb.ldb):
            for j,m in enumerate(self.models.ldb):
                X_transformed[i,j] = sa.list_jaccard(m,d)

        print X_transformed
        # return self.coder.transform(X.todense())
=======
        return self.coder_.transform(X.toarray())
>>>>>>> bdeb95e068a7735d500bed1ffa37c8e6df67dbce
