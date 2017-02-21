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
NMF, Online LDA and SMH topics.
"""
import argparse
import sys
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.svm import LinearSVC
from sklearn.datasets import fetch_20newsgroups
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from nltk.corpus.reader.wordnet import NOUN, VERB, ADV, ADJ
from nltk.corpus.reader.wordnet import NOUN

morphy_tag = {
    'JJ' : ADJ,
    'JJR' : ADJ,
    'JJS' : ADJ,
    'VB' : VERB,
    'VBD' : VERB,
    'VBG' : VERB,
    'VBN' : VERB,
    'VBP' : VERB,
    'VBZ' : VERB,
    'RB' : ADV,
    'RBR' : ADV,
    'RBS' : ADV
}

def line2terms(line):
    """
    Converts original text line to tokenized and lemmatized terms
    """
    tokens = word_tokenize(line.lower())
    tagged = pos_tag(tokens)
    lemmatizer = WordNetLemmatizer()
    terms = []
    for w,t in tagged:
         terms.append(lemmatizer.lemmatize(w, pos=morphy_tag.get(t, NOUN)))

    return terms

# maximum and minimum document frequency of a term
max_df = 0.95
min_df = 2

# vocabulary sizes to evaluate
vocabulary_sizes = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]

# Topic discovery configurations to evaluate
configurations = ((TfidfVectorizer(max_df=max_df,
                                   min_df=min_df,
                                   stop_words='english'),
                   NMF(n_components=100, 
                       alpha=.1,
                       l1_ratio=.5,
                       random_state=0),
                   "NMF (100 topics)"),
                  (TfidfVectorizer(max_df=max_df,
                                   min_df=min_df,
                                   stop_words='english'),
                   NMF(n_components=200,
                       alpha=.1,
                       l1_ratio=.5,
                       random_state=0),
                   "NMF (200 topics)"),
                  (TfidfVectorizer(max_df=max_df,
                                   min_df=min_df,
                                   stop_words='english'),
                   NMF(n_components=300,
                       alpha=.1,
                       l1_ratio=.5,
                       random_state=0),
                   "NMF (300 topics)"),
                  (TfidfVectorizer(max_df=max_df,
                                   min_df=min_df,
                                   stop_words='english'),
                   NMF(n_components=400,
                       alpha=.1,
                       l1_ratio=.5,
                       random_state=0),
                   "NMF (400 topics)"),
                  (CountVectorizer(max_df=max_df,
                                   min_df=min_df,
                                   stop_words='english'),
                   LatentDirichletAllocation(n_topics=100,
                                             max_iter=5,
                                             learning_method='online',
                                             batch_size=4096,
                                             learning_decay=0.5,
                                             learning_offset=64,
                                             random_state=0),
                   "Online LDA (100 topics)"),
                  (CountVectorizer(max_df=max_df,
                                   min_df=min_df,
                                   stop_words='english'),
                   LatentDirichletAllocation(n_topics=200,
                                             learning_method='online',
                                             batch_size=4096,
                                             learning_decay=0.5,
                                             learning_offset=64,
                                             random_state=0),
                   "Online LDA (200 topics)"),
                  (CountVectorizer(max_df=max_df,
                                   min_df=min_df,
                                   stop_words='english'),
                   LatentDirichletAllocation(n_topics=300,
                                             learning_method='online',
                                             batch_size=4096,
                                             learning_decay=0.5,
                                             learning_offset=64,
                                             random_state=0),
                   "Online LDA (300 topics)"),
                  (CountVectorizer(max_df=max_df,
                                   min_df=min_df,
                                   stop_words='english'),
                   LatentDirichletAllocation(n_topics=400,
                                             learning_method='online',
                                             batch_size=4096,
                                             learning_decay=0.5,
                                             learning_offset=64,
                                             random_state=0),
                   "Online LDA (400 topics)"))

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

        print "Fold ", i, "train data size =", X_train.shape, "validation data size = ", X_valid.shape, "accuracy = ", accuracy[i]
        
    return accuracy.mean()

def evaluate_vocabulary_sizes(vectorizer, model, name):
    print "Loading dataset"
    dataset = fetch_20newsgroups(subset='all', remove=('headers', 'footers', 'quotes'))

    print "Evaluating ", name
    accuracy = np.zeros(len(vocabulary_sizes))
    for i,nf in enumerate(vocabulary_sizes):
        print "Vocabulary size = ", nf
        vectorizer.set_params(max_features=nf)
        accuracy[i] = evaluate_model(model, vectorizer, dataset.data, dataset.target)

    return accuracy

def main():
    try:
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser(
        description="Evaluates NMF, Online LDA and SMH in document classification and plots the performances")
        parser.set_defaults(fig=False)
        parser.add_argument("-p", "--path_to_save", type=str, default=None,
                            help="file where to save the accuracies")
        parser.add_argument("-c", "--config", type=int, default=0,
                            help="Configuration number to try")
        args = parser.parse_args()
        accuracy = evaluate_vocabulary_sizes(configurations[args.config][0], configurations[args.config][1], configurations[args.config][2])
        if args.path_to_save:
            print "Saving accuracies in", args.path_to_save
            np.savetxt(args.path_to_save, accuracy)
        
    except SystemExit:
        print "for help use --help"
        sys.exit(2)

if __name__ == "__main__":
    main()
