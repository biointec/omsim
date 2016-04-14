#!/usr/bin/python
import sys
from util import fasta_parse as RF
from knick import knicks
from bnx import bnx_header, bnx_entry
from noise import knick_molecule, fisher_yates, strand

ifname = sys.argv[1]
patterns = [sys.argv[2]]
min_mol_len = int(sys.argv[3]) #kb
if min_mol_len < 0:
        min_mol_len = 0
ofile = open(ifname + ".bnx", 'w')
bns_version = '0.1'
bnx_version = '1.2'
bnx_header(ofile, bns_version, bnx_version, patterns, min_mol_len)
avg = 200000
coverage = 100
fprate = 1.0 #number of fp in 100kb
fnrate = 0.15 #fn rate of true labels
sd = 1500 #sd of knick position

molecules = []
for meta, seq in RF(ifname):
        fk, rck = knicks(seq, patterns)
        seqLen = len(seq)
        seq = None
        size = 0
        while size < coverage * seqLen:
                if (strand()):
                        #forward
                        i, m = knick_molecule(fk, seqLen, avg, fprate, fnrate, sd)
                        l = i[0]
                        if l >= min_mol_len:
                                size += l
                                molecules.append((l, m))
                else:
                        #reverse complement
                        i, m = knick_molecule(rck, seqLen, avg, fprate, fnrate, sd)
                        l = i[0]
                        if l >= min_mol_len:
                                size += l
                                molecules.append((l, m))

moleculeID = 0
for length, molecule in fisher_yates(molecules):
        moleculeID += 1
        bnx_entry((moleculeID, length), molecule, ofile)
        

'''
import sys
import getopt

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
             raise Usage(msg)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())

'''
