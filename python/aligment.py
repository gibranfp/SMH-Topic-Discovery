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
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pl
from smh import smh
import math
from eval.coherence import coherence, utils
from eval.consistency import topics_consistency
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

# MAIN program
if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser("Mines")
    p.add_argument("--thres",default=0.7,type=float,
            action="store", dest='thres',
            help="Threshold for assigment")
    p.add_argument("topics1",default=None,
        action="store", help="Set of topics one")
    p.add_argument("topics2",default=None,
        action="store", help="Set of topics two")


    opts = p.parse_args()

    print "Loading topics one:",opts.topics1
    top1=smh.smh_load(opts.topics1)

    print "Loading topics two:",opts.topics2
    top2=smh.smh_load(opts.topics2)

    res=topics_consistency(top1,top2,opts.thres)

