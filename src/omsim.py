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
from util import fasta_parse
from noise import generate_scan, chip_stretch_factor, scan_stretch_factor
from bnx import write_bnx_header, write_bnx_entry
from settings import Settings
from random import seed
from util import double_stranded_multi_KMP_from_fasta as KMP
import numpy as np
import xml.etree.ElementTree


def omsim(settings):
        # set seeds
        seed(settings.seed)
        np.random.seed(settings.seed)
        # process input
        seqs, seq_lens, fks, rcks = KMP(settings)
        if settings.coverage != 0 and settings.chips != 1:
                settings.chips = 1 + int(sum(seq_lens) * settings.coverage / (settings.scans_per_chip * settings.get_scan_size()))
        settings.estimated_coverage = int(settings.get_scan_size() * settings.scans_per_chip * settings.chips / float(sum(seq_lens)))
        print('Generating reads on ' + str(settings.chips) + ' chip' + ('' if settings.chips == 1 else 's') + ', estimated coverage: ' + str(settings.estimated_coverage) + 'x.')
        bedfile = open(settings.prefix + '.bed', 'w')
        # generate reads
        for chip in range(1, settings.chips + 1):
                chip_settings = {'size': 0, 'scans': 0,
                                 'chip_id': 'unknown', 'run_id': str(chip),
                                 'flowcell': 1, 'molecule_count': 0,
                                 'bpp': 425, 'stretch_factor': chip_stretch_factor(settings)}
                chip_settings['bpp'] /= chip_settings['stretch_factor']
                molecules = {}
                for label in settings.labels:
                        molecules[label] = []
                # generate reads
                moleculeID = 0
                stretch = []
                for scan in range(1, settings.scans_per_chip + 1):
                        chip_settings['scans'] += 1
                        stretch.append(scan_stretch_factor(chip_settings['stretch_factor'], settings))
                        for l, m, meta in generate_scan(seq_lens, fks, rcks, settings):
                                        moleculeID += 1
                                        for mol in meta:
                                                bedfile.write(seqs[mol[0]] + '\t' + str(mol[1]) + '\t' + str(mol[1] + l) + '\t' + str(moleculeID) + '\n')
                                        molecule = {}
                                        for label in settings.labels:
                                                molecule[label] = []
                                        for nick in m:
                                                molecule[nick[1]['label']].append(nick[0])
                                        for label in settings.labels:
                                                if settings.min_nicks <= len(molecule[label]):
                                                        molecules[label].append((l, molecule[label], chip_settings['scans']))
                                        chip_settings['molecule_count'] += 1
                                        chip_settings['size'] += l
                # write output
                ofile = {}
                for label in settings.labels:
                        moleculeID = 0
                        ofile[label] = open(settings.prefix + '.' + label + '.' + str(chip) + '.bnx', 'w')
                        write_bnx_header(ofile[label], settings, label, chip_settings)
                        for l, m, s in molecules[label]:
                                moleculeID += 1
                                write_bnx_entry((moleculeID, l, s), m, ofile[label], chip_settings, stretch[s - 1])
                        ofile[label].close()
        bedfile.close()
        print('Finished processing ' + settings.name + '.\n')


def xml_enzyme_parse(xml_file):
        enzymes = []
        for child in xml.etree.ElementTree.parse(xml_file).getroot():
                enzyme = {}
                for entry in child:
                        if entry.tag in ['id', 'pattern']:
                                enzyme[entry.tag] = entry.text
                        else:
                                enzyme[entry.tag] = float(entry.text)
                enzymes.append(enzyme)
        return enzymes


def xml_input_parse(xml_file):
        s = []
        for child in xml.etree.ElementTree.parse(xml_file).getroot():
                settings = {}
                for entry in child:
                        if entry.tag == 'enzymes':
                                enzymes = []
                                enzyme_xml = []
                                for e in entry:
                                        if e.tag == 'enzyme':
                                                enzyme = {}
                                                for i in e:
                                                        enzyme[i.tag] = i.text
                                                enzymes.append(enzyme)
                                        elif e.tag == 'file':
                                                for enzyme in xml_enzyme_parse(e.text):
                                                        enzyme_xml.append(enzyme)
                                                if len(enzyme_xml) == 0:
                                                        print('Invalid nicking enzyme file.')
                                                settings['enzyme_xml'] = enzyme_xml
                                settings[entry.tag] = enzymes
                        elif entry.tag == 'files':
                                files = []
                                for file in entry:
                                        files.append(file.text)
                                settings[entry.tag] = files
                        elif entry.tag in ['name', 'file', 'prefix']:
                                settings[entry.tag] = entry.text
                        elif entry.tag == 'circular':
                                settings[entry.tag] = True
                        elif entry.tag in ['chimera_rate', 'fp_rate', 'fn_rate', 'stretch_factor', 'stretch_chip_sd', 'stretch_scan_sd']:
                                settings[entry.tag] = float(entry.text)
                        else:
                                settings[entry.tag] = int(entry.text)
                s.append(Settings(settings))
        return s


def print_welcome():
        print('This is an experimental version of omsim, scripts and configuration files based on this version might be incompatible with future versions. Some default settings may not have reasonable values yet.')


def print_usage():
        print('Usage: omsim.py file.xml' + '\n' + 'Example xml-files: example.xml (all options) and minimal.xml (required options).' + '\n' + 'Enzyme properties are specified in enzymes.xml.')


def main(argv=None):
        print_welcome()
        if argv is None:
                argv = sys.argv
        print(' '.join(argv))
        simulations = []
        for i in range(1, len(argv)):
                opt = argv[i]
                if opt == '-h' or opt == '--help':
                        print_usage()
                else:
                        for s in xml_input_parse(opt):
                                simulations.append(s)
        for settings in simulations:
                print(settings)
                omsim(settings)
        return 0

if __name__ == "__main__":
        sys.exit(main())
