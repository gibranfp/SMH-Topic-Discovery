#!/usr/bin/env python
# -*- coding: utf-8
#
# Gibran Fuentes Pineda <gibranfp@turing.iimas.unam.mx>
# IIMAS, UNAM
# 2015
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
Functions to fetch and store the 20newsgroup dataset in corpus format.
"""
import itertools
import sys
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer

def save_corpus_to_file(filename, corpus_list):
    """
    Saves corpus into a file in the following format:
    size_of_doc1 doc1_termid[1]:freq doc1_termid[2]:freq ... doc1_termid[size_of_doc1]:freq
    size_of_doc2 doc2_termid[1]:freq doc2_termid[2]:freq ... doc2_termid[size_of_doc2]:freq
    ...
    size_of_docN docN_termid[1]:freq docN_termid[2]:freq ... docN_termid[size_of_docN]:freq
    """
    with open(filename, 'w') as f:
        for i in corpus_list:
            bow = ''.join([str(i[j][0]) + ':' + str(i[j][1]) + ' ' for j in range(len(i))]) + '\n'
            line = str(len(i)) + ' ' + bow
            f.write(line)
    f.close()

def save_vocabulary_to_file(filename, corpus_list, corpus_counter):
    """
    Saves vocabulary into a file in the following format:
    term1 = id1 = number_of_times_term1_occurs number_of_documents_where_term1_occurs
    term2 = id2 = number_of_times_term2_occurs number_of_documents_where_term2_occurs
    --
    termN = id2 = number_of_times_termN_occurs number_of_documents_where_termN_occurs
    """
    words = corpus_counter.vocabulary_.keys()
    ids = corpus_counter.vocabulary_.values()
    docfreq = [0] * len(words)
    corpfreq = [0] * len(words)
    for i in range(len(corpus_list)):
        for id,freq in corpus_list[i]:
            docfreq[id] += 1
            corpfreq[id] += freq

    ids, corpfreq, docfreq, words = zip(*sorted(zip(ids, corpfreq, docfreq, words)))
    with open(filename, 'w') as f:
        for i in range(len(words)):
            line = words[i] + ' = ' + str(ids[i]) + ' = ' + str(corpfreq[i])  + ' ' + str(docfreq[i]) + '\n'
            f.write(line.encode('utf8'))
    f.close()

def save_idx_to_file(idxfile, newsgroup):
    """
    Saves filenames into a file.
    """
    with open(idxfile, 'w') as f:
        for path in newsgroup.filenames:
            f.write(path + '\n')
    f.close()

def main(dirpath):
    train_newsgroups = fetch_20newsgroups(subset='train')
    train_counter = CountVectorizer(stop_words='english',min_df=5)
    train_mat = train_counter.fit_transform(train_newsgroups.data)
    train_mat.sort_indices()

    num_of_docs, vocab_size = train_mat.shape
    train_list = [[] for i in xrange(num_of_docs)]
    train_coo = train_mat.tocoo()    
    for i,j,v in itertools.izip(train_coo.row, train_coo.col, train_coo.data):
        train_list[i].append([j,v])

    save_corpus_to_file(dirpath + '/20ng.train.corpus', train_list)
    save_vocabulary_to_file(dirpath + '/20ng.train.voca', train_list,train_counter)
    save_idx_to_file(dirpath + '/20ng.train.idx', train_newsgroups)

if __name__ == "__main__":
    main(sys.argv[1])
