#!/usr/bin/python
import sys
from KMP import KnuthMorrisPratt as KMP
from readFasta import fasta_parse as RF
from reverseComplement import reverse_complement as rc

def knick(seq, pattern):
        for pos in KMP(seq, pattern):
                yield(pos)
def init_bnx():
        ofile.write('# BNX File Version: ' + bnx_version + '\n')
        ofile.write('# Label Channels:\n')
        ofile.write('# Nickase Recognition: ' + pattern + '\n')
        ofile.write('# Min Molecule Length (Kb): ' + min_mol_len + '\n')
        ofile.write('# Label SNR Filter Type:\n')
        ofile.write('# Min Label SNR:\n')                                       #avg signal to noise ratio for new chip is ~12
        ofile.write('# Software Version:\n')
        ofile.write('# rh\n')
        ofile.write('# Run Data\n')
        ofile.write('# 0h\n')
        ofile.write('# 0f\n')
        ofile.write('# 1h\n')
        ofile.write('# 1f\n')
        ofile.write('# Qh\n')
        ofile.write('# Qf\n')
def sim_qx11():
        return str(12)
def sim_qx12():
        return str(0.1)
def sim_bnx_entry(seq, pattern):
        backbone = '0'
        channel = '1'
        q1 = 'QX11'
        q2 = 'QX12'
        for pos in knick(seq, pattern):
                channel += '\t' + str(pos)
                q1 += '\t' + sim_qx11()
                q2 += '\t' + sim_qx12()
        ofile.write(backbone + '\n')
        ofile.write(channel + '\n')
        ofile.write(q1 + '\n')
        ofile.write(q2 + '\n')

ifname = sys.argv[1]
pattern = sys.argv[2]
min_mol_len = sys.argv[3] #kb
ofile = open(ifname + ".bnx", 'w')
bnx_version = '1.2'
init_bnx()
for meta, seq in RF(ifname):
        sim_bnx_entry(seq, pattern)
        sim_bnx_entry(rc(seq), pattern)
