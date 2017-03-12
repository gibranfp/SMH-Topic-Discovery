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
from sklearn.svm import LinearSVC
from sklearn.datasets import fetch_20newsgroups
from smh_classifier import SMHClassifier
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# maximum and minimum document frequency of a term
max_df = 0.95
min_df = 2

# vocabulary sizes to evaluate
vocabulary_sizes = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
configurations = ((CountVectorizer(max_df=0.9, min_df=5,
                                   stop_words='english'),
                   SMHClassifier(tuple_size=2, wcc=0.05,
                                 weights=args.weights, expand=args.corpus),
                   "SMH (s=0.05)"),
                  (CountVectorizer(max_df=0.9, min_df=5,
                                   stop_words='english'),
                   SMHClassifier(tuple_size=2, wcc=0.1,
                                 weights=args.weights, expand=args.corpus),
                   "SMH (s=0.1)"),
                  (CountVectorizer(max_df=0.9, min_df=5,
                                   stop_words='english'),
                   SMHClassifier(tuple_size=3, wcc=0.05,
                                 weights=args.weights, expand=args.corpus),
                   "SMH (s=0.05)"),
                  (CountVectorizer(max_df=0.9, min_df=5,
                                   stop_words='english'),
                   SMHClassifier(tuple_size=3, wcc=0.1,
                                 weights=args.weights, expand=args.corpus),
                   "SMH (s=0.1)"))

def kfold_cv(data, target, k = 10):
    """
    Generator for k-fold cross-validation from a given text data and target.
    Used to evaluate topic discovery methods and SVM classifier.
    """
    db_size = len(data)
    fold_size = int(db_size / 10)
    for i in range(k):
        complete_set = range(db_size)
        valid_set = complete_set[fold_size * i:fold_size * (i + 1)]
        train_set = [d for d in complete_set if d not in valid_set]
        
        data_train = [data[d] for d in train_set]
        target_train = [target[d] for d in train_set]

        data_valid = [data[d] for d in valid_set]
        target_valid = [target[d] for d in valid_set]

        yield i, data_train, target_train, data_valid, target_valid

def evaluate_model(model, vectorizer, data, target, k = 10):
    """
    Evaluates a topic discovery method in document classification
    using k-fold cross-validation. Topics are first discovered from
    the train documents and then all documents are represented using
    the discovered topics. This representation is used to train and
    validate a linear svm classifier.
    """
    accuracy = np.zeros(k)
    for i, data_train, target_train, data_valid, target_valid in kfold_cv(data, target, k = 10):
        X_train = vectorizer.fit_transform(data_train)
        X_valid = vectorizer.transform(data_valid)

        topic_rep_train = model.fit_transform(X_train)
        topic_rep_valid = model.transform(X_valid)

        lsvc = LinearSVC()
        lsvc.fit(topic_rep_train, target_train)
        accuracy[i] = lsvc.score(topic_rep_valid, target_valid)

    return accuracy.mean()


def plot_classification_accuracies(show_flag, path_to_save):
    """
    Evaluates SMH in document classification and plots the performances
    """
    print "Loading dataset"
    dataset = fetch_20newsgroups(subset='all', remove=('headers', 'footers', 'quotes'))

    fig = plt.figure(1, figsize=(9, 6))
    ax = fig.add_subplot(111)

    accuracy = np.zeros((len(configurations), len(vocabulary_sizes)))
    print "Evaluating topic discovery methods"
    for i, (vectorizer, model, name) in enumerate(configurations):
        print "Evaluating", name
        for j,nf in enumerate(vocabulary_sizes):
            vectorizer.set_params(max_features=nf)
            accuracy[i, j] = evaluate_model(model, vectorizer, dataset.data, dataset.target)
        ax.plot(vocabulary_sizes, accuracy, label=name)
        print "Accuracies = ", accuracy[i,:]

    ax.legend()
    plt.ylabel("Accuracy")
    plt.xlabel("Vocabulary size")

    if show_flag:
        plt.show()

    if path_to_save:
        plt.savefig(path_to_save)

def main():
    try:
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser(
        description="Evaluates SMH in document classification and plots the performances")
        parser.add_argument('-s', '--show_flag', action='store_true',
                            help="show figure")
        parser.set_defaults(fig=False)
        parser.add_argument("-p", "--path_to_save", type=str, default=None,
                            help="file where to save the figure")
        p.add_argument("--corpus",default=None, action="store", dest="corpus",
                       help="Corpus file")
        p.add_argument("--weights",default=None, action="store", dest="weights",
                       help="Weights file")

        args = parser.parse_args()
        plot_classification_accuracies(args.show_flag, args.path_to_save)
        
    except SystemExit:
        print "for help use --help"
        sys.exit(2)

if __name__ == "__main__":
    main()
