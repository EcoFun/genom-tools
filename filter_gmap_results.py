#!/usr/bin/env python2
# usage:
usage = "./filter_gmap_results.py min_iden min_cov <gmap_file.csv>"

__author__ = "Ludovic Duvaux"
__maintainer__ = "Ludovic Duvaux"
__license__ = "GPL_v3"

import sys, numpy as np, re

argv = sys.argv
if len(argv) is not 4:
    print "Usage: " + usage
    sys.exit()

fgma = argv[1]
min_iden = argv[2]
min_cov = argv[3]


# filter data
nodes = {}
with open(fgma) as gma:
    for l in gma:
        if l[:5] != 'Node\t':
            ele = l.strip().split()
            node = ele[0]
            ide1 = float(ele[3].split(",")[0])
            cov1 = float(ele[4].split(",")[0])
            if ide1 >= min_iden and cov1 >=min_cov:
                sca = ele[3].split(",")[2]
                nodes[node = [node, sca, ide1, cov1]
        else:
            continue


# write results
print "Node\tScafs\tiden\tCoverage"
for k in keys:
    print "\t".join(nodes[k])
