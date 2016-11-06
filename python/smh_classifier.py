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

def array_to_listdb(X):
    # if type(X) is csr_matrix:
    #     listdb = SMH(ldb=csr_to_listdb(X.T))
    # elif type(X) is ndarray:
    #     listdb = SMH(ldb=ndarray_to_listdb(X.T))
    # else:
    #     raise Exception('Invalid array type')
    return csr_to_listdb(X.T)

class SMHClassifier(BaseEstimator):
    """
    SMH-based classifier.
    """
    def __init__(self, tuple_size = 3, n_tuples = 692, wcc = None, ovr_thres = 0.7):
        self.tuple_size = tuple_size
        self.n_tuples = n_tuples

        if wcc:
            self.wcc = wcc
            self.n_tuples = ntuples

    def discover_topics(self,X,tuple_size=3,ntuples=692,weights=None,expand=False,thres=0.7,cutoff=5):
        ifs = array_to_listdb(X)
        mined = ifs.mine(tuple_size=tuple_size,
                             num_tuples=ntuples,
                             weights=weights,
                             expand=expand)
        mined.cutoff(min=cutoff)
        models = mined.cluster_mhlink(thres=thres, tuple_size=3, n_tuples=10)
        
        return SparseCoder(dictionary=normalize(models.toarray()))

    def fit(self,X,tuple_size=3,ntuples=10,weights=None,expand=False,thres=0.7,cutoff=5):
        self.coder = self.discover_topics(X,
                                          tuple_size=tuple_size,
                                          ntuples=ntuples,
                                          weights=weights,
                                          expand=expand,
                                          thres=thres,
                                          cutoff=cutoff)
        
    def transform(self, X):
        return self.coder.transform(X)




