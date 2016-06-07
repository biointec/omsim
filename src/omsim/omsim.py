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
import os
import xml.etree.ElementTree

from util import double_stranded_multi_KMP_from_fasta as KMP
from noise import Noise
from bnx import BNX
from settings import Settings
import struct

def write_processed_input(settings, seqs, seq_lens, fks, rcks, mod=''):
        prefix = settings.prefix + mod
        for idx in range(len(fks)):
                names = ['seqs', 'lens', 'fns', 'rcns']
                meta_file = open(prefix + '.' + str(idx) + '.meta.byte', 'w')
                for j in range(4):
                        array = [seqs, seq_lens, fks, rcks][j][idx]
                        if j in [0, 1]:
                                file = open(prefix + '.' + str(idx) + '.' + names[j] + '.byte', 'w')
                                file.write(str(array))
                                file.close()
                        else:
                                arrays = {}
                                for enzyme in settings.enzymes:
                                        arrays[enzyme['id']] = [[], []]
                                for pos in array:
                                        arrays[pos[2]['id']][int(pos[1])].append(pos[0])
                                for enzyme in settings.enzymes:
                                        for b in [0, 1]:
                                                file_name = prefix + '.' + str(idx) + '.' + names[j] + '.' + enzyme['id'] + '.' + str(b) + '.byte'
                                                file = open(file_name, 'wb')
                                                file.write(struct.pack('i' * len(arrays[enzyme['id']][b]), *(arrays[enzyme['id']][b])))
                                                meta_file.write(enzyme['id'] + '\t' + str(b) + '\t' + str(len(arrays[enzyme['id']][b])) + '\t' + names[j] + '\t' + file_name + '\n')
                                                file.close()
                meta_file.close()

def import_input(settings):
        imported = False
        idx = 0
        seqs = []
        seq_lens = []
        fks = []
        rcks = []
        while os.path.isfile(settings.prefix + '.' + str(idx) + '.meta.byte'):
                infile = open(settings.prefix + '.' + str(idx) + '.seqs.byte')
                for line in infile:
                        seqs.append(line)
                infile.close()
                infile = open(settings.prefix + '.' + str(idx) + '.lens.byte')
                for line in infile:
                        seq_lens.append(int(line))
                infile.close()
                enzymes = {}
                for e in settings.enzymes:
                        enzymes[e['id']] = e
                infile = open(settings.prefix + '.' + str(idx) + '.meta.byte')
                temp_fns = {}
                temp_rcns = {}
                for line in infile:
                        e, b, l, name, file_name = line.split()
                        if not e in temp_fns:
                                temp_fns[e] = {False:{}, True:{}}
                                temp_rcns[e] = {False:{}, True:{}}
                        b = int(b)
                        if name == 'fns':
                                fns_file = open(file_name)
                                temp_fns[e][bool(b)] = struct.unpack('i' * int(l), fns_file.read())
                                fns_file.close()
                        elif name == 'rcns':
                                rcns_file = open(settings.prefix + '.' + str(idx) + '.' + 'rcns' + '.' + e + '.' + str(b) + '.byte')
                                temp_rcns[e][bool(b)] = struct.unpack('i' * int(l), rcns_file.read())
                                rcns_file.close()
                for i in [0, 1]:
                        idxs = {}
                        for e in settings.enzymes:
                                if not e['id'] in idxs:
                                        idxs[e['id']] = {False:{}, True:{}}
                                for b in [True, False]:
                                        idxs[e['id']][b] = 0
                        temp = [temp_fns, temp_rcns][i]
                        tn = []
                        done = False
                        while not done:
                                m = None
                                done = True
                                for e in settings.enzymes:
                                        for b in [True, False]:
                                                if idxs[e['id']][b] >= len(temp[e['id']][b]):
                                                        continue
                                                if m is None or temp[e['id']][b][idxs[e['id']][b]] < m[0]:
                                                        m = [temp[e['id']][b][idxs[e['id']][b]], b, e]
                                if m is not None:
                                        tn.append(m)
                                        idxs[m[2]['id']][m[1]] += 1
                                        done = False
                        [fks, rcks][i].append(tn)
                infile.close()
                imported = True
                idx += 1
        return seqs, seq_lens, fks, rcks, imported

def omsim(settings):
        # process input
        seqs, seq_lens, fks, rcks, imported = import_input(settings)
        if imported:
                print('Imported ' + str(sum(len(f) for f in fks)) + ' nicks in ' + str(sum(seq_lens)) + 'bp.')
        else:
                seqs, seq_lens, fks, rcks = KMP(settings)
        # write processed input
        write_processed_input(settings, seqs, seq_lens, fks, rcks, mod=('imported' if imported else ''))
        #estimate coverage
        if settings.coverage != 0 and settings.chips != 1:
                settings.chips = 1 + int(sum(seq_lens) * settings.coverage / (settings.scans_per_chip * settings.get_scan_size()))
        settings.estimated_coverage = int(settings.get_scan_size() * settings.scans_per_chip * settings.chips / float(sum(seq_lens)))
        print('Generating reads on ' + str(settings.chips) + ' chip' + ('' if settings.chips == 1 else 's') + ', estimated coverage: ' + str(settings.estimated_coverage) + 'x.')
        #bedfile = open(settings.prefix + '.bed', 'w')
        noise = Noise(settings)
        bnx = BNX(settings, noise)
        # generate reads
        for chip in range(1, settings.chips + 1):
                chip_settings = {'size': 0, 'scans': 0,
                                 'chip_id': '20249,11843,07/17/2014,840014289', 'run_id': str(chip),
                                 'flowcell': 1, 'molecule_count': 0,
                                 'bpp': 425, 'stretch_factor': noise.chip_stretch_factor()}
                chip_settings['bpp'] /= chip_settings['stretch_factor']
                molecules = {}
                for label in settings.labels:
                        molecules[label] = []
                # generate reads
                moleculeID = 0
                stretch = []
                for scan in range(1, settings.scans_per_chip + 1):
                        chip_settings['scans'] += 1
                        stretch.append(noise.scan_stretch_factor(chip_settings['stretch_factor']))
                        for l, m, meta in noise.generate_scan(seq_lens, fks, rcks):
                                        moleculeID += 1
                                        #for mol in meta:
                                        #        bedfile.write(seqs[mol[0]] + '\t' + str(mol[1]) + '\t' + str(mol[1] + l) + '\t' + str(moleculeID) + '\n')
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
                        bnx.write_bnx_header(ofile[label], label, chip_settings)
                        for l, m, s in molecules[label]:
                                moleculeID += 1
                                bnx.write_bnx_entry((moleculeID, l, s), m, ofile[label], chip_settings)
                        ofile[label].close()
        #bedfile.close()
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
