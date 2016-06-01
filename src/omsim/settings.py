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


class Settings:
        def __init__(self, args):
                self.version = 'v0.1'
                self.bnx_version = '1.2'
                self.name = 'Unnamed'
                self.files = []
                self.prefix = 'omsim_output'
                self.circular = False
                self.coverage = 0
                self.chips = 1
                self.scans_per_chip = 30
                self.scan_size = 1500
                self.avg_mol_len = 200000
                self.sd_mol_len = 150000
                self.min_mol_len = 1
                self.max_mol_len = 2500000
                self.min_nicks = 1
                self.label_snr_filter_type = 'Static'
                self.min_label_SNR = 0.0
                self.nick_sd = 50
                self.fragile_same = 50
                self.fragile_opposite = 150
                self.fragile_treshold = 25
                self.fragile_factor = 3
                self.label_mu = 1500
                self.label_treshold = 500
                self.label_factor = 100
                self.chimera_rate = 0.01
                self.chimera_mu = 1500
                self.chimera_sigma = 500
                self.stretch_factor = .85
                self.stretch_chip_sd = 0.01
                self.stretch_scan_sd = 0.001
                self.enzymes = []
                self.labels = []
                self.seed = None
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
                for idx in range(len(self.enzymes)):
                        enzyme = self.enzymes[idx]
                        found = False
                        for e in self.enzyme_xml:
                                if e['id'] == enzyme['id']:
                                        e['label'] = enzyme['label']
                                        if not enzyme['label'] in self.labels:
                                                self.labels.append(enzyme['label'])
                                        self.enzymes[idx] = e
                                        found = True
                                        break
                        if not found:
                                print('Unkown nicking enzyme: ' + enzyme['id'])
                                exit()
