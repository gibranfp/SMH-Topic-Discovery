#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Cut off vocabularyof files
# ----------------------------------------------------------------------
# Gibran Fuentes-Pineda, Ivan V. Meza
# 2015/IIMAS, México
# ----------------------------------------------------------------------

# MAIN program
if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser("Mines")
    p.add_argument("--max",default=1000,type=int,
            action="store", dest="max",
            help="Maximum vocabulary")
    p.add_argument("voca",default=None,
        action="store", help="Vocabulary file")
    p.add_argument("corpus",default=None,
        action="store", help="Corpus file")
    p.add_argument("nvoca",default=None,
        action="store", help="New cut off vocabulary file")
    p.add_argument("ncorpus",default=None,
        action="store", help="New cut off corpus file")


    opts = p.parse_args()

    fullvoca=[]
    for line in open(opts.voca):
        bits=line.strip().split()
        fullvoca.append((int(bits[4]),line))

    fullvoca.sort()
    fullvoca.reverse()
    voca={}
    nvoca=open(opts.nvoca,'w')
    i=0;
    for s,line in fullvoca:
        if i>= opts.max:
            break
        bits=line.strip().split()
        if len(bits[0])>3:
            print >> nvoca, line.strip()
            voca[int(bits[2])]=True
            i+=1
    nvoca.close()

    ncorpus=open(opts.ncorpus,'w')
    for i,line in enumerate(open(opts.corpus)):
        bits=line.strip().split()
        bits_=[]
        for bit in bits[1:]:
            tf=bit.split(':')
            t=int(tf[0])
            try:
                voca[t]
                bits_.append(bit)
            except KeyError:
                pass
        if len(bits_)>=0:
            print >> ncorpus, len(bits_)," ".join(bits_)

    ncorpus.close()

