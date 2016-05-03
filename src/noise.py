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
from math import exp
import numpy as np

def randgeometric(mu):
        return int(random.expovariate(1.0 / mu))

def randnegbinom(mu, r):
        mu = float(mu)
        r = float(r)
        p = 1 - mu/(r + mu)
        return np.random.negative_binomial(r, p)

def strand():
        return random.randint(0, 1)

def knick_position(p, sd):
        p = list(p)
        if p[2]:
                p[0] = random.gauss(p[0], sd)
        return p

def false_positive(fprate):
        return random.expovariate(fprate / 100000)

def false_positives(fprate, length):
        fp = []
        false_knick_pos = false_positive(fprate)
        while false_knick_pos < length:
                #generate FP's on random strand
                fp.append((false_knick_pos, strand(), False))
                false_knick_pos += false_positive(fprate)
        return fp

def sigmoid(m, f, x):
        '''
        computes the value of a sigmoid around m at position x, with factor f
        '''
        return 1 - 1 / (1 + exp((m - x) / f))

def break_fragile(prev, curr, settings):
        #TODO improve fragile site tolerance
        if prev[1] == curr[1]:
                cutoff = settings.fragile_same
        else:
                cutoff = settings.fragile_opposite
        dist = curr[0] - prev[0]
        if dist < cutoff - settings.fragile_treshold \
           or cutoff + settings.fragile_treshold < dist \
           or random.random() > sigmoid(cutoff, settings.fragile_factor, dist):
                return False
        else:
                return True

def fragile_sites(l, m, settings):
        '''
        fragile sites are independent of label and pattern
        '''
        if len(m) == 0:
                return (l, m)
        idx = 1
        while idx < len(m):
                if break_fragile(m[idx - 1], m[idx], settings):
                        return (m[idx - 1][0], m[:idx - 1])
                idx += 1
        return (l, m)

def create_chimera(l1, m1, l2, m2, settings):
        l1 = l1 + max(0, random.gauss(settings.chimera_mu, settings.chimera_sigma))
        m1 = m1 + [l1 + k for k in m2]
        l1 += l2
        return l1, m1

def generate_molecule(knicks, size, settings):
        knicks = list(knicks)
        shift = random.randint(0, size - 1)
        length = randnegbinom(settings.avg_len, settings.num_fails)
        if length > size:
                return  (-1, [])
        if random.random() < 0.5:
                shift = shift - length
                if settings.circular and shift < 0:
                        shift += size
        end = shift + length
        if not settings.circular and end >= size:
                return  (-1, [])
        idx = bisect_left(knicks, (shift, None))
        molecule = []
        fp = false_positives(settings.fprate, length)
        while len(fp) > 0 or (idx < len(knicks) and knicks[idx][0] < end):
                if len(fp) != 0 and (idx >= len(knicks) or fp[0][0] < knicks[idx][0] - shift):
                        molecule.append(fp.pop(0))
                else:
                        if random.random() < settings.fnrate:
                                pos = knicks[idx][0] - shift
                                if 0 <= pos and pos <= length - 1:
                                        molecule.append((pos, knicks[idx][1], True))
                        idx += 1
                        if settings.circular and idx == len(knicks):
                                idx = 0
                                end -= size
                                shift -= size
        length, molecule = fragile_sites(length, molecule, settings)
        # remove strand and [T|F]P information and randomise TP
        molecule = [knick_position(p, settings.sd)[0] for p in molecule]
        if len(molecule) > settings.min_knicks:
                return length, molecule
        else:
                return (-1, [])

def cut_long_molecule(l, m, settings):
        idx = len(m)
        while idx > 0 and m[idx - 1] > settings.max_mol_len:
                idx -= 1
        if idx == 0:
                return (-1, [])
        l = random.randint(int(m[idx - 1]), settings.max_mol_len) + (l % 1)
        return l, m[:idx - 1]

def generate_molecules(seqLens, fks, rcks, settings):
        seqCount = len(seqLens)
        cumSeqLens = [sum(seqLens[:k + 1]) for k in range(seqCount)]
        chimera = [False, -1, None]
        size = 0
        while size < settings.coverage * cumSeqLens[-1]:
                idx = bisect_left(cumSeqLens, random.random() * cumSeqLens[-1])
                l, m = generate_molecule(fks[idx] if strand() else rcks[idx], seqLens[idx], settings)
                if chimera[0]:
                        l, m = create_chimera(chimera[1], chimera[2], l, m, settings)
                if random.random() < settings.chimera_rate:
                        chimera = [True, l, m]
                else:
                        chimera = [False, -1, None]
                        if settings.max_mol_len < l:
                                l, m = cut_long_molecule(l, m, settings)
                        if settings.min_mol_len <= l:
                                size += l
                                yield l, m

