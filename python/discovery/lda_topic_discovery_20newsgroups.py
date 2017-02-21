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
Performs topic discovery using Online LDA in the 20 newsgroups dataset
"""
import argparse
import sys
import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.datasets import fetch_20newsgroups
from scipy.sparse import csr_matrix
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time
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

# vocabulary sizes to evaluate
vocabulary_sizes = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]

# Topic discovery configurations to evaluate
configurations = ((CountVectorizer(stop_words='english'),
                   LatentDirichletAllocation(n_topics=100,
                                             max_iter=5,
                                             learning_method='online',
                                             batch_size=4096,
                                             learning_decay=0.5,
                                             learning_offset=64,
                                             random_state=0),
                   "lda100"),
                  (CountVectorizer(stop_words='english'),
                   LatentDirichletAllocation(n_topics=200,
                                             learning_method='online',
                                             batch_size=4096,
                                             learning_decay=0.5,
                                             learning_offset=64,
                                             random_state=0,
                                             n_jobs = 1),
                   "lda200"),
                  (CountVectorizer(stop_words='english'),
                   LatentDirichletAllocation(n_topics=300,
                                             learning_method='online',
                                             batch_size=4096,
                                             learning_decay=0.5,
                                             learning_offset=64,
                                             random_state=0),
                   "lda300"),
                  (CountVectorizer(stop_words='english'),
                   LatentDirichletAllocation(n_topics=400,
                                             learning_method='online',
                                             batch_size=4096,
                                             learning_decay=0.5,
                                             learning_offset=64,
                                             random_state=0),
                   "lda400"))

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

def models_to_topics(models, vocabulary):
    """
    Reads a vocabulary and stores it in a dictionary
    """
    topics = []
    for i,m in enumerate(models):
        terms = []
        for j in m.argsort()[::-1]:
            terms.append(vocabulary[j])
        
        topics.append(terms)

    return topics
    
def discover_topics(vectorizer,
                    model,
                    name,
                    savedir,
                    top_terms_numbers = [10]):
    """
    Discovers topics and evaluates model using topic coherence
    """
    print "Loading dataset"
    dataset = fetch_20newsgroups(subset='all', remove=('headers', 'footers', 'quotes'))

    for i,nf in enumerate(vocabulary_sizes):
        print "Vocabulary size = ", nf
        vectorizer.set_params(max_features=nf)
        corpus = vectorizer.fit_transform(dataset.data)
        
        print "Discovering topics using", name
        start_time = time.time()
        model.fit(corpus)
        end_time = time.time()
        total_time = end_time - start_time
              
        print "Generating topics (lists of terms) from models"
        topics = models_to_topics(model.components_, vectorizer.get_feature_names())

        modelfile = savedir + '/' + name + '_' + '20newsgroups' + str(nf) + '.models'
        print "Saving resulting models to", modelfile
        np.savetxt(modelfile, model.components_)

        # save topics with different top terms numbers
        for top in top_terms_numbers:
            topicfile = savedir + '/' + name + '_' + '20newsgroups' + str(nf) + '_top' + str(top) + '.topics'
            print "Saving the top", top, " terms of the topic to", topicfile
            save_topics(topicfile, topics, top = top)

        timefile = savedir + '/' + name + '_' + '20newsgroups' + str(nf) + '.time'
        print "Saving times to", timefile
        save_time(timefile, total_time)

def main():
    try:
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser(
        description="Evaluates Online LDA in topic discovery from the 20 newsgroups dataset")
        parser.set_defaults(fig=False)
        parser.add_argument("dir",  nargs=1, type=str,
                            help="Directory where the models, topics and times are to be saved")
        parser.add_argument("-t", "--top", type=int, default=[5, 10, 15, 20], nargs='*',
                            help="Configuration number to try")
        parser.add_argument("-c", "--config", type=int, default=0,
                            help="Configuration number to try")
        args = parser.parse_args()
        discover_topics(configurations[args.config][0],
                        configurations[args.config][1],
                        configurations[args.config][2],
                        args.dir[0],
                        args.top)
        
    except SystemExit:
        print "for help use --help"
        sys.exit(2)

if __name__ == "__main__":
    main()
