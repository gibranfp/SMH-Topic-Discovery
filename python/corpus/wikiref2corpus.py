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
Takes Wikipedia text file produced by wiki2ref and produces a corpus file
"""
import argparse
import re
import codecs
from collections import Counter


term_re = re.compile("\w+", re.UNICODE)

def load_stopwords(filepath):
    """
    Reads stopwords from a file (one stopword per line)
    """
    stopwords = []
    for line in codecs.open(filepath, encoding = "utf-8"):
        stopwords.append(line.rstrip())

    return stopwords

def save_vocabulary(vocabulary, vocpath, cutoff):
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

def wikiref_vocabulary(wikiref, stopwords):
    """
    Reads Wikipedia's reference text file and creates vocabulary
    """
    corpus_freq = Counter()
    doc_freq = Counter()
    for line in codecs.open(wikiref, encoding = "utf-8"):
        terms = [t for t in term_re.findall(line)
                 if t not in stopwords]
        for t in terms:
            corpus_freq[t] += 1

        for t in set(terms):
            doc_freq[t] += 1

    vocabulary = {}
    for i, entry in enumerate(doc_freq.most_common()):
        vocabulary[entry[0]] = (i, entry[1], corpus_freq[entry[0]])

    return vocabulary

def wikiref2corpus(wikiref, swpath, corpuspath, vocpath, cutoff = 1000000):
    """
    Reads Wikipedia text file produced by wikie2ref and creates a corpus file
    """
    stopwords = load_stopwords(swpath)
    with open(corpuspath, 'w') as f:
        print "Constructing vocabulary"
        vocabulary = wikiref_vocabulary(wikiref, stopwords)
        print "Saving vocabulary of size ", len(vocabulary), "to", vocpath
        save_vocabulary(vocabulary, vocpath)   

        print "Computing document vectors and saving them to", corpuspath
        for line in codecs.open(wikiref, encoding = "utf-8"):
            ids = Counter([vocabulary[t][0] for t in term_re.findall(line)
                           if t not in stopwords
                           and vocabulary[t][0] < cutoff])
            bow = [i for i in ids.items()]
            f.write(str(len(bow)) + ' ')
            document = [str(t[0]) + ':' + str(t[1]) for t in bow]
            f.write(' '.join(document))
            f.write('\n')
    
def main():
    parser = argparse.ArgumentParser("Creates corpus from Wikipedia text file")
    parser.add_argument("wikiref",
            help="Wikipedia text file produced by wiki2ref")
    parser.add_argument("stopwords", 
                        help="Stopwords file")
    parser.add_argument("corpus",
                        help="File where the corpus file is to be saved")
    parser.add_argument("vocabulary",
                        help="File where the vocabulary file is to be saved")
    parser.add_argument("-c", "--cutoff", type=str, default=1000000,
                        help="Vocabulary cutoff")
    args = parser.parse_args()
    
    wikiref2corpus(args.wikiref,
                   args.stopwords,
                   args.corpus,
                   args.vocabulary,
                   cutoff = args.cutoff)
    
if __name__ == "__main__":
    main()
