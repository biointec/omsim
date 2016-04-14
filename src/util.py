def fasta_parse(ifname):
        infile = open(ifname)
        key = ''
        val = ''
        for line in infile:
                if line.startswith('>'):
                        if key:
                                yield key, val
                        key, val = line[1:].rstrip().split()[0], ''
                elif key:
                        val += line.rstrip()
        if key:
                yield key, val


complements = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}

def complement_list(seq):
        bases = list(seq) 
        return [complements.get(base, base) for base in bases]

def complement(seq):
        return ''.join(complement_list(seq))


def reverse_complement(seq):
        return ''.join(reversed(complement_list(seq)))


def double_stranded_KMP(text, pattern):
        c_pattern = reverse_complement(pattern)
        size = len(pattern)
        # allow indexing into pattern and protect against change during yield
        pattern = list(pattern)
        c_pattern = list(c_pattern)
        # build table of shift amounts
        shifts = [1] * (size + 1)
        shift = 1
        for pos in range(size):
                while shift <= pos and pattern[pos] != pattern[pos - shift]:
                        shift += shifts[pos - shift]
                shifts[pos + 1] = shift
        
        c_shifts = [1] * (size + 1)
        c_shift = 1
        for pos in range(size):
                while c_shift <= pos and c_pattern[pos] != c_pattern[pos - c_shift]:
                        c_shift += c_shifts[pos - c_shift]
                c_shifts[pos + 1] = c_shift
        
        # do the actual search
        startPos = 0
        matchLen = 0
        c_startPos = 0
        c_matchLen = 0
        for c in text:
                while matchLen == size or matchLen >= 0 and pattern[matchLen] != c:
                        startPos += shifts[matchLen]
                        matchLen -= shifts[matchLen]
                matchLen += 1
                if matchLen == size:
                        yield startPos
                while c_matchLen == size or c_matchLen >= 0 and c_pattern[c_matchLen] != c:
                        c_startPos += c_shifts[c_matchLen]
                        c_matchLen -= c_shifts[c_matchLen]
                c_matchLen += 1
                if c_matchLen == size:
                        yield c_startPos




