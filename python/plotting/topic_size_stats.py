
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
Displays topic size statistics
"""
import argparse
import sys
import numpy as np
import codecs

def get_topic_size_stats(filename):
    """
    Reads a topic file and outputs the topic size mean, median, min, max, variance
    and standard deviation 
    """
    topics = []
    with codecs.open(filename, 'r', 'utf-8') as f:
        content = f.readlines()
        for l in content:
            words = l.split()
            topics.append(words)

    sizes = np.sort([len(t) for t in topics])

    print "Min Size =", np.min(sizes)
    print "Max Size =", np.max(sizes)
    print "Average Size =", np.mean(sizes)
    print "Variance =", np.var(sizes)
    print "Median Size =", np.median(sizes)
    print "Standard Deviation =", np.std(sizes)
    
def main():
    try:
        parser = argparse.ArgumentParser()
        parser = argparse.ArgumentParser(
           description="Outputs topic size statistics from a topic file")
        parser.add_argument('topic_file', type=str)
        
        args = parser.parse_args()
        get_topic_size_stats(args.topic_file)
        
    except SystemExit:
        print "for help use --help"
        sys.exit(2)

if __name__ == "__main__":
    main()
