from util import KnuthMorrisPratt as KMP
from util import reverse_complement as rc

def knick(seq, pattern):
        for pos in KMP(seq, pattern):
                yield(pos)

def f_knicks(seq, pattern):
        fknicks = [];
        for pos in knick(seq, pattern):
                fknicks.append(pos)
        return fknicks

def rc_knicks(seq, pattern):
        rcknicks = [];
        offset = len(seq) - len(pattern)
        for pos in knick(seq, rc(pattern)):
                rcknicks.append(offset - pos)
        return reversed(rcknicks)
