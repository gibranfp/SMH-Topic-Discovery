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
            if top:
                f.write(' '.join(t[:top]).encode('utf8'))
            else:
                f.write(' '.join(t).encode('utf8'))
            f.write('\n'.encode('utf8'))

def save_time(filepath, total_time):
    """
    Saves time to a file
    """
    with open(filepath, 'w') as f:
        f.write(str(total_time))

def listdb_to_topics(models, vocpath):
    """
    Reads a vocabulary and stores it in a dictionary
    """
    topics = []
    vocabulary = load_vocabulary(vocpath)
    for m in models.ldb:
        terms = []
        for j in m:
            terms.append(vocabulary[j.item])
        topics.append(terms)

    return topics

def array_to_topics(models, vocpath):
    """
    Reads a vocabulary and stores it in a dictionary
    """
    topics = []
    vocabulary = load_vocabulary(vocpath)
    for i,m in enumerate(models):
        terms = []
        for j in m.argsort()[::-1]:
            terms.append(vocabulary[j])
        
        topics.append(terms)

    return topics
