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
        def __init__(self):
                self.patterns = []
                self.circular = False
                self.min_mol_len = 20000
                self.max_mol_len = 2500000
                self.avg_len = 200000.0
                self.num_fails = 3.0
                self.coverage = 0
                self.chips = 1
                self.fprate = 1.0 #number of fp in 100kb
                self.bns_version = '0.1'
                self.bnx_version = '1.2'
                self.fnrate = 0.15 #fn rate of true labels
                self.chimera_rate = 0.01 #rate of chimeric reads
                self.chimera_mu = 1500 #mean of chimera insert distribution
                self.chimera_sigma = 500 #sd of chimera insert distribution
                self.sd = 50 #sd of knick position
                self.fragile_same = 50
                self.fragile_opposite = 150
                self.fragile_treshold = 25
                self.fragile_factor = 3
                self.label_mu = 1500
                self.label_treshold = 500
                self.label_factor = 100
                #TODO stretchfactor = .85
                self.chip_size = 50000000000 # 50 Gbp
                self.min_knicks = 1
                self.seed = None

        def __str__(self):
                s = ''
                s += 'BNS version: ' + self.bns_version + '\n'
                s += 'BNX version: ' + self.bnx_version + '\n'
                s += 'Patterns: ' + ' '.join(self.patterns) + '\n'
                if self.circular:
                        s += 'Circular genome.\n'
                s += 'Minimal molecule length: ' + str(self.min_mol_len) + ' bp\n'
                s += 'Average molecule length: ' + str(self.avg_len) + ' bp\n'
                s += 'Number of failures for negative binomial length distribution: ' + str(self.num_fails) + '\n'
                s += 'Minimal coverage: ' + str(self.coverage) + 'x\n'
                s += 'FP rate: ' + str(self.fprate) + ' / 100 kbp\n'
                s += 'FN rate: ' + str(self.fnrate * 100) + '%\n'
                s += 'Chimera rate: ' + str(self.chimera_rate * 100) + '%\n'
                if self.seed is not None:
                        s += 'Random seed: ' + str(self.seed) + '\n'
                
                return s





