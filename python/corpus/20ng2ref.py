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
Functions to fetch and store the 20newsgroup dataset in corpus format.
"""
import argparse
import itertools
import sys
import codecs
import re
from collections import Counter
from sklearn.datasets import fetch_20newsgroups
from tokenizer import line2tokens

def newsgroups2ref(dirpath):
    """
    Fetches the 20 newsgroups corpus, vectorized the documents, stores them in
    a database of lists and saves it to file.
    """
    print "Downloading data"
    newsgroups_dataset = fetch_20newsgroups(subset = 'all',
                                            remove = ('headers','footers', 'quotes'))

    refpath = dirpath + "/20newsgroups.ref"
    labelspath = dirpath + "/20newsgroups.labels"
    namespath = dirpath + "/20newsgroups.names"
    
    fref = codecs.open(refpath, 'w', 'utf-8')
    flabels = codecs.open(labelspath, 'w', 'utf-8')
    for doc,label in zip(newsgroups_dataset.data,
                         newsgroups_dataset.target):
        line = doc.replace('\n',' ').replace('\r',' ').replace('\t',' ')
        tokens = line2tokens(line)
        fref.write(' '.join(tokens) + '\n')
        flabels.write(str(label) + '\n')

    fnames = codecs.open(namespath, 'w', 'utf-8')
    for name in newsgroups_dataset.target_names:
        fnames.write(name + '\n')
        
def main():
    """
    Main function
    """
    try:
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser(
            description="Downloads the 20 newsgroups corpus and creates reference and labels files")
        parser.add_argument("dirpath",
                            help="directory where the reference and labels files are to be saved")
        args = parser.parse_args()

        newsgroups2ref(args.dirpath)
            
    except SystemExit:
        print "for help use --help"
        sys.exit(2)

if __name__ == "__main__":
    main()
