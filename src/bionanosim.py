#!/usr/bin/python
import sys
from readFasta import fasta_parse as RF
from knick import f_knicks, rc_knicks
from bnx import bnx_header, bnx_entry
from noise import knick_molecules, fisher_yates, strand

ifname = sys.argv[1]
pattern = sys.argv[2]
min_mol_len = sys.argv[3] #kb
ofile = open(ifname + ".bnx", 'w')
bnx_version = '1.2'
bnx_header(ofile, bnx_version, pattern, min_mol_len)
avg = 200000
coverage = 10

molecules = []
for meta, seq in RF(ifname):
        #this step might use some memory
        fk = f_knicks(seq, pattern)
        rck = rc_knicks(seq, pattern)
        c = 0
        while c < coverage:
                if (strand()):
                        #forward
                        molecules += list(knick_molecules(fk, len(seq), avg))
                else:
                        #reverse complement
                        molecules += list(knick_molecules(rck, len(seq), avg))
                c += 1
for molecule in fisher_yates(molecules):
        bnx_entry(molecule, ofile)
        

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
