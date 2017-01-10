#!/usr/bin/env python2
# Collect BUSCO metrics for individuals of different runs.

__author__ = "Ludovic Duvaux"
__maintainer__ = "Ludovic Duvaux"
__license__ = "GPL_v3"

import sys, argparse, os, glob, re

# 0.1) get options from commands lines
parser = argparse.ArgumentParser(description='Collect BUSCO metrics for individuals of different runs.',
epilog="Example: collect_Busco_summary.py -l -e '\.' 01_analyses/ > Busco_stats_Ventus.csv")
parser.add_argument('dirs', help='Directories of the global assembly runs (the script look for "run_*" in each of these dir).', nargs='+')
parser.add_argument('-e', '--regex-split', help='regex specifying the split character to retrieve the sample name from the short_summary* file (to be specified between quotes).', nargs=1, default=["\.c|_"])
parser.add_argument('-l', '--genlen', help='Does the script compute the genome length? If so, the name of fasta file will be obtained from the respective "short_summary*" BUSCO file. [False]', action='store_true')

# 0.2) set options
argv = parser.parse_args()
dirs = argv.dirs
reg = argv.regex_split[0]
tgl = argv.genlen
if tgl:
	from Bio import SeqIO
#~print tgl
#~sys.exit()

fres = {}
inds = []
for d in sorted(dirs):
	ldirs = glob.glob(d + "/run_*")
	#~print ldirs
	for r in ldirs:
		fil = glob.glob(r + "/short_summary_*")
		if len(fil)>0:
			fil = fil[0]
		else:
			continue
		#~print reg
		ind = re.split(reg, fil.split("short_summary_")[-1])[0]
		#~print ind
		#~sys.exit()

		if ind not in inds:
			inds.append(ind)
		#~print ind
		with open(fil) as f:
			txt = f.readlines()
			pdat = os.path.dirname(txt[0].split(":")[-1].strip())
			#~print pdat
			res = [ ind, d ]
			for l in txt[7:12]:
				res.append(l.split("\t")[1])
			# update fres
			#~print ind, r
			try:
				fres[ind][r] = "\t".join(res)
			except KeyError:
				fres[ind] = { r : "\t".join(res) }
		if tgl:
			gl = 0
			patt = d + pdat + "/*" + ind + "*"
			print d, pdat, ind
			print patt
			sys.stderr.write(ind + "\n")
			src = glob.glob(patt)[0]
			#~print src
			#~sys.exit()
			with open(src) as fs:
				for s in SeqIO.parse(fs, "fasta"):
					gl += len(s)
				#~print gl
			fres[ind][r] += "\t%s" % gl
			#~print fres[ind][r]
			#~sys.exit()
#~sys.exit()

# print res
header = "Individual\tAssembly\tComplete Single-Copy BUSCO\tComplete Duplicated BUSCO\tFragmented BUSCO\tMissing BUSCO\tTotal BUSCO"
if tgl:
	header += "\tGenome length"
print header
for i in sorted(inds):
	#~print i
	for k in sorted(fres[i].keys()):
		#~print k
		print fres[i][k]
