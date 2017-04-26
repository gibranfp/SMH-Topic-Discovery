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
Generates cross-validation partitions to evaluate LDA / SMH in document classification.
"""
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.datasets import fetch_20newsgroups
from sklearn.metrics import f1_score

def kfold_cv(X, y, k = 10):
    """
    Generator for k-fold cross-validation from a given text data and target.
    Used to evaluate topic discovery methods and SVM classifier.
    """
    fold_size = int(X.shape[0] / 10)
    for i in range(k):
        valid_mask = np.zeros(X.shape[0], dtype=bool)
        valid_mask[fold_size * i:fold_size * (i + 1)] = True

        train_mask = np.logical_not(valid_mask)
        
        X_train = X[train_mask, :]
        y_train = y[train_mask]
        
        X_valid = X[valid_mask, :]
        y_valid = y[valid_mask]

        yield i, X_train, y_train, X_valid, y_valid

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

        lsvc = LinearSVC( C = 1.0, 
                          class_weight = None, 
                          dual = False, 
                          fit_intercept = True,
                          intercept_scaling = 1, 
                          loss= 'squared_hinge', 
                          max_iter = 1000, 
                          multi_class = 'ovr',
                          penalty = 'l2', 
                          random_state = 1, 
                          tol = 0.001, 
                          verbose = 0)
        lsvc.fit(topic_rep_train, target_train)
        accuracy[i] = lsvc.score(topic_rep_valid, target_valid)

        print "   Fold ", i, 
        print "      train data size =", X_train.shape
        print "      validation data size = ", X_valid.shape 
        print "      accuracy = ", accuracy[i]
        
    return accuracy.mean()

def evaluate_vocabulary_sizes(vectorizer, model, name, vocabulary_sizes):
    """
    Evaluates a topic discovery method in document classification
    with different vocabulary sizes and using k-fold cross-validation. 
    Topics are first discovered from the train documents and then all documents 
    are represented using the discovered topics. This representation is used to train and
    validate a linear svm classifier.
    """
    print "Loading dataset"
    dataset = fetch_20newsgroups(subset = 'all', 
                                 remove = ('headers', 'footers', 'quotes'))

    print "Evaluating ", name
    accuracy = np.zeros(len(vocabulary_sizes))
    for i,nf in enumerate(vocabulary_sizes):
        print "Vocabulary size = ", nf
        vectorizer.set_params(max_features = nf)
        accuracy[i] = evaluate_model(model, vectorizer, dataset.data, dataset.target)
        
    return accuracy
