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

from util import double_stranded_multi_KMP_

def nicks(seq, enzymes):
        f = [];
        r = [];
        for pos, rev in double_stranded_multi_KMP_(seq, enzymes):
                f.append(pos)
                r.append(rev)
        return f, list(reversed(r))

def index_sequence(seq, settings):
        max_pattern_len = max([len(e['pattern']) for e in settings.enzymes])
        seqLen = len(seq)
        if settings.circular:
                seq += seq[0:max_pattern_len]
        fk, rck = nicks(seq, settings.enzymes)
        #remove duplicate hits
        if len(fk) > 0:
                while fk[-1][0] >= seqLen:
                        fk.pop()
        if len(fk) > 0:
                while rck[-1][0] >= seqLen:
                        rck.pop()
        return fk, rck
