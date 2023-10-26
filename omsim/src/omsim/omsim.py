#!/usr/bin/python
'''
        Copyright (C) 2016 Giles Miclotte (giles.miclotte@ugent.be)
        This file is part of OMSim

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

import math
import sys
import os
import xml.etree.ElementTree

from util import double_stranded_multi_KMP_from_fasta as KMP
from noise import Noise
from bnx import BNX
from settings import Settings
import struct
from cmap import Cmap, Nicks
from merge import merge_bnx

def write_processed_input(settings, cmaps):
        prefix = settings.directory + '/' + settings.byte_prefix
        mfn = prefix + '.byte.meta'
        meta_file = open(mfn, 'w')
        nfn = prefix + '.byte.nicks'
        nicks_file = open(nfn, 'wb')
        meta_file.write(str(2) + '\t' + mfn + '\t' + nfn + '\n')
        meta_file.write(str(len(cmaps)))
        for iname in cmaps.keys():
                meta_file.write('\t' + iname)
        meta_file.write('\n')
        for iname in cmaps:
                cmap = cmaps[iname]
                count = cmap.seq_count()
                enzymes = cmap.enzymes
                meta_file.write(str(count))
                for s in cmap.seqs:
                        meta_file.write('\t' + s)
                meta_file.write('\n')
                meta_file.write(str(count))
                for l in cmap.seq_lens:
                        meta_file.write('\t' + str(l))
                meta_file.write('\n')
                meta_file.write(str(len(enzymes)))
                for e in cmap.enzymes:
                        meta_file.write('\t' + e)
                meta_file.write('\n')
                meta_file.write(str(2 * len(cmap.enzymes) * count))
                for nicks in cmap.nicks:
                        for enzyme in cmap.enzymes:
                                if enzyme in nicks.nicks.keys():
                                        array = nicks.nicks[enzyme]
                                else:
                                        array = {False: [], True: []}
                                for b in [0, 1]:
                                        nicks_file.write(struct.pack('i' * len(array[b]), *(array[b])))
                                        meta_file.write('\t' + str(len(array[b])))
                meta_file.write('\n')
        meta_file.close()
        nicks_file.close()


def import_input(settings):
        cmaps = {}
        prefix = settings.directory + '/' + settings.byte_prefix
        if os.path.isfile(prefix + '.byte.meta'):
                meta_file = open(prefix + '.byte.meta')
                byte_file = open(prefix + '.byte.nicks', 'rb')
                line = meta_file.readline()
                line = meta_file.readline()
                file_count = int(line[0])
                inames = line.split()[1:]
                for iname in inames:
                        cmaps[iname] = Cmap(iname)
                        s = meta_file.readline().split()[1:]
                        l = meta_file.readline().split()[1:]
                        for e in meta_file.readline().split()[1:]:
                                cmaps[iname].add_enzyme(e)
                        c = meta_file.readline().split()[1:]
                        c_idx = 0
                        for idx in range(len(s)):
                                cmaps[iname].add_meta(idx, s[idx], int(l[idx]))
                                for e in cmaps[iname].enzymes:
                                        for b in [False, True]:
                                                size = int(c[c_idx])
                                                cmaps[iname].add_nicks(idx, e, b, struct.unpack('i' * size, byte_file.read(4 * size)))
                                                c_idx += 1
        return cmaps


def filter_nicks(settings, nicks):
        done = False
        idxs = {}
        fns = []
        for e in nicks.keys():
                idxs[e] = {False: 0, True: 0}
        while not done:
                m = None
                done = True
                for e in nicks.keys():
                        if not e in settings.enzymes.keys():
                                continue
                        for b in [False, True]:
                                if idxs[e][b] >= len(nicks[e][b]):
                                        continue
                                if m is None or nicks[e][b][idxs[e][b]] < m[0]:
                                        m = (nicks[e][b][idxs[e][b]], b, settings.enzymes[e])
                if m is not None:
                        fns.append(m)
                        idxs[m[2]['id']][m[1]] += 1
                        done = False
        return list(fns)

def filter_input(settings, cmaps):
        seqs = []
        seq_lens = []
        fns = []
        for iname in cmaps:
                cmap = cmaps[iname]
                if not cmap.iname in settings.files:
                        continue
                for idx in range(len(cmap.seqs)):
                        if cmap.seq_lens[idx] > settings.min_mol_len:
                                seqs.append(cmap.seqs[idx])
                                seq_lens.append(cmap.seq_lens[idx])
                                fns.append(filter_nicks(settings, cmap.nicks[idx].nicks))
        return seqs, seq_lens, fns

def get_rns(settings, fns, seq_lens):
        rns = []
        for idx in range(len(fns)):
                f = fns[idx]
                l = seq_lens[idx]
                rns.append(list(reversed([(l - pos[0] - len(settings.enzymes[pos[2]['id']]['pattern']), pos[1], pos[2]) for pos in f])))
        return rns


def generate_scan(settings, chip_settings, noise, seq_lens, cum_seq_lens, fns, rns, molecules, total_num_mol):
        """
        Generate a single scan on the chip defined by chip_settings.
        chip_settings and molecules are modified here
        """
        moleculeID = 0
        scan = 0
        while True if settings.min_num_mol > 0 else scan < settings.scans_per_chip:
                scan += 1
                chip_settings['scans'] += 1
                scan_stretch = noise.scan_stretch_factor(chip_settings['stretch_factor'])
                for l, m, meta, stretch_factor in noise.generate_scan(seq_lens, cum_seq_lens, fns, rns, scan_stretch):
                        moleculeID += 1
                        molecule = {}
                        for label in settings.labels:
                                molecule[label] = []
                        for nick in m:
                                molecule[nick[1]['label']].append(nick[0])
                        rel_stretch_factor = stretch_factor / chip_settings['stretch_factor_estimate']
                        if settings.min_mol_len <= l * rel_stretch_factor and settings.min_nicks <= len(m):
                                for label in settings.labels:
                                        molecules[label].append((l, molecule[label], chip_settings['scans'], meta,
                                                                 rel_stretch_factor, moleculeID))
                        chip_settings['molecule_count'] += 1
                        total_num_mol += 1
                        if total_num_mol >= settings.max_num_mol > 0:
                                return total_num_mol
                if total_num_mol >= settings.min_num_mol > 0:
                        break
        return total_num_mol

def omsim(settings):
        # process input
        cmaps = import_input(settings)
        print('Imported ' + str(sum(cmaps[iname].count() for iname in cmaps)) + ' nicks in ' + str(sum(cmaps[iname].seq_len() for iname in cmaps)) + 'bp.')
        cmaps = KMP(settings, cmaps)
        # write processed input
        write_processed_input(settings, cmaps)
        # filter input for enzymes / files we need
        seqs, seq_lens, fns = filter_input(settings, cmaps)
        # print(fns)
        prev = 0
        cum_seq_lens = []
        for seq_len in seq_lens:
                curr = prev + seq_len
                cum_seq_lens += [curr]
                prev = curr
        print('Using ' + str(sum(len(f) for f in fns)) + ' nicks in ' + str(sum(seq_lens)) + 'bp.')
        #compute reverse nicking sites
        rns = get_rns(settings, fns, seq_lens)
        # determine number of chips
        if settings.chips > 0:
                # if number of chips is specified, then this takes priority
                settings.chips = settings.chips
        elif settings.min_num_mol > 0:
                # if minimal number of molecules is specified, then a single chip will be simulated
                settings.chips = 1
        elif settings.coverage > 0:
                # if the coverage is specified, then estimate the number of required chips
                temp = math.ceil(sum(seq_lens) * settings.coverage / (settings.scans_per_chip * settings.get_scan_size()))
                settings.chips = temp if temp > 1 else 1
        else:
                # in the final case, nothing is specified, and a single chip will be simulated
                settings.chips = 1
        #estimate coverage
        settings.estimated_coverage = 0
        if settings.min_num_mol == 0:
                settings.estimated_coverage = settings.get_scan_size() * settings.scans_per_chip * settings.chips / float(sum(seq_lens))
        else:
                settings.estimated_coverage = settings.min_num_mol * settings.avg_mol_len / float(sum(seq_lens))
        if settings.max_num_mol > 0:
                cap = settings.max_num_mol * settings.avg_mol_len / float(sum(seq_lens))
                settings.estimated_coverage = min(settings.estimated_coverage, cap)
        print(f'Generating reads on {settings.chips} chip{"" if settings.chips == 1 else "s"}, estimated coverage: {settings.estimated_coverage:.2f}x.')
        noise = Noise(settings)
        bnx = BNX(settings, noise)
        total_num_mol = 0
        # generate reads
        for chip in range(1, settings.chips + 1):
                if total_num_mol >= settings.max_num_mol > 0:
                        break
                chip_settings = {'scans': 0,
                                 'chip_id': '20249,11843,07/17/2014,840014289', 'run_id': str(chip),
                                 'flowcell': 1, 'molecule_count': 0,
                                 'bpp': 425, 'stretch_factor': noise.chip_stretch_factor()}
                chip_settings['stretch_factor_estimate'] = chip_settings['stretch_factor']
                if settings.fixed_stretch_factor_estimate > 0:
                        chip_settings['stretch_factor_estimate'] = settings.fixed_stretch_factor_estimate
                chip_settings['bpp'] /= chip_settings['stretch_factor_estimate']
                molecules = {}
                for label in settings.labels:
                        molecules[label] = []
                # generate reads
                total_num_mol = generate_scan(settings, chip_settings, noise, seq_lens, cum_seq_lens, fns, rns, molecules, total_num_mol)

                # write output
                prefix = settings.directory + '/' + settings.prefix
                for label in settings.labels:
                        moleculeID = 0
                        ofile = open(prefix + '.' + label + '.' + str(chip) + '.bnx', 'w')
                        bnx.write_bnx_header(ofile, label, chip_settings)
                        for l, m, s, meta, stretch_factor, original_ID in molecules[label]:
                                moleculeID += 1
                                bnx.write_bnx_entry((moleculeID, l, s), m, ofile, chip_settings, stretch_factor, original_ID)
                        ofile.close()
                # write bed file
                if settings.bed_file:
                        bed_file = open(prefix + '.' + str(chip) + '.bed', 'w')
                        moleculeID = 0
                        for _, _, _, meta, _ in molecules[settings.labels[0]]:
                                moleculeID += 1
                                for idx, mol in enumerate(meta):
                                        is_forward = mol[3]
                                        start = mol[1] if is_forward else seq_lens[mol[0]] - mol[1]
                                        end = start + mol[2] if is_forward else start - mol[2]
                                        molecule_pos = seqs[mol[0]] + '\t' + str(start) + '\t' + str(end) + '\t'
                                        molecule_id = str(moleculeID) + ('.' + str(idx) if len(meta) > 1 else '') + '\n'
                                        bed_file.write(molecule_pos + molecule_id)
                        bed_file.close()
                if not settings.do_not_merge_bnx:
                        merge_bnx(prefix + '.' + str(chip) + '.bnx', [prefix + '.' + label + '.' + str(chip) + '.bnx' for label in settings.labels])
                print('Finished chip ' + str(chip) + '/' + str(settings.chips))
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
        directory = os.path.dirname(os.path.realpath(xml_file))
        for child in xml.etree.ElementTree.parse(xml_file).getroot():
                settings = {'directory': directory}
                for entry in child:
                        if entry.tag == 'enzymes':
                                enzymes = []
                                enzyme_xml = []
                                for e in entry:
                                        if e.tag == 'enzyme':
                                                enzyme = {}
                                                for i in e:
                                                        if i.tag in ['id', 'pattern', 'label']:
                                                                enzyme[i.tag] = i.text
                                                        else:
                                                                enzyme[i.tag] = float(i.text)
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
                        elif entry.tag in ['name', 'file', 'prefix', 'byte_prefix', 'label_snr_filter_type']:
                                settings[entry.tag] = entry.text
                        elif entry.tag == 'circular':
                                settings[entry.tag] = True
                        elif entry.tag == 'bed_file':
                                settings[entry.tag] = True
                        elif entry.tag == 'do_not_merge_bnx':
                                settings[entry.tag] = True
                        elif entry.tag in ['min_label_SNR', 'chimera_rate', 'fixed_stretch_factor_estimate', 'stretch_factor', 'stretch_chip_sd', 'stretch_scan_sd', 'stretch_mol_sd', 'molecule_AI_mu', 'molecule_AI_sd', 'label_AI_mu', 'label_AI_sd', 'molecule_SNR_mu', 'molecule_SNR_sd', 'label_SNR_mu', 'label_SNR_sd']:
                                settings[entry.tag] = float(entry.text)
                        else:
                                settings[entry.tag] = int(entry.text)
                s.append(Settings(settings))
        return s


def print_welcome(version):
        print('Welcome to OMSim ' + version)


def print_usage():
        print('Usage: omsim.py file.xml' + '\n' + 'Example xml-files: example.xml (many options) and minimal.xml (minimal required options).' + '\n' + 'Enzyme properties are specified in enzymes.xml.')


def main(argv=None):
        version = "v1.2.2"
        print_welcome(version)
        if argv is None:
                argv = sys.argv
        print(' '.join(argv))
        simulations = []
        if len(argv) == 1:
                print_usage()
                return 0
        for i in range(1, len(argv)):
                opt = argv[i]
                if opt == '-h' or opt == '--help':
                        print_usage()
                else:
                        for s in xml_input_parse(opt):
                                s.version = version
                                simulations.append(s)
        for settings in simulations:
                print(settings)
                settings.warn()
                omsim(settings)
        return 0
