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
Takes text file produced by wiki2text and processes it to produce a file with 1
document per line
"""
import argparse
import codecs
import os
from collections import Counter
from tokenizer import line2tokens

def wiki2ref(wiki2text, dirpath):
    """
    Reads Wikipedia's text file produced by wiki2text, processes it and
    stores it in a single line per document format
    """
    title_mark = '= '
    section_mark = '=='
    basename = os.path.basename(wiki2text).rstrip('.txt')

    refpath = dirpath + '/' + basename + '.ref'
    titlespath = dirpath + '/' + basename + '.titles'

    fref = codecs.open(refpath, 'w', 'utf-8') 
    ftitles = codecs.open(titlespath, 'w', 'utf-8')
    for i,line in enumerate(codecs.open(wiki2text, 'r', 'utf-8')):
        line = line.rstrip()
        if line[:2] == title_mark:
            title = line.lstrip('= ').rstrip(' =')
            ftitles.write(title + '\n')
            if i > 0:
                fref.write('\n')
        elif line[:2] != section_mark:
            tokens = line2tokens(line)
            fref.write(' '.join(tokens))
            fref.write(' ')
    fref.close()
    ftitles.close()
                                        
def main():
    parser = argparse.ArgumentParser("Creates reference corpus")
    parser.add_argument("wiki2text",
            help="Wikipedia text file produced by wiki2text")
    parser.add_argument("dirpath",
            help="Directory where the reference and title files are to be saved")
    args = parser.parse_args()

    wiki2ref(args.wiki2text, args.dirpath)
        
if __name__ == "__main__":
    main()
