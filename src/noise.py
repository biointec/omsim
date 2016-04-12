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

def sim_molecules(size, avg):
        '''
        returns end positions of the molecules
        '''
        pos = 0
        while pos < size:
                pos += random.expovariate(1.0 / avg)
                yield pos
        yield size

def knick_molecules(knicks, size, avg, circular = 0):
        knicks = list(knicks)
        molecules = sim_molecules(size, avg)
        shift = 0
        if circular:
                shift = random.randint(0, size - 1)
        index = 0
        while index + 1 < len(knicks) and shift > knicks[index + 1]:
                #skip until we passed the circular shift
                index += 1
        for end in molecules:
                molecule = []
                while index < len(knicks) and shift + end > knicks[index]:
                        #add knicks in region [shift, shift + end[
                        molecule.append(knicks[index])
                        index += 1
                if(len(molecule) > 0):
                        yield molecule

def strand():
        return random.randint(0, 1)

