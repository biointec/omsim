#!/usr/bin/python
import sys
from util import fasta_parse as RF
from knick import knicks
from bnx import bnx_header, bnx_entry
from noise import knick_molecule, strand

ifname = sys.argv[1]
patterns = [sys.argv[2]]
min_mol_len = int(sys.argv[3]) #kb
circular = int(sys.argv[4])
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

max_pattern_len = max([len(p) for p in patterns])
moleculeID = 0
for meta, seq in RF(ifname):
        seqLen = len(seq)
        if circular:
                seq += seq[0:max_pattern_len]
        fk, rck = knicks(seq, patterns)
        if circular:
                #remove duplicate hits
                while fk[-1][0] >= seqLen:
                        fk.pop()
                while rck[-1][0] >= seqLen:
                        rck.pop()
        seq = None
        size = 0
        while size < coverage * seqLen:
                i, m = knick_molecule([fk, rck][strand()], seqLen, avg, fprate, fnrate, sd, circular)
                l = i[0]
                if l >= min_mol_len:
                        size += l
                        moleculeID += 1
                        bnx_entry((moleculeID, l), m, ofile)

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
