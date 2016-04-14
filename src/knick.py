from util import double_stranded_multi_KMP

def knicks(seq, patterns):
        f = [];
        r = [];
        for pos, rev in double_stranded_multi_KMP(seq, patterns):
                f.append(pos)
                r.append(rev)
        return f, list(reversed(r))

def index_sequence(seq, circular, patterns):
        max_pattern_len = max([len(p) for p in patterns])
        seqLen = len(seq)
        if circular:
                seq += seq[0:max_pattern_len]
        fk, rck = knicks(seq, patterns)
        #remove duplicate hits
        while fk[-1][0] >= seqLen:
                fk.pop()
        while rck[-1][0] >= seqLen:
                rck.pop()
        return fk, rck
