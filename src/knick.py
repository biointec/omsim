from util import double_stranded_KMP

def double_stranded_knick(seq, pattern):
        for pos in double_stranded_KMP(seq, pattern):
                yield(pos)

def knicks(seq, pattern):
        k = [];
        for pos in double_stranded_knick(seq, pattern):
                k.append(pos)
        return k
