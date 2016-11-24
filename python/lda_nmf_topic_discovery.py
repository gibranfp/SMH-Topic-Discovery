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
Performs topic discovery using NMF and Online LDA
"""
import argparse
import sys
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from scipy.sparse import csr_matrix
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Topic discovery configurations to evaluate
configurations = ((NMF(n_components=100, 
                       alpha=.1,
                       l1_ratio=.5,
                       random_state=0),
                   "NMF (100 topics)"),
                   (NMF(n_components=200,
                        alpha=.1,
                        l1_ratio=.5,
                        random_state=0),
                    "NMF (200 topics)"),
                  (NMF(n_components=300,
                       alpha=.1,
                       l1_ratio=.5,
                       random_state=0),
                   "NMF (300 topics)"),
                  (NMF(n_components=400,
                       alpha=.1,
                       l1_ratio=.5,
                       random_state=0),
                   "NMF (400 topics)"),
                  (LatentDirichletAllocation(n_topics=100,
                                             max_iter=5,
                                             learning_method='online',
                                             batch_size=4096,
                                             learning_decay=0.5,
                                             learning_offset=64,
                                             random_state=0),
                   "Online LDA (100 topics)"),
                  (LatentDirichletAllocation(n_topics=200,
                                             learning_method='online',
                                             batch_size=4096,
                                             learning_decay=0.5,
                                             learning_offset=64,
                                             random_state=0),
                   "Online LDA (200 topics)"),
                  (LatentDirichletAllocation(n_topics=300,
                                             learning_method='online',
                                             batch_size=4096,
                                             learning_decay=0.5,
                                             learning_offset=64,
                                             random_state=0),
                   "Online LDA (300 topics)"),
                  (LatentDirichletAllocation(n_topics=400,
                                             learning_method='online',
                                             batch_size=4096,
                                             learning_decay=0.5,
                                             learning_offset=64,
                                             random_state=0),
                   "Online LDA (400 topics)"))

def load_listdb_as_csr(listdb_file):
    """
    Returns the ListDB structure as a Compressed Sparse Row (CSR) matrix
    """
    with open(listdb_file, 'r') as f:
        content = f.readlines()
        indptr = [0]
        indices = []
        data = []
        for line in content:
            for entry in line.split()[1:]:
                term,value = entry.split(':')
                indices.append(int(term))
                data.append(int(value))
            indptr.append(len(indices))

    return csr_matrix((data, indices, indptr), dtype=np.uint32)

def save_topics(filename, coherence, model):
    print "Saving topics to",filename
    with open(filename ,'w') as f:
        print "Total tópicos", len(coherence)
        for c,t in coherence:
            t = model.ldb[t]
            ws = [voca[w.item] for w in t]
            print >> f, c, ", ".join(ws)

def pmi(t_i, t_j, ifs, vocabulary_mapper):
    p_i = ifs[t_i,:].sum()
    p_i = ifs[t_i,:].sum()
    for d in ifs[t_i,:]:
        
    
def compute_pmi_score(topics, corpus, vocabulary_mapper = None):
    results = []
    sorted_words = np.argsort(topics)

    for i,row in enumerate(topics):
        topic_coherence = 0.0
        for j in range(top_terms):
            for k in range(j + 1, top_terms):
                pmi(j, k, corpus, vocabulary_mapper)
    
def discover_topics(model,
                    name,
                    train_corpus,
                    train_vocab,
                    test_corpus,
                    test_vocab,
                    modelfile,
                    topicfile,
                    timefile):
    """
    Discovers topics and evaluates model using topic coherence
    """
    print "Loading train corpus"
    train_documents = load_listdb_as_csr(train_corpus)

    print "Discovering topics using", name
    model.fit(train_documents)

    print "Loading test corpus"
    test_documents = load_listdb_as_csr(test_corpus)

    print "Loading train vocabulary"
    train_vocabulary = utils.i2v(train_vocab)

    print "Mapping train and test vocabularies"
    vocabulary_mapper = utils.t2c(train_vocab, test_vocab)
    
    # print "Calculating coherence on testing..."
    # test_models,test_coherence = coherence(train_models,
    #                                        test_corpus,
    #                                        vocab_mapper,
    #                                        ntop=10,
    #                                        min_coherence = -1)
    # test_coherence = [(c,t) for t,c in test_coherence]
    # test_coherence.sort()
    # test_coherence.reverse()
      
    # print "Saving resulting model to", modelfile
    # train_models.save(filename)

    # save_topics(topicfile, test_coherence, train_models)

def main():
    try:
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser(
        description="Evaluates NMF and Online LDA in topic discovery")
        parser.set_defaults(fig=False)
        parser.add_argument("train_corpus", nargs=1, type=str,
                            help="Train corpus file (database of ID lists)")
        parser.add_argument("train_vocab", nargs=1, type=str,
                            help="Vocabulary file for train corpus")
        parser.add_argument("test_corpus", nargs=1, type=str,
                            help="Test corpus file (database of ID lists)")
        parser.add_argument("test_vocab", nargs=1, type=str,
                            help="Vocabulary file for test corpus")
        parser.add_argument("models", nargs=1, type=str,
                            help="file where to save the models (database of ID lists)")
        parser.add_argument("topics",  nargs=1, type=str,
                            help="file where to save the topics (database of word lists and coherences)")
        parser.add_argument("times",  nargs=1, type=str,
                            help="file where to save the time and memory used")
        parser.add_argument("-c", "--config", type=int, default=0,
                            help="Configuration number to try")
        args = parser.parse_args()
        discover_topics(configurations[args.config][0],
                        configurations[args.config][1],
                        args.train_corpus[0],
                        args.train_vocab[0],
                        args.test_corpus[0],
                        args.test_vocab[0],
                        args.models[0],
                        args.topics[0],
                        args.times[0])
        
    except SystemExit:
        print "for help use --help"
        sys.exit(2)

if __name__ == "__main__":
    main()
