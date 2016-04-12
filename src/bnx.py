def bnx_header(ofile, bnx_version, pattern, min_mol_len):
        '''
        Writes the bnx-header
        '''
        ofile.write('# BNX File Version: ' + bnx_version + '\n')
        ofile.write('# Label Channels:\n')
        ofile.write('# Nickase Recognition: ' + pattern + '\n')
        ofile.write('# Min Molecule Length (Kb): ' + min_mol_len + '\n')
        ofile.write('# Label SNR Filter Type:\n')
        ofile.write('# Min Label SNR:\n') #avg signal to noise ratio for new chip is ~12
        ofile.write('# Software Version:\n')
        ofile.write('# rh\n')
        ofile.write('# Run Data\n')
        ofile.write('# 0h\n')
        ofile.write('# 0f\n')
        ofile.write('# 1h\n')
        ofile.write('# 1f\n')
        ofile.write('# Qh\n')
        ofile.write('# Qf\n')

def sim_qx11():#TODO
        return str(12)

def sim_qx12():#TODO
        return str(0.1)

def bnx_entry(knicks, ofile):
        backbone = '0'
        channel = '1'
        q1 = 'QX11'
        q2 = 'QX12'
        for pos in knicks:
                channel += '\t' + str(pos)
                q1 += '\t' + sim_qx11()
                q2 += '\t' + sim_qx12()
        ofile.write(backbone + '\n')
        ofile.write(channel + '\n')
        ofile.write(q1 + '\n')
        ofile.write(q2 + '\n')
