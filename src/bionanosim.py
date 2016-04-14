#!/usr/bin/python
import sys
from util import fasta_parse
from knick import index_sequence
from noise import generate_molecules
from bnx import write_bnx_header, write_bnx_entry

ifname = sys.argv[1]
patterns = [sys.argv[2]]
min_mol_len = int(sys.argv[3]) #kb
circular = int(sys.argv[4])
if min_mol_len < 0:
        min_mol_len = 0
ofile = open(ifname + ".bnx", 'w')
bns_version = '0.1'
bnx_version = '1.2'
avg = 200000
coverage = 100
fprate = 1.0 #number of fp in 100kb
fnrate = 0.15 #fn rate of true labels
sd = 1500 #sd of knick position
#TODO stretchfactor = .85
#TODO bp per chip

stats = [avg, coverage, fprate, fnrate, sd, min_mol_len]

moleculeID = 0
fks = []
rcks = []
seqLens = []
for meta, seq in fasta_parse(ifname):
        print('Indexing sequence: ' + meta)
        seqLens.append(len(seq))
        fk, rck = index_sequence(seq, circular, patterns)
        print(str(len(fk)) + ' knicks found.')
        fks.append(fk)
        rcks.append(rck)
        meta = None
        seq = None

print('Generating reads...')
write_bnx_header(ofile, bns_version, bnx_version, patterns, min_mol_len)
for l, m in generate_molecules(seqLens, fks, rcks, stats, [circular] * len(fks)):
                moleculeID += 1
                write_bnx_entry((moleculeID, l), m, ofile)
print('Finished.')


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
