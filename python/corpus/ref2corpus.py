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
Takes reference file produced by wiki2ref, reuters2ref or 20newsgroups2ref
and generates a corpus file
"""
import argparse
import re
import codecs
import os
from collections import Counter
from string import digits

term_re = re.compile("\w+", re.UNICODE)

def load_stopwords(filepath):
    """
    Reads stopwords from a file (one stopword per line)
    """
    stopwords = []
    for line in codecs.open(filepath, encoding = "utf-8"):
        stopwords.append(line.rstrip())

    return stopwords

def save_vocabulary(vocabulary, vocpath, cutoff = 10000):
    """
    Saves vocabulary in a file
    """
    termlist = [(t[0], t[1][0], t[1][1], t[1][2])
                for t in vocabulary.items()
                if t[1][0] < cutoff]
    termlist = sorted(termlist, key = lambda t: t[1])
    
    with codecs.open(vocpath, 'w', encoding = "utf-8") as f:
        for t in termlist:
            f.write(t[0] + ' = ' + str(t[1]) +
                    ' = ' + str(t[2]) + ' ' + str(t[3]) + '\n')

def ref_vocabulary(wikiref, stopwords):
    """
    Reads reference produced by wiki2ref, reuters2ref or 20newsgroups2ref
    and generates a vocabulary
    """
    corpus_freq = Counter()
    doc_freq = Counter()
    for line in codecs.open(wikiref, encoding = "utf-8"):
        line = re.sub(r'\d+', '', line)
        terms = [t for t in term_re.findall(line)
                 if t not in stopwords]
        
        for t in terms:
            corpus_freq[t] += 1

        for t in set(terms):
            doc_freq[t] += 1

    vocabulary = {}
    for i, entry in enumerate(corpus_freq.most_common()):
        vocabulary[entry[0]] = (i, entry[1], doc_freq[entry[0]])

    return vocabulary

def ref2corpus(refpath, swpath, dirpath, cutoff = 10000, min_doc_terms = 1):
    """
    Reads reference file produced by wiki2ref, reuters2ref or 20newsgroups2ref
    and generates a corpus file
    """
    basename = os.path.basename(refpath).rstrip('.ref')
    corpuspath = dirpath + '/' + basename + str(cutoff) + '.corpus'
    vocpath = dirpath + '/' + basename + str(cutoff) + '.vocab'
    
    stopwords = load_stopwords(swpath)
    with open(corpuspath, 'w') as f:
        print "Constructing vocabulary"
        vocabulary = ref_vocabulary(refpath, stopwords)
        print "Saving vocabulary of size", str(cutoff), "to", vocpath
        save_vocabulary(vocabulary, vocpath, cutoff = cutoff)   

        print "Computing document vectors and saving them to", corpuspath
        for line in codecs.open(refpath, encoding = "utf-8"):
            line = re.sub(r'\d+', '', line)
            ids = Counter([vocabulary[t][0] for t in term_re.findall(line)
                           if t not in stopwords
                           and vocabulary[t][0] < cutoff])
            if sum(ids.itervalues()) >= min_doc_terms:
                bow = [i for i in sorted(ids.items())]
                f.write(str(len(bow)) + ' ')
                document = [str(t[0]) + ':' + str(t[1]) for t in bow]
                f.write(' '.join(document))
                f.write('\n')
            else:
                f.write('0\n')
    
def main():
    parser = argparse.ArgumentParser("Generates a corpus from a reference file")
    parser.add_argument("ref",
                        help = "Reference file")
    parser.add_argument("stopwords", 
                        help = "Stopwords file")
    parser.add_argument("dirpath",
                        help = "Directory where to save corpus and vocabulary")
    parser.add_argument("-c", "--cutoff", type = int, default = 10000,
                        help = "Vocabulary size")
    parser.add_argument("-m", "--min_doc_terms", type = int, default = 100,
                        help = "Minimum number of terms in a document to be considered")
    args = parser.parse_args()
    
    ref2corpus(args.ref,
               args.stopwords,
               args.dirpath,
               cutoff = args.cutoff,
               min_doc_terms = args.min_doc_terms)
    
if __name__ == "__main__":
    main()
