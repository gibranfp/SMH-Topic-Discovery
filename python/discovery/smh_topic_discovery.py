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
Intarface for topic discovery using Sampled Min-Hashing.
"""
import argparse
import sys
import numpy as np
from sklearn.base import BaseEstimator
    
class SMHTopicDiscovery(BaseEstimator):
    """
    SMH-based topic discovery.
    """
    def __init__(self,
                 tuple_size = 3,
                 n_tuples = 692,
                 wcc_thres = None,
                 overlap = 0.7):
        self.tuple_size = tuple_size

        if wcc_thres:
            self.wcc_thres = wcc_thres
            self.n_tuples = log(0.5) / log(1.0 - pow(wcc_thres, tuple_size))
        else:
            self.n_tuples = n_tuples

    def fit(self,
            X,
            tuple_size = 3,
            n_tuples = 692,
            weights = True,
            expand = True,
            thres = 0.7,
            cutoff = 3):
        """
        Discovers topics from a text corpus.
        """
        mined = ifs.mine(tuple_size=tuple_size,
                         num_tuples=n_tuples,
                         weights=weights,
                         expand=expand)
        mined.cutoff(min=cutoff)
        self.models = mined.cluster_mhlink(thres=thres)

        return self.models
    
def main():
    try:
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser(
        description="Performs topic discovery using Sampled Min-Hashing")
        parser.add_argument("-m", "--models", type=str, default=None,
                            help="file where to save the models (as lists of ids)")
        parser.add_argument("-t", "--topics", type=str, default=None,
                            help="file where to save the topics (as lists of terms)")
        args = parser.parse_args()
        
    except SystemExit:
        print "for help use --help"
        sys.exit(2)

if __name__ == "__main__":
    main()
