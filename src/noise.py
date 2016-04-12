import random

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

def sim_molecules(size, avg):
        '''
        returns end positions of the molecules
        '''
        pos = 0
        while pos < size:
                pos += randgeometric(avg)
                yield pos
        yield size

def knick_molecules(knicks, size, avg, fprate, fnrate, circular = 0):
        knicks = list(knicks)
        molecules = sim_molecules(size, avg)
        shift = 0
        if circular:
                shift = random.randint(0, size - 1)
        index = 0
        while index + 1 < len(knicks) and shift > knicks[index + 1]:
                #skip until we passed the circular shift
                index += 1
        prev = shift
        for end in molecules:
                molecule = []
                fp = []
                false_knick_pos = randgeometric(fprate)
                while false_knick_pos < end - prev:
                        #FP
                        fp.append(false_knick_pos)
                        false_knick_pos += randgeometric(fprate)
                while len(fp) > 0 or (index < len(knicks) and knicks[index] < shift + end):
                        if len(fp) == 0:
                                if random.randint(0, fnrate) != 0:
                                        molecule.append(knicks[index] - prev)
                                index += 1
                        elif index >= len(knicks) or fp[0] < knicks[index] - prev:
                                molecule.append(fp.pop(0))
                        else:
                                if random.randint(0, fnrate) != 0:
                                        molecule.append(knicks[index] - prev)
                                index += 1
                if(len(molecule) > 0):
                        yield molecule
                prev = end

def strand():
        return random.randint(0, 1)

