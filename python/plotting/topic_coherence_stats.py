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
Outputs topic coherence statistics
"""
import argparse
import sys
import numpy as np
import codecs
from plot_coherences import read_coherence_from_file

def display_topic_coherence_stats(filename):
    """
    Reads a topic coherence file and outputs the mean, median, min and max topic coherence
    """
    coherences, average, median = read_coherence_from_file(filename)
    coherences = np.sort(coherences)
    
    print "Min =", np.min(coherences)
    print "Max =", np.max(coherences)
    print "Average =", np.mean(coherences)
    print "Variance =", np.var(coherences)
    print "Median =", np.median(coherences)
    print "Standard Deviation =", np.std(coherences)
    
def main():
    try:
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser(
           description="Outputs topic coherence statistics from a topic coherence file")
        parser.add_argument('topic_coherence_file', type=str)
        
        args = parser.parse_args()
        display_topic_coherence_stats(args.topic_coherence_file)
        
    except SystemExit:
        print "for help use --help"
        sys.exit(2)

if __name__ == "__main__":
    main()
