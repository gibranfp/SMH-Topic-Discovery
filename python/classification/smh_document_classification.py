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
import argparse
import sys
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from smh_classifier import SMHClassifier
from smh import rng_init
from document_classification import kfold_cv, evaluate_model, evaluate_vocabulary_sizes

def main():
    try:
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser(
        description="Evaluates SMH in document classification and plots the performances")
        parser.add_argument("--tuple_size", type=int, default=2,
                            help="Size of tuples")
        parser.add_argument("--number_of_tuples", type=int, default=None,
                            help="Number of tuples")
        parser.add_argument("--table_size", type=int, default=2**20,
                            help="Size of hash tables")
        parser.add_argument("--cooccurrence_threshold", type=float, default=0.02,
                            help="Weighted co-occurrence coefficient threshold")
        parser.add_argument("--min_set_size", type=int, default=3,
                           help="Minimum size of mined co-occurring term lists")
        parser.add_argument("--cluster_tuple_size", type=int, default=3,
                            help="Size of tuples")
        parser.add_argument("--cluster_number_of_tuples", type=int, default=255,
                            help="Number of tuples")
        parser.add_argument("--cluster_table_size", type=int, default=2**20,
                            help="Size of hash tables")
        parser.add_argument("--overlap", type=float, default=0.9,
                            help="Overlap threshold for MHLink")
        parser.add_argument("--min_cluster_size", type=int, default=5,
                            help="Minimum size of clusters")
        parser.add_argument("--seed", type=int, default=12345678,
                            help="Seed for random number generato")
        parser.add_argument("-p", "--path_to_save", type = str, default = None,
                            help = "file where to save the accuracies")
        parser.add_argument("-k", "--number_of_topics", type = int, default = 400,
                            help = "Number of SMH topics to model")
        parser.add_argument("-s", "--sizes", 
                            type = int, default = [50000],
                            nargs = '*',
                            help = "N")
        args = parser.parse_args()

        # vectorizes corpus and creates LDA model
        vectorizer = CountVectorizer(stop_words = 'english')
        smh = SMHClassifier(tuple_size = args.tuple_size,
                            number_of_tuples = args.number_of_tuples,
                            table_size = args.table_size,
                            cooccurrence_threshold = args.cooccurrence_threshold, 
                            min_set_size = args.min_set_size,
                            cluster_number_of_tuples = args.cluster_number_of_tuples,
                            cluster_tuple_size = args.cluster_tuple_size,
                            cluster_table_size = args.cluster_table_size,
                            overlap = args.overlap,
                            min_cluster_size = args.min_cluster_size,
                            number_of_topics = args.number_of_topics)
        rng_init(args.seed)

        title = "SMH (" + str(args.number_of_topics) + " topics)"

        # computes document classification accuracies
        accuracy = evaluate_vocabulary_sizes(vectorizer, smh, title, args.sizes)

        # saves accuracies
        if args.path_to_save:
            print "Saving accuracies in", args.path_to_save
            np.savetxt(args.path_to_save, accuracy)
        
    except SystemExit:
        print "for help use --help"
        sys.exit(2)

if __name__ == "__main__":
    main()
