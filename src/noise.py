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

def fragile_sites(molecule, length):
        # TODO
        # note that this breaks molecules after the size has been sampled
        # this might mess up the molecule size distribution ...
        return ([(molecule, length)])

def generate_molecule(knicks, size, stats, circular = 0):
        avg, coverage, fprate, fnrate, sd, min_mol_len = stats
        knicks = list(knicks)
        shift = random.randint(0, size - 1)
        length = randgeometric(avg)
        if length > size:
                return  ([-1], [])
        end = shift + length
        if not circular and end >= size:
                return  ([-1], [])
        idx = bisect_left(knicks, (shift, None))
        molecule = []
        fp = false_positives(fprate, length)
        while len(fp) > 0 or (idx < len(knicks) and knicks[idx][0] < end):
                if len(fp) != 0 and (idx >= len(knicks) or fp[0][0] < knicks[idx][0] - shift):
                        molecule.append(fp.pop(0)[0])
                else:
                        if random.random() < fnrate:
                                pos = knick_position(knicks[idx][0] - shift, sd)
                                if 0 <= pos and pos <= length - 1:
                                        molecule.append(pos)
                        idx += 1
                        if circular and idx == len(knicks):
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

def generate_molecules(seqLens, fks, rcks, stats, circular):
        avg, coverage, fprate, fnrate, sd, min_mol_len = stats
        size = 0
        seqCount = len(seqLens)
        cumSeqLens = [sum(seqLens[:k + 1]) for k in range(seqCount)]
        while size < coverage * cumSeqLens[-1]:
                idx = seqCount
                r = random.random() * cumSeqLens[-1]
                while 0 < idx and r < cumSeqLens[idx - 1]:
                        idx -= 1
                i, m = generate_molecule([fks[idx], rcks[idx]][strand()], seqLens[idx], stats, circular[idx])
                l = i[0]
                if l >= min_mol_len:
                        size += l
                        yield l, m

