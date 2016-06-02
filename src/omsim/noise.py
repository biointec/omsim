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
from scipy.stats import invgamma, nbinom

def randgamma(mu, sd):
        a = (mu * mu) / (sd * sd)
        b = (sd * sd) / mu
        return random.gammavariate(a, b)


def randgeometric(mu):
        return int(random.expovariate(1.0 / mu))


def randnegbinom(mu, sd):
        mu = float(mu)
        sd = float(sd)
        r = (mu * mu) / (sd * sd - mu)
        p = 1 - mu / (r + mu)
        return nbinom.rvs(r, p)


def strand():
        return random.randint(0, 1)


def nick_position(p, sd):
        p = list(p)
        if p[2]:
                temp = random.gauss(p[0], sd)
                while temp < 0:
                        temp = random.gauss(p[0], sd)
                p[0] = temp
        return p


def false_positive(fprate):
        return random.expovariate(fprate / 100000)


def false_positives(fprate, length, enzyme):
        fp = []
        false_nick_pos = false_positive(fprate)
        while false_nick_pos < length:
                # generate FP's on random strand
                fp.append((false_nick_pos, strand(), False, enzyme))
                false_nick_pos += false_positive(fprate)
        return fp


def sigmoid(m, f, x):
        '''
        computes the value of a sigmoid around m at position x, with factor f
        '''
        return 1 - 1 / (1 + exp((m - x) / f))


def break_fragile(prev, curr, settings):
        if prev[1] == curr[1]:
                cutoff = settings.fragile_same
        else:
                cutoff = settings.fragile_opposite
        dist = curr[0] - prev[0]
        if dist < cutoff - settings.fragile_treshold:
                # don't break, nicks are so close that molecule does not become fragile
                return False
        elif cutoff + settings.fragile_treshold < dist:
                # don't break, nicks are too far apart for molecule to become fragile
                return False
        else:
                # break if roll is smaller than chance
                return random.random() < sigmoid(cutoff, settings.fragile_factor, dist)


def fragile_sites(l, m, settings):
        '''
        fragile sites are independent of label and pattern
        '''
        if len(m) == 0:
                return (l, m)
        idx = 1
        while idx < len(m):
                if break_fragile(m[idx - 1], m[idx], settings):
                        return [1 + int(m[idx - 1][0]), m[:idx - 1]]
                idx += 1
        return (l, m)


def create_chimera(l1, m1, meta1, l2, m2, meta2, settings):
        l1 = l1 + max(0, int(random.gauss(settings.chimera_mu, settings.chimera_sigma)))
        m1 = m1 + [[l1 + k[0], k[1]] for k in m2]
        l1 += l2
        return l1, m1, meta1 + meta2


def read_position(size, settings):
        shift = random.randint(0, size - 1)
        length = randnegbinom(settings.avg_mol_len / settings.stretch_factor, settings.sd_mol_len / settings.stretch_factor)
        if random.random() < 0.5:
                shift = shift - length
                if settings.circular and shift < 0:
                        shift += size
        end = shift + length
        return shift, length, end


def sort_labels(fp, tp):
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
                        if fp[0][0] < tp[0][0]:
                                molecule.append(fp[f_idx])
                                f_idx += 1
                        else:
                                molecule.append(tp[t_idx])
                                t_idx += 1
        return molecule


def generate_molecule(nicks, size, settings):
        nicks = list(nicks)
        #determine read position
        shift, length, end = read_position(size, settings)
        #abort if improper read position
        if length > size or shift < 0 or (not settings.circular and end >= size):
                return (-1, [], [-1, -1])
        #set meta for bed file
        meta = [-1, shift]
        #generate false positives
        fp = []
        for enzyme in settings.enzymes:
                fp = fp + false_positives(enzyme['fp'], length, enzyme)
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
                if idx == len(nicks) and settings.circular:
                        idx = 0
                        shift -= size
                        end -= size
        #sort labels
        molecule = sort_labels(fp, tp)
        #break at fragile sites
        length, molecule = fragile_sites(length, molecule, settings)
        # remove strand and [T|F]P information and randomise TP
        molecule = [[nick_position(p, settings.nick_sd)[0], p[-1]] for p in molecule]
        return length, molecule, meta


def cut_long_molecule(l, m, settings):
        idx = len(m)
        while idx > 0 and m[idx - 1][0] > settings.max_mol_len:
                idx -= 1
        if idx == 0:
                return (-1, [], [-1, -1])
        l = random.randint(int(m[idx - 1][0]) + 1, settings.max_mol_len) + (l % 1)
        return l, m[:idx - 1]


def merge_labels(m, settings):
        if len(m) == 0:
                return m
        mol = []
        mu = settings.label_mu
        t = settings.label_treshold
        f = settings.label_factor
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
                elif random.random() < sigmoid(mu, f, dist):
                        # merge
                        prev[0] = random.randint(int(prev[0]), int(curr[0])) + (prev[0] % 1)
                else:
                        # don't merge
                        mol.append(prev)
                        prev = curr
        mol.append(prev)
        return mol


def generate_scan(seqLens, fks, rcks, settings):
        seqCount = len(seqLens)
        cumSeqLens = [sum(seqLens[:k + 1]) for k in range(seqCount)]
        chimera = [False, -1, None, [[-1, -1]]]
        size = 0
        while size < settings.get_scan_size():
                idx = bisect_left(cumSeqLens, random.random() * cumSeqLens[-1])
                l = -1
                while l < 0:
                        l, m, meta = generate_molecule(fks[idx] if strand() else rcks[idx], seqLens[idx], settings)
                meta[0] = idx
                meta = [meta]
                if chimera[0]:
                        l, m, meta = create_chimera(chimera[1], chimera[2], chimera[3], l, m, meta, settings)
                if random.random() < settings.chimera_rate:
                        chimera = [True, l, m, meta]
                else:
                        chimera = [False, -1, None, [[-1, -1]]]
                        m = merge_labels(m, settings)
                        if settings.max_mol_len < l:
                                l, m = cut_long_molecule(l, m, settings)
                        if settings.min_mol_len <= l:
                                size += l
                                yield l, m, meta


def chip_stretch_factor(settings):
        return random.gauss(settings.stretch_factor, settings.stretch_chip_sd)


def scan_stretch_factor(chip_stretch, settings):
        return random.gauss(chip_stretch, settings.stretch_scan_sd)


def intensity(mu, sigma):
        result = -1
        while result < 0 or result > 1:
                result = random.gauss(float(mu), float(sigma))
        return result


def sim_average_intensity():
        return intensity(.3, .2)


def sim_label_intensity():
        return intensity(0.07, 0.04)


def SNR(mu, sigma):
        t = (mu * mu) / (sigma * sigma)
        a = 2 + t
        b = mu * (1 + t)
        return invgamma.rvs(a, scale = b)


def sim_backbone_SNR():
        return SNR(15, 75)


def sim_label_SNR():
        return SNR(14, 11)
