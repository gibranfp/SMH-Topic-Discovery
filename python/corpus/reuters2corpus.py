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
Takes the Reuters directories and produces a corpus file
"""
import argparse
import sys
import re
import codecs
from collections import Counter
import os
from zipfile import ZipFile
import xml.etree.ElementTree as ET

term_re = re.compile("\w+", re.UNICODE)

def line2tokens(line):
    """
    Converts a text line to a list of tokenized and lemmatized tokens
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
    Reads stopwords from a file (one stopword per line)
    """
    stopwords = []
    for line in codecs.open(filepath, encoding = "utf-8"):
        stopwords.append(line.rstrip())

    return stopwords

def save_vocabulary(vocabulary, vocpath):
    """
    Saves vocabulary into a file in the following format:
    term1 = id1 = number_of_times_term1_occurs number_of_documents_where_term1_occurs
    term2 = id2 = number_of_times_term2_occurs number_of_documents_where_term2_occurs
    --
    termN = id2 = number_of_times_termN_occurs number_of_documents_where_termN_occurs
    """
    termlist = [(t[0], t[1][0], t[1][1], t[1][2]) for t in vocabulary.items()]
    termlist = sorted(termlist, key = lambda t: t[1])
    
    with codecs.open(vocpath, 'w', encoding = "utf-8") as f:
        for t in termlist:
            f.write(t[0] + ' = ' + str(t[1]) + ' = ' + str(t[2]) + ' ' + str(t[3]) + '\n')

def get_zipfiles(dirs):
    """
    Creates a list of zip file names from Reuter's directories
    """
    filepaths = []
    for d in dirs:
        if os.path.isdir(d):
            for f in os.listdir(d):
                ext = os.path.splitext(f)[1]
                if ext == '.zip':
                    filepath = os.path.join(d, f)
                    filepaths.append(filepath)
    return filepaths

def xmlfiles(zipfile):
    """
    Yields XML file names from ZIP file
    """
    with ZipFile(zipfile) as zf:
        for entry in zf.infolist():
            if entry.filename.endswith('.xml'):
                yield ET.fromstring(zf.read(entry.filename))

def reuters_vocabulary(dirs, stopwords):
    """
    Reads Reuters's directories files and creates vocabulary
    """
    corpus_freq = Counter()
    doc_freq = Counter()
    for zf in get_zipfiles(dirs):
        for xf in xmlfiles(zf):
            for child in xf.findall('text'):
                text = []
                for p in child:
                    text.append(p.text.replace('\n',''))
                tokens = line2tokens(' '.join(text))
                terms = [t for t in tokens if t not in stopwords]
                for t in terms:
                    corpus_freq[t] += 1
                
                for t in set(terms):
                    doc_freq[t] += 1

    vocabulary = {}
    for i, entry in enumerate(doc_freq.most_common()):
        vocabulary[entry[0]] = (i, entry[1], corpus_freq[entry[0]])

    return vocabulary

def vectorize_and_save(stopwords, corpuspath, dirs, cutoff):
    """
    Vectorizes documents, stores them in
    a database of lists and saves it to file.
    """
    basename = corpuspath + "/reuters" + str(cutoff)
    with open(basename + ".corpus", 'w') as f:
        print "Constructing vocabulary"
        vocabulary = reuters_vocabulary(dirs, stopwords)
        print "Saving vocabulary to ", basename + ".vocab"
        save_vocabulary(vocabulary, basename + ".vocab")

        print "Vectorizing documents and saving them to", basename + ".corpus"
        for zf in get_zipfiles(dirs):
            for xf in xmlfiles(zf):
                for child in xf.findall('text'):
                    text = []
                    for p in child:
                        text.append(p.text.replace('\n',''))
                    tokens = line2tokens(' '.join(text))
                    terms = [t for t in tokens if t not in stopwords]
                    ids = Counter([vocabulary[t][0] for t in terms
                                   if vocabulary[t][0] < cutoff])
                    bow = [i for i in ids.items()]
                    f.write(str(len(bow)) + ' ')
                    document = [str(i[0]) + ':' + str(i[1]) for i in bow]
                    f.write(' '.join(document))
                    f.write('\n')

def reuters2corpus(reuters, swpath, corpuspath, cutoff = [1000000]):
    """
    Reads Reuters's reference text file and creates a corpus file
    """
    dirs = [reuters + '/' + 'cd1', reuters + '/' + 'cd2']
    if not os.path.isdir(dirs[0]) or not os.path.isdir(dirs[1]):
        print reuters, "is not a valid Reuters directory"
        sys.exit(-1)

    stopwords = load_stopwords(swpath)
    
    Parallel(n_jobs = cpu_count())(delayed(vectorize_and_save)
                                   (stopwords,
                                    corpuspath,
                                    dirs,
                                    c) for c in cutoff)

def main():
    parser = argparse.ArgumentParser("Creates corpus from Reuters directory")
    parser.add_argument("reuters",
                        help="Reuters root directory")
    parser.add_argument("stopwords", 
                        help="Stopwords file")
    parser.add_argument("corpus",
                        help="file where the corpus file is to be saved")
    parser.add_argument("-c", "--cutoff", nargs="*", type=int,
                        default=[10000, 20000, 30000, 40000, 50000,
                                 60000, 70000, 80000, 90000, 100000],
                        help="Vocabulary cutoff")
    args = parser.parse_args()

    reuters2corpus(args.reuters,
                   args.stopwords,
                   args.corpus,
                   cutoff = args.cutoff)
    
if __name__ == "__main__":
    main()
