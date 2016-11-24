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

def save_vocabulary_to_file(filename, corpus_list, corpus_counter, min_df = 6):
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
            
    less_frequent_ids = [i for i, df in enumerate(docfreq) if df < min_df]
    more_frequent_terms = [[term, corpfreq[id], docfreq[id]] for (term, id) in vocabulary if id not in less_frequent_ids]
    more_frequent_terms = sorted(more_frequent_terms, key=itemgetter(2), reverse=True)

    with open(filename, 'w') as f:
        for i, [term, corpfreq, docfreq] in enumerate(more_frequent_terms):
            line = term + ' = ' + str(i) + ' = ' + str(corpfreq)  + ' ' + str(docfreq) + '\n'
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

def fetch_and_save(dirpath, vocpath = None, min_df = 6, tokenizer = None):
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
        newsgroups_counter = CountVectorizer(stop_words='english',
                                             tokenizer=tokenizer,
                                             vocabulary=vocabulary,
                                             min_df=min_df)
    else:
        newsgroups_counter = CountVectorizer(stop_words='english',
                                             tokenizer=tokenizer,
                                             min_df=min_df)

    # generates csr matrix with the vectors of term frequencies
    newsgroups_mat = newsgroups_counter.fit_transform(newsgroups_dataset.data)
    
    # converts csr matrix to a database of lists
    num_of_docs, vocab_size = newsgroups_mat.shape
    newsgroups_list = [[] for i in xrange(num_of_docs)]
    newsgroups_coo = newsgroups_mat.tocoo()    
    for i,j,v in itertools.izip(newsgroups_coo.row, newsgroups_coo.col, newsgroups_coo.data):
        newsgroups_list[i].append([j,v])

    # saves corpus, vocabulary and indices
    save_corpus_to_file(dirpath + '/20newsgroups.corpus', newsgroups_list)
    save_vocabulary_to_file(dirpath + '/20newsgroups.vocab', newsgroups_list, newsgroups_counter)
    save_idx_to_file(dirpath + '/20newsgroups.idx', newsgroups_dataset)

def main():
    """
    Main function
    """
    try:
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser(
            description="Downloads, preprocess and saves 20 newsgroups corpus")
        parser.add_argument("-m", "--min", type=int, default=6,
                            help="Minimum document frequency for each term")
        parser.add_argument("-d", "--dir", type=str, default='./',
                            help="directory where the corpus is to be saved (default = cwd)")
        parser.add_argument("-v", "--vocabulary", type=str, default=None,
                            help="file where to save the figure")
        parser.add_argument("-t", "--tokenizer", type=bool, default=False,
                            help="Use custom tokenizer")
        args = parser.parse_args()

        if args.tokenizer:
            fetch_and_save(args.dir, args.vocabulary, args.min, tokenizer = None)
        else:
            fetch_and_save(args.dir, args.vocabulary, args.min, tokenizer = line2terms)
            
            
    except SystemExit:
        print "for help use --help"
        sys.exit(2)

if __name__ == "__main__":
    main()
