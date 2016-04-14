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


base_complements = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}

def complement_list(seq):
        bases = list(seq) 
        return [base_complements.get(base, base) for base in bases]

def complement(seq):
        return ''.join(complement_list(seq))


def reverse_complement(seq):
        return ''.join(reversed(complement_list(seq)))

def double_stranded_multi_KMP(seq, patterns):
        patterns = [pattern for pattern in patterns] + [reverse_complement(pattern) for pattern in patterns]
        for pos, rev in multi_KMP(seq, patterns):
                yield pos, rev

def multi_KMP(seq, patterns):
        count = len(patterns)
        sizes = [len(pattern) for pattern in patterns]
        reverses = [len(seq) - sizes[i] for i in range(count)]
        # allow indexing into patterns
        patterns = [list(pattern) for pattern in patterns]
        # build table of shifts
        shifts = []
        shift = [1] * count
        for i in range(count):
                shifts.append([1] * (sizes[i] + 1))
                for pos in range(sizes[i]):
                        while shift[i] <= pos and patterns[i][pos] != patterns[i][pos - shift[i]]:
                                shift[i] += shifts[i][pos - shift[i]]
                        shifts[i][pos + 1] = shift[i]
        # search for patterns
        startPos = [0] * count
        matchLen = [0] * count
        for c in seq:
                for i in range(count):
                        while matchLen[i] == sizes[i] or matchLen[i] >= 0 and patterns[i][matchLen[i]] != c:
                                startPos[i] += shifts[i][matchLen[i]]
                                matchLen[i] -= shifts[i][matchLen[i]]
                        matchLen[i] += 1
                        if matchLen[i] == sizes[i]:
                                yield startPos[i], reverses[i] - startPos[i]


