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
NMF, Online LDA and SMH topics.
"""
import argparse
import sys
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from cross_validation import evaluate_vocabulary_sizes

def main():
    try:
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser(
        description="Evaluates Online LDA in document classification")
        parser.add_argument("-p", "--path_to_save", type = str, default = None,
                            help = "file where to save the accuracies")
        parser.add_argument("-k", "--number_of_topics", type = int, default = 100,
                            help = "Number of LDA topics to model")
        parser.add_argument("-s", "--sizes", 
                            type = int, default = [1000, 2000, 3000, 4000, 5000, 
                                                   6000, 7000, 8000, 9000, 10000], 
                            nargs = '*',
                            help = "List of different vocabulary sizes to use")
        args = parser.parse_args()

        # vectorizes corpus and creates LDA model
        vectorizer = CountVectorizer(stop_words = 'english')
        lda = LatentDirichletAllocation(n_topics = args.number_of_topics,
                                        max_iter = 5,
                                        learning_method = 'online',
                                        batch_size = 4096,
                                        learning_decay = 0.5,
                                        learning_offset = 64,
                                        random_state = 1)
        title = "Online LDA (" + str(args.number_of_topics) + " topics)"
        # computes document classification accuracies
        accuracy = evaluate_vocabulary_sizes(vectorizer, lda, title, args.sizes)

        # saves accuracies
        if args.path_to_save:
            print "Saving accuracies in", args.path_to_save
            np.savetxt(args.path_to_save, accuracy)
        
    except SystemExit:
        print "for help use --help"
        sys.exit(2)

if __name__ == "__main__":
    main()
