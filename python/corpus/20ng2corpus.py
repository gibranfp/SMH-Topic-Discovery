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
import codecs
import re
from collections import Counter
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals.joblib import Parallel, delayed, cpu_count
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

term_re = re.compile("\w+", re.UNICODE)

def line2tokens(line):
    """
    Converts original text line to tokenized and lemmatized tokens
    """
    terms = [t.lower() for t in term_re.findall(line)]
    tagged = pos_tag(word_tokenize(' '.join(terms)))
    lemmatizer = WordNetLemmatizer()
    tokens = []
    for w,t in tagged:
        tokens.append(lemmatizer.lemmatize(w, pos=morphy_tag.get(t, NOUN)))

    return tokens

def load_stopwords(filepath):
    """
    Reads stopwords from a file (one word per line)
    """
    stopwords = []
    for line in codecs.open(filepath, encoding = "utf-8"):
        stopwords.append(line.rstrip())

    return stopwords

def save_corpus(filename, corpus_list):
    """
    Saves corpus to a file in the following format:
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

def save_vocabulary(vocpath, corpus_list, corpus_counter):
    """
    Saves vocabulary into a file in the following format:
    term1 = id1 = number_of_times_term1_occurs number_of_documents_where_term1_occurs
    term2 = id2 = number_of_times_term2_occurs number_of_documents_where_term2_occurs
    --
    termN = id2 = number_of_times_termN_occurs number_of_documents_where_termN_occurs
    """
    corpus_freq = Counter()
    doc_freq = Counter()
    for l in corpus_list:
        for id,freq in l:
            corpus_freq[id] += freq
            doc_freq[id] += 1

    with open(vocpath, 'w') as f:
        vocabulary = corpus_counter.get_feature_names()
        for entry in doc_freq.most_common():
            line = vocabulary[entry[0]] + ' = ' + \
                   str(entry[0]) + ' = ' + \
                   str(corpus_freq[entry[0]])  + ' ' + \
                   str(entry[1]) + '\n'
            f.write(line.encode('utf8'))

def vectorize_and_save(stopwords, corpuspath, data, cutoff, tokenizer):
    """
    Vectorizes documents, stores them in
    a database of lists and saves it to file.
    """
    print "Vectorizing documents with cutoff =", cutoff
    newsgroups_counter = CountVectorizer(max_features = cutoff,
                                         stop_words=stopwords,
                                         tokenizer=tokenizer)    
    newsgroups_mat = newsgroups_counter.fit_transform(data)
    
    num_of_docs, vocab_size = newsgroups_mat.shape
    newsgroups_list = [[] for i in xrange(num_of_docs)]
    newsgroups_coo = newsgroups_mat.tocoo()
    for i,j,v in itertools.izip(newsgroups_coo.row,
                                newsgroups_coo.col,
                                newsgroups_coo.data):
        newsgroups_list[i].append([j,v])
        
    basename = corpuspath + "/20newsgroups"+ str(cutoff)
        
    print "Saving corpus in", basename + ".corpus"
    save_corpus(basename + ".corpus", newsgroups_list)
    
    print "Saving vocabulary in", basename + ".vocab"
    save_vocabulary(basename + ".vocab", newsgroups_list, newsgroups_counter)

def ng2corpus(swpath, corpuspath, cutoff = [1000], tokenizer = line2tokens):
    """
    Fetches the 20 newsgroups corpus, vectorized the documents, stores them in
    a database of lists and saves it to file.
    """

    print "Downloading data"
    newsgroups_dataset = fetch_20newsgroups(subset='all',
                                            remove=('headers','footers', 'quotes'),
                                            random_state=123)
    stopwords = load_stopwords(swpath)

    Parallel(n_jobs = cpu_count())(delayed(vectorize_and_save)
                                   (stopwords,
                                    corpuspath,
                                    newsgroups_dataset.data,
                                    c,
                                    tokenizer) for c in cutoff)
    
def main():
    """
    Main function
    """
    try:
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser(
            description="Downloads, preprocess and saves 20 newsgroups corpus")
        parser.add_argument("stopwords", 
                            help="Stopwords file")
        parser.add_argument("corpus",
                            help="directory where the corpus files are to be saved")
        parser.add_argument("-c", "--cutoff", nargs="*", type=int,
                            default=[1000, 2000, 3000, 4000, 5000,
                                     6000, 7000, 8000, 9000, 10000],
                            help="Vocabulary cutoff")
        parser.add_argument("-t", "--tokenizer", type=bool, default=True,
                            help="Do not use custom tokenizer")
        args = parser.parse_args()

        if args.tokenizer:
            ng2corpus(args.stopwords,
                      args.corpus,
                      cutoff = args.cutoff,
                      tokenizer = line2tokens)
        else:
            ng2corpus(args.stopwords,
                      args.corpus,
                      cutoff = args.cutoff,
                      tokenizer = None)
            
    except SystemExit:
        print "for help use --help"
        sys.exit(2)

if __name__ == "__main__":
    main()
