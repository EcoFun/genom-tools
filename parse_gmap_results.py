#!/usr/bin/env python2
# usage:
usage = "./parse_gmap_results.py.py <gmap_file>"

__author__ = "Ludovic Duvaux"
__maintainer__ = "Ludovic Duvaux"
__license__ = "GPL_v3"

import sys, numpy as np, re

argv = sys.argv
if len(argv) is not 2:
    print "Usage: " + usage
    sys.exit()

fgma = argv[1]

# read data
    # ID
    # npath
    # scaffs matching on
    # total coverage for each scaff
    # identity
nodes = {}
keys = []
with open(fgma) as gma:
    for l in gma:
        # ID
        if l[0] == ">":
            # try to update data
            try:
                fsca = ",".join(sca)
                fcov = ','.join(str(x) for x in cov)
                fiden = ",".join(iden)
                nodes[key] = [key, str(npath), fsca, fiden, fcov]
            except:
                pass
            key = l.strip().strip(">")
            keys.append(key)
            npath = -1 ; i = 1 ; sca = [] ; cov = [] ; iden = []   # initialize data
        # npaths
        elif l[:7] == "Paths (":
            npath = int(re.split("\(|\)", l)[1])
        # scaffolds
        elif l[:7] == "  Path ":
            if i > npath:
                print l
                sys.exit("Too many paths for the node " + key)
                #~print "Too many paths for the node " + key
                #~break
            nsca = re.split(" |:", l)[11]
            #~if nsca not in sca:
                #~sca.append(nsca)
            sca.append(nsca)
            i += 1
        # coverage
        elif l[:13] == "    Coverage:":
            ncov = float(l.split()[1])
            #~ind = sca.index(nsca)
            #~try:
                #~cov[ind] += ncov
            #~except IndexError:
                #~cov.append(ncov)
            cov.append(ncov)
        elif l[:21] == "    Percent identity:":
            niden = l.split()[2]
            iden.append(niden)
        else:
            continue

# don't forget the last entry!
fsca = ",".join(sca)
fcov = ','.join(str(x) for x in cov)
fiden = ",".join(iden)
nodes[key] = [key, str(npath), fsca, fiden, fcov]

#~for k in keys:
    #~if k not in nodes.keys():
        #~print k

# write results
print "Node\tNpaths\tScafs\tiden\tCoverage"
for k in keys:
    print "\t".join(nodes[k])
