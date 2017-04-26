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
Performs document classification from document representations created from
SMH topics.
"""
import argparse
import sys
from sklearn.feature_extraction.text import CountVectorizer
from cross_validation import evaluate_vocabulary_sizes

def main():
    try:
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser(
        description="Evaluates SMH in document classification and plots the performances")
        parser.add_argument('-s', '--show_flag', action='store_true',
                            help="show figure")
        parser.set_defaults(fig=False)
        parser.add_argument("-p", "--path_to_save", type=str, default=None,
                            help="file where to save the figure")
        p.add_argument("--corpus",default=None, action="store", dest="corpus",
                       help="Corpus file")
        p.add_argument("--weights",default=None, action="store", dest="weights",
                       help="Weights file")

        args = parser.parse_args()
        plot_classification_accuracies(args.show_flag, args.path_to_save)
        
    except SystemExit:
        print "for help use --help"
        sys.exit(2)

if __name__ == "__main__":
    main()
