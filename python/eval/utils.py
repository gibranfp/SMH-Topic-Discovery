#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Utils for reading files
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2015/IIMAS/UNAM
# ----------------------------------------------------------------------
#
# System libraries
def t2c(vtopics,vcorpus):
    '''Returns a map between vocbulary'''
    topic2corpus=None
    v_topics={}
    for line in open(vtopics):
        line=line.strip().split()
        v_topics[line[0]]=int(line[2])
    topic2corpus={}
    for line in open(vcorpus):
        line=line.strip().split()
        try:
            topic2corpus[v_topics[line[0]]]=int(line[2])
        except KeyError:
            pass
    return topic2corpus

