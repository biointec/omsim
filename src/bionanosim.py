#!/usr/bin/python
import sys
from util import fasta_parse
from knick import index_sequence
from noise import generate_molecules
from bnx import write_bnx_header, write_bnx_entry
from settings import Settings

def bnsim(settings):
        moleculeID = 0
        fks = []
        rcks = []
        seqLens = []
        for meta, seq in fasta_parse(settings.ifname):
                print('Indexing sequence: ' + meta)
                seqLens.append(len(seq))
                fk, rck = index_sequence(seq, settings)
                print('Found ' + str(len(fk)) + ' knicks in ' + str(seqLens[-1]) + 'bp.')
                fks.append(fk)
                rcks.append(rck)
                meta = None
                seq = None
        print('Generating reads...')
        chip = 1
        chip_size = 0
        ofile = open(settings.ifname + '.' + str(chip) + '.bnx', 'w')
        write_bnx_header(ofile, settings)
        for l, m in generate_molecules(seqLens, fks, rcks, settings):
                        moleculeID += 1
                        write_bnx_entry((moleculeID, l), m, ofile)
                        chip_size += l
                        if chip_size > settings.chip_size:
                                chip += 1
                                ofile.close()
                                ofile = open(settings.ifname + '.' + str(chip) + '.bnx', 'w')
                                chip_size = 0
        ofile.close()
        print('Finished.')

def main(argv = None):
        if argv is None:
                argv = sys.argv
        settings = Settings()
        settings.ifname = argv[1]
        settings.patterns = [argv[2]]
        settings.min_mol_len = int(argv[3]) #kb
        settings.circular = int(argv[4])
        if settings.min_mol_len < 0:
                settings.min_mol_len = 0
        bnsim(settings)

if __name__ == "__main__":
        sys.exit(main())
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
