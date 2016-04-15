import random
from bisect import bisect_left

def randgeometric(mu):
        return int(random.expovariate(1.0 / mu))

def strand():
        return random.randint(0, 1)

def knick_position(mu, sd):
        pos = random.gauss(mu, sd)
        return pos

def false_positive(fprate):
        return random.expovariate(fprate / 100000)

def false_positives(fprate, length):
        fp = []
        false_knick_pos = false_positive(fprate)
        while false_knick_pos < length:
                #generate FP's on random strand
                fp.append((false_knick_pos, strand()))
                false_knick_pos += false_positive(fprate)
        return fp

def fragile_sites(molecule, length): # TODO
        # note that this breaks molecules after the size has been sampled
        # this might mess up the molecule size distribution ...
        return ([(molecule, length)])

def create_chimera(l1, m1, l2, m2):
        l1 = l1 #TODO what intermolecular distance should be added
        for k in m2:
                m1.append((l1 + k[0], k[1]))
        l1 += l2
        return l1, m1

def generate_molecule(knicks, size, settings):
        knicks = list(knicks)
        shift = random.randint(0, size - 1)
        length = randgeometric(settings.avg)
        if length > size:
                return  ([-1], [])
        end = shift + length
        if not settings.circular and end >= size:
                return  ([-1], [])
        idx = bisect_left(knicks, (shift, None))
        molecule = []
        fp = false_positives(settings.fprate, length)
        while len(fp) > 0 or (idx < len(knicks) and knicks[idx][0] < end):
                if len(fp) != 0 and (idx >= len(knicks) or fp[0][0] < knicks[idx][0] - shift):
                        molecule.append(fp.pop(0))
                else:
                        if random.random() < settings.fnrate:
                                pos = knick_position(knicks[idx][0] - shift, settings.sd)
                                if 0 <= pos and pos <= length - 1:
                                        molecule.append((pos, knicks[idx][1]))
                        idx += 1
                        if settings.circular and idx == len(knicks):
                                idx = 0
                                end -= size
                                shift -= size
        res = []
        for m, l in fragile_sites(molecule, length):
                if len(m) > 0:
                        res.append(([l], m))
        if len(res) > 0:
                idx = random.randint(0, len(res) - 1)
                return res[idx]
        else:
                return ([-1], [])

def generate_molecules(seqLens, fks, rcks, settings):
        seqCount = len(seqLens)
        cumSeqLens = [sum(seqLens[:k + 1]) for k in range(seqCount)]
        chimera = [False, -1, None]
        size = 0
        while size < settings.coverage * cumSeqLens[-1]:
                idx = bisect_left(cumSeqLens, random.random() * cumSeqLens[-1])
                i, m = generate_molecule(fks[idx] if strand() else rcks[idx], seqLens[idx], settings)
                l = i[0]
                if chimera[0]:
                        l, m = create_chimera(chimera[1], chimera[2], l, m)
                if random.random() < settings.chimrate:
                        chimera = [True, l, m]
                else:
                        chimera = [False, -1, None]
                        if l >= settings.min_mol_len:
                                size += l
                                # remove strand information
                                m = zip(*m)[0]
                                yield l, m

