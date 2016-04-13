import random
from bisect import bisect_left

def fisher_yates(els):
        '''
        Implements the Fisher-Yates shuffle, this yields elements of a list in pseudo-random order.
        Note that for even rather small len(els), the total number of permutations of els is larger than the period of most random number generators; this implies that most permutations of a long list can never be generated.
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

def false_positive(rate):
        return random.expovariate(rate / 100000)

def sim_molecules(size, avg):
        '''
        returns end positions of the molecules
        '''
        pos = 0
        while pos < size:
                pos += randgeometric(avg)
                yield pos
        yield size

def knick_position(mu, sd):
        pos = random.gauss(mu, sd)
        return pos

def knick_molecule(knicks, size, avg, fprate, fnrate, sd, circular = 0):
        knicks = list(knicks)
        shift = random.randint(0, size - 1)
        length = randgeometric(avg)
        if length > size:
                return
        end = shift + length
        if not circular and end >= size:
                return
        index = bisect_left(knicks, shift)
        molecule = []
        fp = []
        TP = 0
        FP = 0
        FN = 0
        false_knick_pos = false_positive(fprate)
        while false_knick_pos < end - shift:
                #generate FP's
                fp.append(false_knick_pos)
                false_knick_pos += false_positive(fprate)
        while len(fp) > 0 or (index < len(knicks) and knicks[index] < end):
                if len(fp) != 0 and (index >= len(knicks) or fp[0] < knicks[index] - shift):
                        molecule.append(fp.pop(0))
                        FP += 1
                else:
                        if random.random() < fnrate:
                                pos = molecule.append(knick_position(knicks[index] - shift, sd))
                                if 0 <= pos and pos <= length - 1:
                                        molecule.append(knick_position(knicks[index] - shift, sd))
                                TP += 1
                        else:
                                FN += 1
                        index += 1
        if(len(molecule) > 0):
                yield [length, TP, FP, FN], molecule

def strand():
        return random.randint(0, 1)

