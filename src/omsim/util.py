'''
        Copyright (C) 2016 Giles Miclotte (giles.miclotte@intec.ugent.be)
        This file is part of BioNanoSim

        This program is free software; you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation; either version 2 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program; if not, write to the
        Free Software Foundation, Inc.,
        59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
'''


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


def double_stranded_multi_KMP(seq, enzymes):
        patterns = [e['pattern'] for e in enzymes]
        patterns = [pattern for pattern in patterns] + [reverse_complement(pattern) for pattern in patterns]
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
                                yield (startPos[i], i < count / 2, enzymes[i % (count / 2)]), (reverses[i] - startPos[i], i < count / 2, enzymes[i % (count / 2)])


def double_stranded_multi_KMP_from_fasta(settings):
        '''
                this is truly a monster worth refactoring, probably to a separate class
        '''
        enzymes = settings.enzymes
        patterns = [e['pattern'] for e in enzymes]
        max_pattern_len = max([len(pattern) for pattern in patterns])
        patterns = [pattern for pattern in patterns] + [reverse_complement(pattern) for pattern in patterns]
        count = len(patterns)
        sizes = [len(pattern) for pattern in patterns]
        # reverses = [len(seq) - sizes[i] for i in range(count)]
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
        # output containers
        metas = []
        seq_lens = []
        fs = []
        rcs = []
        # search for patterns
        for iname in settings.files:
                ifile = open(iname)
                c = ifile.read(1)
                f = []
                rc = []
                startPos = [0] * count
                matchLen = [0] * count
                seq_len = 0
                seq = ''
                while c:
                        if c == '>':
                                '''
                                        start of a new sequence
                                '''
                                meta = ifile.readline().rstrip().split()[0]
                                metas.append(meta)
                                print('Indexing sequence: ' + meta)
                        elif c != '\n':
                                '''
                                        process next character of the sequence
                                '''
                                if settings.circular and seq_len < max_pattern_len:
                                        seq += c
                                seq_len += 1
                                for i in range(count):
                                        while matchLen[i] == sizes[i] or matchLen[i] >= 0 and patterns[i][matchLen[i]] != c:
                                                startPos[i] += shifts[i][matchLen[i]]
                                                matchLen[i] -= shifts[i][matchLen[i]]
                                        matchLen[i] += 1
                                        if matchLen[i] == sizes[i]:
                                                f.append((startPos[i], i < count / 2, enzymes[i % int(count / 2)]))
                                                rc.append((- sizes[i] - startPos[i], i < count / 2, enzymes[i % int(count / 2)]))
                        c = ifile.read(1)
                        if seq_len > 0 and (not c or c == '>'):
                                '''
                                        we reached the end of the sequence
                                '''
                                for cc in seq:
                                        for i in range(count):
                                                while matchLen[i] == sizes[i] or matchLen[i] >= 0 and patterns[i][matchLen[i]] != cc:
                                                        startPos[i] += shifts[i][matchLen[i]]
                                                        matchLen[i] -= shifts[i][matchLen[i]]
                                                matchLen[i] += 1
                                                if matchLen[i] == sizes[i]:
                                                        f.append((startPos[i], i < count / 2, enzymes[i % int(count / 2)]))
                                                        rc.append((- sizes[i] - startPos[i], i < count / 2, enzymes[i % int(count / 2)]))
                                if len(f) > 0:
                                        while f[-1][0] >= seq_len:
                                                f.pop()
                                rc = list(reversed([(pos[0] + seq_len, pos[1], pos[2]) for pos in rc]))
                                if len(rc) > 0:
                                        while rc[-1][0] >= seq_len:
                                                rc.pop()
                                print('Found ' + str(len(f)) + ' nicks in ' + str(seq_len) + 'bp.')
                                seq_lens.append(seq_len)
                                fs.append(f)
                                rcs.append(rc)
                                f = []
                                rc = []
                                startPos = [0] * count
                                matchLen = [0] * count
                                seq_len = 0
                                seq = ''
        return [metas, seq_lens, fs, rcs]
