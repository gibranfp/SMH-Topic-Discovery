#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Ivan V. Meza
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
    p.add_argument("word",
        action="store", help="Word to search")
    p.add_argument("topics",default=None,nargs="*",
        action="store", help="Set of topics in text")
 
    opts = p.parse_args()

    fdics={}
    for filename in opts.topics:
        for line in open(filename):
            line=line.strip()
            score,line=line.split(" ",1)
            words=line.split(", ")
            if opts.word in words or opts.word=='*':
                print filename
                fdics[filename]=True
                print "${0:1.2f}$".format(float(score)),"&",", ".join(words[:5]),"\\\\"
                print "& & ",", ".join(words[5:10]),"$({0})$".format(len(words)),"\\\\\\hline"
    print "Total de archivos",len(fdics)
