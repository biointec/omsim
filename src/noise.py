import random
from bisect import bisect_left

def fisher_yates(els):
        '''
        Implements the Fisher-Yates shuffle, this yields elements of a list in 
        pseudo-random order. Note that for even rather small len(els), the total
        number of permutations of els is larger than the period of most random 
        number generators; this implies that most permutations of a long list 
        can never be generated.
        '''
        l = list(els)
        while len(l):
                i = random.randint(0, len(l) - 1)
                el = l[i]
                l[i] = l[-1]
                l.pop()
                yield el

def randgeometric(mu):
        return int(random.expovariate(1.0 / mu))

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
        #TODO
        return ([(molecule, length)])

def knick_molecule(knicks, size, avg, fprate, fnrate, sd, circular = 0):
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
        fp = false_positives(fprate, end - shift)
        while len(fp) > 0 or (idx < len(knicks) and knicks[idx][0] < end):
                if len(fp) != 0 and (idx >= len(knicks) or fp[0][0] < knicks[idx][0] - shift):
                        molecule.append(fp.pop(0)[0])
                else:
                        if random.random() < fnrate:
                                pos = knick_position(knicks[idx][0] - shift, sd)
                                if 0 <= pos and pos <= length - 1:
                                        molecule.append(pos)
                        idx += 1
        res = []
        for m, l in fragile_sites(molecule, length):
                if len(m) > 0:
                        res.append(([l], m))
        if len(res) > 0:
                idx = random.randint(0, len(res) - 1)
                return res[idx]
        else:
                return ([-1], [])

def strand():
        return random.randint(0, 1)

