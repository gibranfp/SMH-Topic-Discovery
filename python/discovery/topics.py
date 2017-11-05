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
Functions to load and save models (lists of IDs) as topics (lists of terms)
"""
import numpy as np
import codecs
from math import log

def load_vocabulary(vocpath):
    """
    Reads a vocabulary and stores it in a dictionary
    """
    vocabulary = {}
    docfreq = {}
    with codecs.open(vocpath, 'r', 'utf-8') as f:
        content = f.readlines()
        for line in content:
            tokens = line.split(' = ')
            freqs = tokens[2].split()
            docfreq[int(tokens[1])] = float(freqs[1])
            vocabulary[int(tokens[1])] = tokens[0]

    return vocabulary, docfreq

def save_topics(filepath, topics, top = 10):
    """
    Saves topics to a file
    """
    with codecs.open(filepath, 'w', 'utf-8') as f:
        for t in topics:
            if top:
                f.write(' '.join(t[:top]))
            else:
                f.write(' '.join(t))
            f.write('\n')

def save_time(filepath, total_time):
    """
    Saves time to a file
    """
    with codecs.open(filepath, 'w', 'utf-8') as f:
        f.write(str(total_time))

def get_models_docfreq(models, vocabulary, docfreq):
    """
    Loads models from a database of lists, finds the document frequencies of their terms and saves them as lists of terms
    """
    topics = []
    models_docfreq = []
    for m in models.ldb:
        mdf = [(docfreq[t.item], t.item) for t in m]
        models_docfreq.append(mdf)
        topics.append([vocabulary[t[1]] for t in mdf])
        
    return models_docfreq, topics

def sort_topics(models, topics, top = 10):
    """
    Sorts topics based on scores
    """
    topic_scores = np.zeros(len(models))
    for i,m in enumerate(models):
        if top:
            if len(m) >= top:
                topic_scores[i] = np.mean([t[0] for t in m[:top]])
        else:
            topic_scores[i] = np.mean([t[0] for t in m])
            
    topic_indices = np.argsort(topic_scores)[::-1]
    sorted_topics = [topics[i] for i in topic_indices if len(topics[i]) >= top]

    return sorted_topics
    
def listdb_to_topics(models, vocabulary):
    """
    Reads a vocabulary and stores it in a dictionary
    """
    topics = []
    for m in models.ldb:
        terms = []
        for j in m:
            terms.append(vocabulary[j.item])
        topics.append(terms)

    return topics

def array_to_topics(models, vocabulary):
    """
    Reads a vocabulary and stores it in a dictionary
    """
    topics = []
    for m in models:
        terms = []
        for j in m.argsort()[::-1]:
            terms.append(vocabulary[j])
        
        topics.append(terms)

    return topics
