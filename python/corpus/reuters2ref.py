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
from tokenizer import line2tokens

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

def get_xmlfiles(zipfile):
    """
    Yields XML file names from ZIP file
    """
    with ZipFile(zipfile) as zf:
        for entry in zf.infolist():
            if entry.filename.endswith('.xml'):
                yield ET.fromstring(zf.read(entry.filename)), entry.filename

def get_labels(xmlfile):
    """
    Gets labels from XML file
    """
    labels = []
    metadata = xmlfile.find('metadata')
    for codes in metadata.findall('codes'):
        class_attr = codes.get('class')
        if class_attr == 'bip:topics:1.0':
            for c in codes.findall('code'):
                labels.append(c.get('code'))

    return ' '.join(labels)

def get_text(xmlfile):
    """
    Gets text from XML file
    """
    text = []
    for p in xmlfile.find('text'):
        text.append(p.text.replace('\n',''))
    tokens = line2tokens(' '.join(text))

    return ' '.join(tokens)

def reuters2ref(reuters, dirpath):
    """
    Creates Reuters's reference text file from Reuters corpus
    """
    dirs = [reuters + '/' + 'cd1', reuters + '/' + 'cd2']
    if not os.path.isdir(dirs[0]) or not os.path.isdir(dirs[1]):
        print reuters, "is not a valid Reuters directory"
        sys.exit(-1)

    refpath = dirpath + "/reuters.ref.txt"
    labelspath = dirpath + "/reuters.labels.txt"
    filenamepath = dirpath + "/reuters.filenames.txt"
    
    fref = codecs.open(refpath, 'w', 'utf-8')
    flabels = codecs.open(labelspath, 'w', 'utf-8')
    ffnames = codecs.open(filenamepath, 'w', 'utf-8')
    for zipfile in get_zipfiles(dirs):
        for xmlfile, xmlname in get_xmlfiles(zipfile):
            fref.write(get_text(xmlfile))
            fref.write('\n')
                
            flabels.write(get_labels(xmlfile))
            flabels.write('\n')

            ffnames.write(zipfile + ' ' + xmlname)
            ffnames.write('\n')

    fref.close()
    flabels.close()
    ffnames.close()
    
def main():
    parser = argparse.ArgumentParser("Creates corpus from Reuters directory")
    parser.add_argument("reuters",
                        help="Reuters root directory")
    parser.add_argument("dirpath",
                        help="Directory where the reference and labels file are to be saved")
    args = parser.parse_args()

    reuters2ref(args.reuters, args.dirpath)
    
if __name__ == "__main__":
    main()
