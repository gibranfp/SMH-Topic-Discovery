#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Sampled MinHash demo with images
# ----------------------------------------------------------------------
# Gibran Fuentes-Pineda, Ivan V. Meza
# 2015/IIMAS, México
# ----------------------------------------------------------------------

import numpy as np
import pylab as pl

from smh import smh

# MAIN program
if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser("Mines")
    p.add_argument("-r","--tuple_size",default=4,type=int,
        action="store", dest='r',help="Size of the tupple")
    p.add_argument("-l","--number_tuples",default=10,type=int,
        action="store", dest='l',help="Number of the tupple")
    p.add_argument("--output",default=None,type=str,
        action="store", dest='output',help="Filename to save mined model")
    p.add_argument("--min",default=1000,type=int,
        action="store", dest='min',help="Minimum number of items")
    p.add_argument("--show",default=False,
            action="store_true", dest='show',help="Show bases found")
    p.add_argument("ifs",default=None,
        action="store", help="Inverted file structure of documents")

    opts = p.parse_args()

    print "Loading file ifs:",opts.ifs
    s=smh.smh_load(opts.ifs)
    print "Mining topics..."
    m=s.mine(opts.r,opts.l)
    print "Size of original mined topics:",m.size()
    m.cutoff(min=opts.min)
    print "Size of cutted off mined topics:",m.size()

 
    if opts.output:
        print "Saving resulting model to",opts.output
        smh.smh_save(opts.output)




