#!/usr/bin/python
import sys
from readFasta import fasta_parse as RF
from knick import f_knicks, rc_knicks
from bnx import bnx_header, bnx_entry
from noise import knick_molecule, fisher_yates, strand

ifname = sys.argv[1]
pattern = sys.argv[2]
min_mol_len = sys.argv[3] #kb
ofile = open(ifname + ".bnx", 'w')
bns_version = '0.1'
bnx_version = '1.2'
bnx_header(ofile, bns_version, bnx_version, pattern, min_mol_len)
avg = 200000
coverage = 100
fprate = 1.0 #number of fp in 100kb
fnrate = 0.15 #fn rate of true labels
sd = 1500 #sd of knick position

molecules = []
for meta, seq in RF(ifname):
        #this step might use some memory
        fk = f_knicks(seq, pattern)
        rck = rc_knicks(seq, pattern)
        c = 0
        size = 0
        while c < coverage:
                while size < (c + 1) * len(seq):
                        if (strand()):
                                #forward
                                for i, m in knick_molecule(fk, len(seq), avg, fprate, fnrate, sd):
                                        size += i[0]
                                        molecules.append((i[0], m))
                        else:
                                #reverse complement
                                for i, m in knick_molecule(rck, len(seq), avg, fprate, fnrate, sd):
                                        size += i[0]
                                        molecules.append((i[0], m))
                c += 1
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
