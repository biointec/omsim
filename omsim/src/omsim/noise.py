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

import random
from bisect import bisect_left
from math import exp, sqrt, log, fabs, floor, pi
import numpy as np
from scipy.stats import invgamma, nbinom, norm, describe


class Noise:
        def __init__(self, settings):
                self.settings = settings
                self.m_size = []
                self.m_size_idx = -1
                self.m_size_len = 0
                self.l_SNR = []
                self.l_SNR_idx = -1
                self.l_SNR_len = 0
                self.l_AI = []
                self.l_AI_idx = -1
                self.l_AI_len = 0
                self.m_SNR = []
                self.m_SNR_idx = -1
                self.m_SNR_len = 0
                self.m_AI = []
                self.m_AI_idx = -1
                self.m_AI_len = 0
                # set seeds
                random.seed(self.settings.seed)
                np.random.seed(self.settings.seed)
        
        
        def randgamma(self, mu, sd):
                a = (mu * mu) / (sd * sd)
                b = (sd * sd) / mu
                return random.gammavariate(a, b)
        
        
        def randgeometric(self, mu):
                return int(random.expovariate(1.0 / mu))
        
        
        def strand(self):
                return random.randint(0, 1)==0
        
        
        def nick_position(self, p, sd):
                p = list(p)
                if p[2]:
                        temp = random.gauss(p[0], sd)
                        while temp < 0:
                                temp = random.gauss(p[0], sd)
                        p[0] = temp
                return p
        
        
        def false_positive(self, fprate):
                return random.expovariate(fprate / 100000)
        
        
        def false_positives(self, fprate, length, enzyme):
                fp = []
                false_nick_pos = self.false_positive(fprate)
                while false_nick_pos < length:
                        # generate FP's on random strand
                        fp.append([int(false_nick_pos), self.strand(), False, enzyme])
                        false_nick_pos += self.false_positive(fprate)
                return fp
        
        
        def sigmoid(self, m, f, x):
                '''
                computes the value of a sigmoid around m at position x, with factor f
                '''
                return 1 - 1 / (1 + exp((m - x) / f))
        
        
        def break_fragile(self, prev, curr):
                if prev[1] == curr[1]:
                        cutoff = self.settings.fragile_same
                else:
                        cutoff = self.settings.fragile_opposite
                dist = curr[0] - prev[0]
                if dist < cutoff - self.settings.fragile_treshold:
                        # don't break, nicks are so close that molecule does not become fragile
                        return False
                elif cutoff + self.settings.fragile_treshold < dist:
                        # don't break, nicks are too far apart for molecule to become fragile
                        return False
                else:
                        # break if roll is smaller than chance
                        return random.random() < self.sigmoid(cutoff, self.settings.fragile_factor, dist)
        
        
        def fragile_sites(self, l, m):
                '''
                fragile sites are independent of label and pattern
                '''
                if len(m) == 0:
                        return (l, m)
                idx = 1
                while idx < len(m):
                        if self.break_fragile(m[idx - 1], m[idx]):
                                return [1 + int(m[idx - 1][0]), m[:idx - 1]]
                        idx += 1
                return (l, m)
        
        
        def create_chimera(self, l1, m1, meta1, l2, m2, meta2):
                l1 = l1 + max(0, int(random.gauss(self.settings.chimera_mu, self.settings.chimera_sigma)))
                m1 = m1 + [[l1 + k[0], k[1]] for k in m2]
                l1 += l2
                return l1, m1, meta1 + meta2
        
        
        def read_position(self, size):
                shift = random.randint(0, size - 1)
                length = self.next_m_size()
                if random.random() < 0.5:
                        shift = shift - length
                        if self.settings.circular and shift < 0:
                                shift += size
                end = shift + length
                return shift, length, end
        
        
        def sort_labels(self, fp, tp):
                molecule = []
                t_idx = 0
                f_idx = 0
                while f_idx < len(fp) or t_idx < len(tp):
                        if f_idx == len(fp):
                                molecule.append(tp[t_idx])
                                t_idx += 1
                        elif t_idx == len(tp):
                                molecule.append(fp[f_idx])
                                f_idx += 1
                        else:
                                if fp[f_idx][0] < tp[t_idx][0]:
                                        molecule.append(fp[f_idx])
                                        f_idx += 1
                                else:
                                        molecule.append(tp[t_idx])
                                        t_idx += 1
                return molecule
        
        
        def generate_molecule(self, nicks, size):
                #determine read position
                shift, length, end = self.read_position(size)
                #abort if improper read position
                if length > size or shift < 0 or (not self.settings.circular and end >= size):
                        return (-1, [], [-1, -1])
                #set meta for bed file
                meta = [-1, shift]
                #generate false positives
                fp = []
                for eid in self.settings.enzymes:
                        enzyme = self.settings.enzymes[eid]
                        fp = fp + self.false_positives(enzyme['fp'], length, enzyme)
                fp.sort(key=lambda x: x[0], reverse=False)
                #determine true positives
                tp = []
                idx = bisect_left(nicks, (shift,))
                while idx < len(nicks) and nicks[idx][0] < end:
                        r = random.random()
                        fn_rate = nicks[idx][2]['fn']
                        if r > fn_rate:
                                pos = nicks[idx][0] - shift
                                tp.append([pos, nicks[idx][1], True, nicks[idx][2]])
                        idx += 1
                        if idx == len(nicks) and self.settings.circular:
                                idx = 0
                                shift -= size
                                end -= size
                #sort labels
                molecule = self.sort_labels(fp, tp)
                #break at fragile sites
                length, molecule = self.fragile_sites(length, molecule)
                # remove strand and [T|F]P information and randomise TP
                molecule = [[self.nick_position(p, self.settings.nick_sd)[0], p[-1]] for p in molecule]
                molecule = [p for p in molecule if p[0] < length]
                return length, molecule, meta
        
        
        def cut_long_molecule(self, l, m):
                idx = len(m)
                while idx > 0 and m[idx - 1][0] > self.settings.max_mol_len:
                        idx -= 1
                if idx == 0:
                        return (-1, [], [-1, -1])
                l = random.randint(int(m[idx - 1][0]) + 1, self.settings.max_mol_len) + (l % 1)
                return l, m[:idx - 1]
        
        
        def merge_labels(self, m):
                if len(m) == 0:
                        return m
                mol = []
                mu = self.settings.label_mu
                t = self.settings.label_treshold
                f = self.settings.label_factor
                prev = None
                for curr in m:
                        if prev is None:
                                prev = curr
                                continue
                        if prev[0] > curr[0]:
                                temp = prev
                                prev = curr
                                curr = temp
                        dist = curr[0] - prev[0]
                        if dist < mu - t:
                                # merge
                                prev[0] = random.randint(int(prev[0]), int(curr[0])) + (prev[0] % 1)
                        elif mu + t < dist:
                                # don't merge
                                mol.append(prev)
                                prev = curr
                        elif random.random() < self.sigmoid(mu, f, dist):
                                # merge
                                prev[0] = random.randint(int(prev[0]), int(curr[0])) + (prev[0] % 1)
                        else:
                                # don't merge
                                mol.append(prev)
                                prev = curr
                mol.append(prev)
                return mol
        
        
        def generate_scan(self, seqLens, fks, rcks):
                seqCount = len(seqLens)
                cumSeqLens = [sum(seqLens[:k + 1]) for k in range(seqCount)]
                chimera = [False, -1, None, [[-1, -1]]]
                size = 0
                while size < self.settings.get_scan_size():
                        idx = bisect_left(cumSeqLens, random.random() * cumSeqLens[-1])
                        l = -1
                        while l < 0:
                                l, m, meta = self.generate_molecule(fks[idx] if self.strand() else rcks[idx], seqLens[idx])
                        meta[0] = idx
                        meta = [meta]
                        if chimera[0]:
                                l, m, meta = self.create_chimera(chimera[1], chimera[2], chimera[3], l, m, meta)
                        if random.random() < self.settings.chimera_rate:
                                chimera = [True, l, m, meta]
                        else:
                                chimera = [False, -1, None, [[-1, -1]]]
                                m = self.merge_labels(m)
                                if self.settings.max_mol_len < l:
                                        l, m = self.cut_long_molecule(l, m)
                                if self.settings.min_mol_len <= l:
                                        size += l
                                        yield l, m, meta
        
        
        def chip_stretch_factor(self):
                return random.gauss(self.settings.stretch_factor, self.settings.stretch_chip_sd)
        
        
        def scan_stretch_factor(self, chip_stretch):
                return random.gauss(chip_stretch, self.settings.stretch_scan_sd)
        
        
        def mol_stretch_factor(self, scan_stretch):
                return random.gauss(scan_stretch, self.settings.stretch_mol_sd)
        
        
        def intensity(self, mu, sd, size):
                mu = float(mu)
                sd = float(sd)
                result = norm.rvs(mu, scale=sd, size=size)
                #print('norm', describe(result))
                return result
        
         
        
        def SNR(self, mu, sd, size):
                mu = float(mu)
                sd = float(sd)
                t = 1.0 + (mu * mu) / (sd * sd)
                a = 1.0 + t
                b = mu * t
                result = invgamma.rvs(a, scale=b, size=size)
                #result = [1.0 / random.gammavariate(a, 1.0 / b) for i in range(int(size))]
                #print('invgamma', describe(result))
                return result
        
        
        def randnegbinom(self, mu, sd, size):
                mu = float(mu)
                sd = float(sd)
                r = (mu * mu) / (sd * sd - mu)
                p = 1 - mu / (r + mu)
                result = nbinom.rvs(r, p, size=size)
                #print('nbinom', describe(result))
                return result
        
        
        def next_m_size(self):
                self.m_size_idx += 1
                if self.m_size_idx == self.m_size_len:
                        self.m_size = self.randnegbinom(self.settings.avg_mol_len,
                                                        self.settings.sd_mol_len,
                                                        self.settings.sim_batch_size)
                        self.m_size_idx = 0
                        self.m_size_len = len(self.m_size)
                return self.m_size[self.m_size_idx]
        
        
        def next_m_SNR(self):
                self.m_SNR_idx += 1
                if self.m_SNR_idx == self.m_SNR_len:
                        self.m_SNR = self.SNR(self.settings.molecule_SNR_mu, self.settings.molecule_SNR_sd, self.settings.sim_batch_size)
                        self.m_SNR_idx = 0
                        self.m_SNR_len = len(self.m_SNR)
                return self.m_SNR[self.m_SNR_idx]
        
        
        def next_l_SNR(self):
                self.l_SNR_idx += 1
                if self.l_SNR_idx == self.l_SNR_len:
                        self.l_SNR = self.SNR(self.settings.label_SNR_mu, self.settings.label_SNR_sd, 10 * self.settings.sim_batch_size)
                        self.l_SNR_idx = 0
                        self.l_SNR_len = len(self.l_SNR)
                return self.l_SNR[self.l_SNR_idx]
        
        
        def next_m_AI(self):
                self.m_AI_idx += 1
                if self.m_AI_idx == self.m_AI_len:
                        self.m_AI = self.intensity(self.settings.molecule_AI_mu, self.settings.molecule_AI_sd, self.settings.sim_batch_size)
                        self.m_AI_idx = 0
                        self.m_AI_len = len(self.m_AI)
                result = self.m_AI[self.m_AI_idx]
                if result < 0 or 1 < result:
                        return self.next_m_AI()
                else:
                        return result
        
        
        def next_l_AI(self):
                self.l_AI_idx += 1
                if self.l_AI_idx == self.l_AI_len:
                        self.l_AI = self.intensity(self.settings.label_AI_mu, self.settings.label_AI_sd, 10 * self.settings.sim_batch_size)
                        self.l_AI_idx = 0
                        self.l_AI_len = len(self.l_AI)
                result = self.l_AI[self.l_AI_idx]
                if result < 0 or 1 < result:
                        return self.next_l_AI()
                else:
                        return result
