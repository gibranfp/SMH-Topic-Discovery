#!/usr/bin/env python
# -*- coding: utf-8
#
# Gibran Fuentes-Pineda <gibranfp@unam.mx>
# IIMAS, UNAM
# 2016
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
from smh.smh import ndarray_to_listdb, csr_to_listdb
from smh.smh import SMH
from scipy.sparse.csr import csr_matrix
from numpy import ndarray
from math import log, pow

def array_to_listdb(X):
    """
    Converts array (CSR or ndarray) to a dabase of lists
    """
    if type(X) is csr_matrix:
        listdb = csr_to_listdb(X.T)
    elif type(X) is ndarray:
        listdb = ndarray_to_listdb(X.T)
    else:
        raise Exception('Invalid array type')

    return listdb

class SMHClassifier(BaseEstimator):
    """
    SMH-based classifier.
    """
    def __init__(self, tuple_size=3, n_tuples=692,
                 wcc=None, ovr_thres=0.7):
        self.tuple_size = tuple_size

        if wcc:
            self.wcc = wcc
            self.n_tuples = log(0.5) / log(1.0 - pow(wcc, tuple_size))
        else:
            self.n_tuples = n_tuples

    def discover_topics(self, X, tuple_size=3, n_tuples=692,
                        weights=True, expand=True,
                        thres=0.7, cutoff=3):
        """
        Discovers topics from a text corpus.
        """
        ifs = array_to_listdb(X)
        mined = ifs.mine(tuple_size=tuple_size,
                         num_tuples=n_tuples,
                         weights=weights,
                         expand=expand)
        mined.cutoff(min=cutoff)
        models = mined.cluster_mhlink(thres=thres)
    
        return models

    def fit(self, X, tuple_size=3, n_tuples=692,
            weights=True, expand=True,
            thres=0.7, cutoff=3):
        """
        Discovers topics and used them as a dictionary for sparse-coding.
        """
        models = self.discover_topics(X,
                                      tuple_size=tuple_size,
                                      n_tuples=n_tuples,
                                      weights=weights,
                                      expand=expand,
                                      thres=thres,
                                      cutoff=cutoff)
        self.coder = SparseCoder(dictionary=normalize(models.toarray()),
                                 transform_algorithm='lasso_lars',
                                 split_sign=True,
                                 n_jobs=4)
        
    def fit_transform(self, X, tuple_size=3, n_tuples=692,
                      weights=None, expand=None,
                      thres=0.7, cutoff=3):
        """
        Discovers topics and used them as a dictionary to sparse-code
        the documents.
        """
        self.fit(X, tuple_size=tuple_size, n_tuples=n_tuples, weights=weights, expand=expand,
                 thres=thres, cutoff=cutoff)
        return self.coder.fit_transform(X.todense())

    
    def transform(self, X):
        """
        Sparse-code a given set of documents from the
        discovered topics.
        """
        return self.coder.transform(X.todense())










