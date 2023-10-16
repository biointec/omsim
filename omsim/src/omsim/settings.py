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


class Settings:
        def __init__(self, args):
                self.bnx_version = '1.2'
                
                self.circular = False
                
                self.name = 'Unnamed'
                self.prefix = 'omsim_output'
                self.byte_prefix = 'omsim'
                self.bed_file = False
                self.do_not_merge_bnx = False
                self.coverage = 0
                self.chips = 0
                self.scans_per_chip = 30
                self.scan_size = 1500
                self.avg_mol_len = 90000
                self.sd_mol_len = 85000
                self.min_mol_len = 1
                self.max_mol_len = 2500000
                self.min_nicks = 1
                self.label_snr_filter_type = 'Static'
                self.min_label_SNR = 0.0
                self.nick_sd = 50
                self.fragile_same = 50
                self.fragile_opposite = 150
                self.fragile_threshold = 25
                self.fragile_factor = 3
                self.label_mu = 1500
                self.label_threshold = 500
                self.label_factor = 100
                self.chimera_rate = 0.01
                self.chimera_mu = 1500
                self.chimera_sigma = 500
                self.fixed_stretch_factor_estimate = 0.0
                self.stretch_factor = .85
                self.stretch_chip_sd = 0.02
                self.stretch_scan_sd = 0.01
                self.stretch_mol_sd = 0.005
                self.molecule_AI_mu = 0.3
                self.molecule_AI_sd = 0.2
                self.label_AI_mu = 0.07
                self.label_AI_sd = 0.04
                self.molecule_SNR_mu = 15.0
                self.molecule_SNR_sd = 75.0
                self.label_SNR_mu = 14.0
                self.label_SNR_sd = 11.0
                self.sim_batch_size = 100000
                self.always_forward = False
                self.seed = None
                
                self.enzyme_xml = ""
                
                self.files = []
                self.enzymes = []
                self.labels = []

                self.__dict__.update(args)
                self.avg_mol_len = float(self.avg_mol_len)
                self.sd_mol_len = float(self.sd_mol_len)
                self.set_patterns()

        def __str__(self):
                s = ''
                s += 'Version: ' + self.version + '\n'
                s += 'BNX version: ' + self.bnx_version + '\n'
                # s += 'Patterns: ' + ' '.join([str(enzyme) for enzyme in self.enzymes]) + '\n'
                if self.circular:
                        s += 'Circular genome.\n'
                s += 'Minimal molecule length: ' + str(self.min_mol_len) + ' bp\n'
                s += 'Average molecule length: ' + str(self.avg_mol_len) + ' bp\n'
                s += 'Standard deviation of molecule length: ' + str(self.sd_mol_len) + '\n'
                s += 'Minimal coverage: ' + str(self.coverage) + 'x\n'
                s += 'Chimera rate: ' + str(self.chimera_rate * 100) + '%\n'
                if self.seed is not None:
                        s += 'Random seed: ' + str(self.seed) + '\n'
                return s

        def get_scan_size(self):
                MEGA = 1000 * 1000
                return self.scan_size * MEGA

        def set_patterns(self):
                enzymes = {}
                for enzyme in self.enzymes:
                        found = False
                        if 'id' in enzyme and 'label' in enzyme:
                                if 'pattern' in enzyme and 'fn' in enzyme and 'fp' in enzyme:
                                        enzymes[enzyme['id']] = enzyme
                                        found = True
                                else:
                                        if self.enzyme_xml == "":
                                                break
                                        for e in self.enzyme_xml:
                                                if e['id'] == enzyme['id']:
                                                        enzymes[enzyme['id']] = e
                                                        found = True
                                                        break
                        if found:
                                if 'label' in enzyme:
                                        label = enzyme['label']
                                else:
                                        label = 'label_' + str(len(self.labels))
                                enzymes[enzyme['id']]['label'] = label
                                if not label in self.labels:
                                        self.labels.append(label)
                        else:
                                print('Unknown nicking enzyme: ' + enzyme['id'])
                                exit()
                self.enzymes = enzymes
