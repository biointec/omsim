#!/usr/bin/python
'''
        Copyright (C) 2016 Giles Miclotte (giles.miclotte@intec.ugent.be)
        This file is part of BioNanoSim

        This program is free software; you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation; either version 2 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program; if not, write to the
        Free Software Foundation, Inc.,
        59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
'''

import sys
import getopt
from util import fasta_parse
from knick import index_sequence
from noise import generate_molecules
from bnx import write_bnx_header, write_bnx_entry
from settings import Settings
from random import seed

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

        try:
                opts, args = getopt.getopt(argv[1:], 'hi:p:cl:', ['help', 'input=', 'pattern=', 'circular', 'length=', 'fp=', 'fn='])
        except getopt.error:
                print >>sys.stderr, 'For help use --help'
                return 2

        settings = Settings()
        for opt, val in opts:
                if opt == '-h' or opt == '--help':
                        print('Help message should come here.') #TODO
                elif opt == '-i' or opt == '--input':
                        settings.ifname = val
                elif opt == '-p' or opt == '--pattern':
                        settings.patterns.append(val)
                elif opt == '-c' or opt == '--circular':
                        settings.circular = True
                elif opt == '-l' or opt == '--length':
                        settings.min_mol_len = int(val)
                elif opt == '--fp':
                        settings.fprate = float(val)
                elif opt == '--fn':
                        settings.fnrate = float(val)
                elif opt == '--chim':
                        settings.chimrate = float(val)
        print(settings)
        seed(settings.seed)
        bnsim(settings)

if __name__ == "__main__":
        sys.exit(main())
