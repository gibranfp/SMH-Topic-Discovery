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
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from scipy.sparse import csr_matrix
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time

# Topic discovery configurations to evaluate
configurations = ((NMF(n_components=100, 
                       alpha=.1,
                       l1_ratio=.5,
                       random_state=0),
                   "nmf100"),
                  (NMF(n_components=200,
                       alpha=.1,
                       l1_ratio=.5,
                       random_state=0),
                   "nmf200"),
                  (NMF(n_components=300,
                       alpha=.1,
                       l1_ratio=.5,
                       random_state=0),
                   "nmf300"),
                  (NMF(n_components=400,
                       alpha=.1,
                       l1_ratio=.5,
                       random_state=0),
                   "nmf400"),
                  (LatentDirichletAllocation(n_topics=100,
                                             max_iter=5,
                                             learning_method='online',
                                             batch_size=4096,
                                             learning_decay=0.5,
                                             learning_offset=64,
                                             random_state=0),
                   "lda100"),
                  (LatentDirichletAllocation(n_topics=200,
                                             learning_method='online',
                                             batch_size=4096,
                                             learning_decay=0.5,
                                             learning_offset=64,
                                             random_state=0),
                   "lda200"),
                  (LatentDirichletAllocation(n_topics=300,
                                             learning_method='online',
                                             batch_size=4096,
                                             learning_decay=0.5,
                                             learning_offset=64,
                                             random_state=0),
                   "lda300"),
                  (LatentDirichletAllocation(n_topics=400,
                                             learning_method='online',
                                             batch_size=4096,
                                             learning_decay=0.5,
                                             learning_offset=64,
                                             random_state=0),
                  "lda400"))

def load_vocabulary(vocpath):
    """
    Reads a vocabulary and stores it in a dictionary
    """
    vocabulary = {}
    with open(vocpath, 'r') as f:
        content = f.readlines()
        for line in content:
            tokens = line.split(' = ')
            vocabulary[int(tokens[1])] = tokens[0]

    return vocabulary

def save_topics(filepath, topics, top = 10):
    """
    Saves topics to a file
    """
    with open(filepath, 'w') as f:
        for t in topics:
            f.write(' '.join(t[:top]).encode('utf8'))
            f.write('\n'.encode('utf8'))

def save_time(filepath, total_time):
    """
    Saves time to a file
    """
    with open(filepath, 'w') as f:
        f.write(str(total_time))

def models_to_topics(models, vocpath):
    """
    Reads a vocabulary and stores it in a dictionary
    """
    topics = []
    vocabulary = load_vocabulary(vocpath)
    for i,m in enumerate(models):
        terms = []
        for j in m.argsort():
            terms.append(vocabulary[j])
        
        topics.append(terms)

    return topics
    
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

def discover_topics(model,
                    name,
                    corpuspath,
                    vocpath,
                    savedir,
                    top_terms_numbers = [10]):
    """
    Discovers topics and evaluates model using topic coherence
    """
    print "Loading train corpus"
    documents = load_listdb_as_csr(corpuspath)

    print "Discovering topics using", name
    start_time = time.time()
    model.fit(documents)
    end_time = time.time()
    total_time = end_time - start_time
              
    print "Generating topics (lists of terms) from models"
    topics = models_to_topics(model.components_, vocpath)

    corpusname = os.path.splitext(os.path.basename(corpuspath))[0]
    modelfile = savedir + '/' + name + '_' + corpusname + '.models'
    print "Saving resulting models to", modelfile
    np.savetxt(modelfile, model.components_)

    # save topics with different top terms numbers
    for top in top_terms_numbers:
        topicfile = savedir + '/' + name + '_' + corpusname + '_top' + str(top) + '.topics'
        print "Saving the top", top, " terms of the topic to", topicfile
        save_topics(topicfile, topics, top = top)

    timefile = savedir + '/' + name + '_' + corpusname + '.time'
    print "Saving times to", timefile
    save_time(timefile, total_time)

def main():
    try:
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser(
        description="Evaluates NMF and Online LDA in topic discovery")
        parser.set_defaults(fig=False)
        parser.add_argument("corpus", nargs=1, type=str,
                            help="Corpus file (database of ID lists)")
        parser.add_argument("vocabulary", nargs=1, type=str,
                            help="Vocabulary file for corpus")
        parser.add_argument("dir",  nargs=1, type=str,
                            help="Directory where the models, topics and times are to be saved")
        parser.add_argument("-t", "--top", type=int, default=[5, 10, 15, 20], nargs='*',
                            help="Configuration number to try")
        parser.add_argument("-c", "--config", type=int, default=0,
                            help="Configuration number to try")
        args = parser.parse_args()
        discover_topics(configurations[args.config][0],
                        configurations[args.config][1],
                        args.corpus[0],
                        args.vocabulary[0],
                        args.dir[0],
                        args.top)
        
    except SystemExit:
        print "for help use --help"
        sys.exit(2)

if __name__ == "__main__":
    main()
