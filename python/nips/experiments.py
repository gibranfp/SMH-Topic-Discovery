#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Sampled MinHash demo with images
# ----------------------------------------------------------------------
# Gibran Fuentes-Pineda, Ivan V. Meza
# 2015/IIMAS, México
# ----------------------------------------------------------------------

import sys
sys.path.append('python')
import numpy as np
import pylab as pl
from smh import smh
from eval.coherence import coherence


# MAIN program
if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser("Mines")
    p.add_argument("-r","--tuple_size",default=[3],
                action="append", dest="rs",type=int,
                help="Size of the tuple")
    p.add_argument("-l","--number_tuples",default=[120],
                action="append", dest="ls",type=int,
                help="Number of tuples")
    p.add_argument("--output_pref",default=None,type=str,
        action="store", dest='outputpref',help="Prefix of output files")
    p.add_argument("--cutoff",default=None,type=int,
        action="store", dest='cutoff',help="Cutoff of topics [Off]")
    p.add_argument("--show",default=False,
            action="store_true", dest='show',help="Show bases found")
    p.add_argument("ifs",default=None,
        action="store", help="Inverted file structure of documents")

    opts = p.parse_args()

    if len(opts.ls)>1:
        opts.ls.pop(0)
    if len(opts.rs)>1:
        opts.rs.pop(0)

    print "Loading file ifs:",opts.ifs
    s=smh.smh_load(opts.ifs)

    pairs=zip(opts.rs,opts.ls)
    sorted(pairs)

    cs=[]

    for r,l in pairs:
        print "Experiment tuples (r)",r,"Number of tuples (l)",l
        print "Mining topics..."
        m=s.mine(r,l)
        print "Size of original mined topics:",m.size()
        if opts.cutoff:
            m.cutoff(min=opts.cutoff)
        print "Size of cutted off mined topics:",m.size()

        # EVAL coherence
        co=coherence(m,s)
        cs.append(((r,l),[c for t,c in co]))
        
        # Histograms of coherence
        vals=[c for t,c in co]
        h=pl.hist(vals)
        pl.title("r={0},l={1} (Avg. {2})".format(r,l,sum(vals)/len(vals)))
        pl.show()
        print "Average coherence:",sum(vals)/len(vals)

        if opts.outputpref:
            print "Saving resulting model to",opts.outputpref
            m.save(opts.outputpref+"r_{0}_l_{1}.topics".format(r,l))


    # Draw boxplot sizes
    ax = pl.subplot(111)
    pl.boxplot([d for x,d in cs])
    pl.xticks(range(1,len(cs)+1),["r={0},l={1}".format(x[0],x[1]) for x,d in
        cs],rotation="vertical")
    #pl.ylim((ax.get_ylim()[],0))
    pl.show()

  


