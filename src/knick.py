from util import double_stranded_multi_KMP

def knicks(seq, patterns):
        f = [];
        r = [];
        for pos, rev in double_stranded_multi_KMP(seq, patterns):
                f.append(pos)
                r.append(rev)
        return f, list(reversed(r))
