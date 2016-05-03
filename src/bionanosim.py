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
import numpy as np
import xml.etree.ElementTree

def bnsim(settings):
        moleculeID = 0
        fks = []
        rcks = []
        seqs = []
        seq_lens = []
        for file in settings.files:
                for meta, seq in fasta_parse(file):
                        print('Indexing sequence: ' + meta)
                        seqs.append(meta)
                        seq_lens.append(len(seq))
                        fk, rck = index_sequence(seq, settings)
                        print('Found ' + str(len(fk)) + ' knicks in ' + str(seq_lens[-1]) + 'bp.')
                        fks.append(fk)
                        rcks.append(rck)
        if settings.coverage != 0:
                settings.chips = 1 + int(sum(seq_lens) * settings.coverage / (settings.get_chip_size()))
        print('Generating reads on ' + str(settings.chips) + ' chip' + ('' if settings.chips == 1 else 's') + '.')
        chip = 1
        chip_size = 0
        bedfile = open(settings.prefix + '.bed', 'w')
        while chip <= settings.chips:
                ofile = open(settings.prefix + '.' + str(chip) + '.bnx', 'w')
                write_bnx_header(ofile, settings)
                for l, m, meta in generate_molecules(seq_lens, fks, rcks, settings):
                                moleculeID += 1
                                for mol in meta:
                                        bedfile.write(seqs[mol[0]] + '\t' + str(mol[1]) + '\t' + str(mol[1] + l) + '\t' + str(moleculeID) + '\n')
                                write_bnx_entry((moleculeID, l), m, ofile)
                                chip_size += l
                chip += 1
                chip_size = 0
                ofile.close()
        bedfile.close()
        print('Finished.')

def xml_knick_parse(xml_file):
        knicks = []
        for child in xml.etree.ElementTree.parse(xml_file).getroot():
                knick = {}
                for entry in child:
                        knick[entry.tag] = entry.text
                knicks.append(knick)
        return knicks

def xml_input_parse(xml_file):
        s = []
        for child in xml.etree.ElementTree.parse(xml_file).getroot():
                settings = {}
                for entry in child:
                        if entry.tag == 'knicks':
                                knicks = []
                                for k in entry:
                                        knick = {}
                                        for i in k:
                                                knick[i.tag] = i.text
                                        knicks.append(knick)
                                settings[entry.tag] = knicks
                        elif entry.tag == 'files':
                                files = []
                                for file in entry:
                                        files.append(file.text)
                                settings[entry.tag] = files
                        elif entry.tag in ['name', 'file', 'prefix']:
                                settings[entry.tag] = entry.text
                        elif entry.tag == 'circular':
                                settings[entry.tag] = True
                        elif entry.tag in ['chimera_rate', 'fp_rate', 'fn_rate']:
                                settings[entry.tag] = float(entry.text)
                        else:
                                settings[entry.tag] = int(entry.text)
                s.append(Settings(settings))
        return s


def main(argv = None):
        print('This is an experimental version of BNS, scripts and configuration files based on this version may not be compatible with future versions.')
        if argv is None:
                argv = sys.argv

        try:
                opts, args = getopt.getopt(argv[1:], 'hk:x:i:p:cl:', ['help', 'knicks=', 'xml=', 'input=', 'pattern=', 'circular', 'length=', 'fp=', 'fn=', 'seed='])
        except getopt.error:
                print >>sys.stderr, 'For help use --help'
                return 2

        simulations = []
        knicks = []
        settings = Settings({})
        for opt, val in opts:
                if opt == '-h' or opt == '--help':
                        print('Help message should come here.') #TODO
                elif opt == '-k' or opt == '--knicks':
                        for knick in xml_knick_parse(val):
                                knicks.append(knick)
                        if len(knicks) == 0:
                                print('Invalid knicking enzyme file.')
                                exit()
                elif opt == '-x' or opt == '--xml':
                        for s in xml_input_parse(val):
                                simulations.append(s)
                elif opt == '-i' or opt == '--input':
                        settings.files.append(val)
                elif opt == '-p' or opt == '--pattern':
                        settings.patterns.append(val)
                elif opt == '-c' or opt == '--circular':
                        settings.circular = True
                elif opt == '--seed':
                        settings.seed = int(val)
                        seed(settings.seed)
                        np.random.seed(settings.seed)
        if len(knicks) == 0:
                print('No knicking enzyme files were specified.')
                exit()
        if len(settings.files) > 0:
                simulations.append(settings)
        for settings in simulations:
                settings.set_patterns(knicks)
                print(settings)
                bnsim(settings)

if __name__ == "__main__":
        sys.exit(main())
