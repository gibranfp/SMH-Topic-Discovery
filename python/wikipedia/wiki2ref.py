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
Takes text file produced by wiki2text and processes it to produce a file with 1
document per line
"""
import argparse
import sys
import os
import os.path
import random
import re
import codecs
from collections import Counter
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from nltk.corpus.reader.wordnet import NOUN, VERB, ADV, ADJ

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
    tokens = word_tokenize(line)
    tagged = pos_tag(tokens)
    lemmatizer = WordNetLemmatizer()
    terms = []
    for w,t in tagged:
         terms.append(lemmatizer.lemmatize(w, pos=morphy_tag.get(t, NOUN)))

    return ' '.join(terms)
    
def wiki2ref(wikitext, reference):
    """
    Reads Wikipedia's text file produced by wiki2text, processes it and
    stores it in a single line per document format
    """
    re_title = re.compile('^= ')
    with codecs.open(reference, 'w', 'utf-8') as f:
        for i, line in enumerate(codecs.open(wikitext, encoding = "utf-8")):
            if re_title.match(line):
                if i > 0:
                    f.write('\n')
            else:
                terms = line2terms(re.sub("[=\n]", "", line).lower())
                f.write(terms)
            
    
def main():
    parser = argparse.ArgumentParser("Creates reference corpus")
    parser.add_argument("wikitext",
            help="Wikipedia text file produced by wiki2text")
    parser.add_argument("reference",
            help="File where the reference file is to be saved")
    args = parser.parse_args()

    wiki2ref(args.wikitext, args.reference)
    
    
if __name__ == "__main__":
    main()

