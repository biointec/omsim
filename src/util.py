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


# Knuth-Morris-Pratt string matching
# David Eppstein, UC Irvine, 1 Mar 2002
#from http://code.activestate.com/recipes/117214/
def KnuthMorrisPratt(text, pattern):
        '''Yields all starting positions of copies of the pattern in the text.
        Calling conventions are similar to string.find, but its arguments can be
        lists or iterators, not just strings, it returns all matches, not just
        the first one, and it does not need the whole text in memory at once.
        Whenever it yields, it will have read the text exactly up to and including
        the match that caused the yield.'''
        # allow indexing into pattern and protect against change during yield
        pattern = list(pattern)
        # build table of shift amounts
        shifts = [1] * (len(pattern) + 1)
        shift = 1
        for pos in range(len(pattern)):
                while shift <= pos and pattern[pos] != pattern[pos - shift]:
                        shift += shifts[pos - shift]
                shifts[pos + 1] = shift
        # do the actual search
        startPos = 0
        matchLen = 0
        for c in text:
                while matchLen == len(pattern) or \
                      matchLen >= 0 and pattern[matchLen] != c:
                        startPos += shifts[matchLen]
                        matchLen -= shifts[matchLen]
                matchLen += 1
                if matchLen == len(pattern):
                        yield startPos


