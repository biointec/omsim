'''
        Copyright (C) 2016 Giles Miclotte (giles.miclotte@ugent.be)
        This file is part of OMSim

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

class Nicks:
        def __init__(self):
                self.nicks = {}
        
        def add_nick(self, enzyme, fwd, nick):
                if not enzyme in self.nicks.keys():
                        self.nicks[enzyme] = {False: [], True: []}
                self.nicks[enzyme][fwd].append(nick)
        
        def get_nicks(self, enzyme, fwd):
                if enzyme in self.nicks.keys():
                        return self.nicks[enzyme][fwd]
                return []
        
        def check(self, seq_len):
                for enzyme in self.nicks.keys():
                        for b in [False, True]:
                                while len(self.nicks[enzyme][b]) > 0 and self.nicks[enzyme][b][-1] >= seq_len:
                                        self.nicks[enzyme][b].pop()
        
        def count(self):
                count = 0
                for enzyme in self.nicks.keys():
                        for b in [False, True]:
                                count += len(self.nicks[enzyme][b])
                return count

class Cmap:
        def __init__(self, iname):
                self.iname = iname
                self.seqs = []
                self.seq_lens = []
                self.nicks = []
                self.base_count = 0
                self.enzymes = []
        
        def add_enzyme(self, enzyme):
                if not enzyme in self.enzymes:
                        self.enzymes.append(enzyme)
        
        def add_meta(self, seq_idx, seq, seq_len):
                        if seq_idx == len(self.seqs):
                                self.seqs.append(seq)
                                self.seq_lens.append(seq_len)
        
        def add_nick(self, seq_idx, enzyme=None, fwd=None, nick=None):
                while seq_idx >= len(self.nicks):
                        n = Nicks()
                        self.nicks.append(n)
                if not nick is None:
                        self.nicks[seq_idx].add_nick(enzyme, fwd, nick)
        
        def add_nicks(self, seq_idx, enzyme, fwd, nicks):
                while seq_idx >= len(self.nicks):
                        n = Nicks()
                        self.nicks.append(n)
                for nick in nicks:
                        self.add_nick(seq_idx, enzyme, fwd, nick)
        
        def count(self):
                count = 0
                for nicks in self.nicks:
                        count += nicks.count()
                return count
        
        def seq_count(self):
                return len(self.seqs)
        
        def seq_len(self):
                return sum(self.seq_lens)
        
        def check(self):
                for idx in range(len(self.seq_lens)):
                        self.nicks[idx].check(self.seq_lens[idx])
