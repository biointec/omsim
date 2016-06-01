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
HAS_NUMPY = False
#try:
#        import numpy as np
#        HAS_NUMPY = True
#except ImportError:
#        HAS_NUMPY = False

def randgeometric(mu):
        return int(random.expovariate(1.0 / mu))

def randpoisson(lambd):
        if lambd > 10:
                return randpoisson_1(lambd)
        elif lambd == 0:
                return 0
        else:
                return randpoisson_2(lambd)

def randpoisson_1(lambd):
        ls2pi = 0.91893853320467267
        twelfth = 0.083333333333333333333333
        slambd = sqrt(lambd)
        loglambd = log(lambd)
        b = 0.931 + 2.53 * slambd
        a = -0.059 + 0.02483 * b
        invalpha = 1.1239 + 1.1328 / (b - 3.4)
        vr = 0.9277 - 3.6224 / (b - 2)
        while(True):
                U = random.random() - 0.5
                V = random.random()
                us = 0.5 - fabs(U)
                k = floor((2 * a / us + b) * U + lambd + 0.43)
                if us >= 0.07 and V <= vr:
                        return k
                if (k < 0) or (us < 0.013 and V > us):
                        continue
                if log(V) + log(invalpha) - log(a / (us * us) + b) \
                                <= -lambd + k * loglambd - loggam(k + 1):
                        return k


def randpoisson_2(lambd):
        enlambd = exp(-lambd)
        X = 0
        prod = 1.0
        while(True):
                U = random.random()
                prod *= U
                if prod > enlambd:
                        X += 1
                else:
                        return X


def loggam(x):
        '''
        log-gamma function to support some of these distributions. The
        algorithm comes from SPECFUN by Shanjie Zhang and Jianming Jin and their
        book "Computation of Special Functions", 1996, John Wiley & Sons, Inc.
        '''
        a = [8.333333333333333e-02,-2.777777777777778e-03,
             7.936507936507937e-04,-5.952380952380952e-04,
             8.417508417508418e-04,-1.917526917526918e-03,
             6.410256410256410e-03,-2.955065359477124e-02,
             1.796443723688307e-01,-1.39243221690590e+00]
        x0 = x
        n = 0
        if x == 1.0 or x == 2.0:
                return 0.0
        elif x <= 7.0:
                n = int(7 - x)
                x0 = x + n
        x2 = 1.0 / (x0 * x0)
        xp = 2 * pi
        gl0 = a[9]
        for k in range(8, 0, -1):
                gl0 *= x2
                gl0 += a[k]
        gl = gl0 / x0 + 0.5 * log(xp) + (x0 - 0.5) * log(x0) - x0
        if x <= 7.0:
                for k in range(1, n, 1):
                        gl -= log(x0 - 1.0)
                        x0 -= 1.0
        return gl;

def randnegbinom(mu, sd):
        mu = float(mu)
        sd = float(sd)
        r = (mu * mu) / (sd * sd - mu)
        p = 1 - mu / (r + mu)
        if HAS_NUMPY:
                return np.random.negative_binomial(r, p)
        else:
                return randpoisson(1 - p) / p * random.gammavariate(r, 1)


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


def generate_molecule(nicks, size, settings):
        nicks = list(nicks)
        shift = random.randint(0, size - 1)
        length = randnegbinom(settings.avg_mol_len / settings.stretch_factor, settings.sd_mol_len)
        meta = [-1, -1]
        if length > size:
                return (-1, [], [-1, -1])
        if random.random() < 0.5:
                shift = shift - length
                if settings.circular and shift < 0:
                        shift += size
        meta[1] = shift
        end = shift + length
        if shift < 0 or (not settings.circular and end >= size):
                return (-1, [], [-1, -1])
        idx = bisect_left(nicks, (shift,))
        molecule = []
        fp = []
        for enzyme in settings.enzymes:
                fp = fp + false_positives(enzyme['fp'], length, enzyme)
        fp.sort(key=lambda x: x[0], reverse=False)
        while len(fp) > 0 or (idx < len(nicks) and nicks[idx][0] < end):
                if len(fp) != 0 and (idx >= len(nicks) or fp[0][0] < nicks[idx][0] - shift):
                        nick = fp.pop(0)
                        molecule.append(nick)
                else:
                        if random.random() < nicks[idx][2]['fn']:
                                pos = nicks[idx][0] - shift
                                if 0 <= pos and pos <= length - 1:
                                        molecule.append([pos, nicks[idx][1], True, nicks[idx][2]])
                        idx += 1
                        if settings.circular and idx == len(nicks):
                                idx = 0
                                end -= size
                                shift -= size
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
        return randnegbinom(float(mu), float(sigma))


def sim_backbone_SNR():
        return SNR(15, 75)


def sim_label_SNR():
        return SNR(14, 11)
