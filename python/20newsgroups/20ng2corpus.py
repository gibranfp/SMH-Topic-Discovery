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
Functions to fetch and store the 20newsgroup dataset in corpus format.
"""
import argparse
import itertools
import sys
from operator import itemgetter
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
    vocabulary = sorted(corpus_counter.vocabulary_.items(), key=itemgetter(1))
    docfreq = [0] * len(vocabulary)
    corpfreq = [0] * len(vocabulary)
    for l in corpus_list:
        for id,freq in l:
            docfreq[id] += 1
            corpfreq[id] += freq

    with open(filename, 'w') as f:
        for (word, id) in vocabulary:
            line = word + ' = ' + str(id) + ' = ' + str(corpfreq[id])  + ' ' + str(docfreq[id]) + '\n'
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

def load_vocabulary(vocpath):
    """
    Loads vocabulary from a file
    """
    with open(vocpath, 'r') as f:
        vocabulary = f.read().splitlines()

    return vocabulary

def fetch_and_save(dirpath, vocpath):
    """
    Fetches the 20 newsgroups corpus, vectorized the documents, stores them in
    a database of lists and saves it to file.
    """
    # Loading data
    newsgroups_dataset = fetch_20newsgroups(subset='all',
                                            remove=('headers','footers', 'quotes'),
                                            random_state=123)

    # uses a predefined vocabulary list if available
    if vocpath:
        vocabulary = load_vocabulary(vocpath)
        newsgroups_counter = CountVectorizer(vocabulary=vocabulary, max_df=0.95, min_df=5)
    else:
        newsgroups_counter = CountVectorizer(stop_words='english', max_df=0.95, min_df=5)

    # generates csr matrix with the vectors of term frequencies
    newsgroups_mat = newsgroups_counter.fit_transform(newsgroups_dataset.data)
    
    # converts csr matrix to a database of lists
    num_of_docs, vocab_size = newsgroups_mat.shape
    newsgroups_list = [[] for i in xrange(num_of_docs)]
    newsgroups_coo = newsgroups_mat.tocoo()    
    for i,j,v in itertools.izip(newsgroups_coo.row, newsgroups_coo.col, newsgroups_coo.data):
        newsgroups_list[i].append([j,v])

    # saves corpus, vocabulary and indices
    save_corpus_to_file(dirpath + '/newsgroups.corpus', newsgroups_list)
    save_vocabulary_to_file(dirpath + '/newsgroups.voca', newsgroups_list, newsgroups_counter)
    save_idx_to_file(dirpath + '/newsgroups.idx', newsgroups_dataset)

def main():
    """
    Main function
    """
    try:
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser(
            description="Downloads, preprocess and saves 20 newsgroups corpus")
        parser.add_argument("-d", "--dir", type=str, default='./',
                            help="directory where the corpus is to be saved (default = cwd)")
        parser.add_argument("-v", "--vocabulary", type=str, default=None,
                            help="file where to save the figure")
        args = parser.parse_args()
        fetch_and_save(args.dir, args.vocabulary)
            
    except SystemExit:
        print "for help use --help"
        sys.exit(2)

if __name__ == "__main__":
    main()
