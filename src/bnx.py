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

def write_bnx_header(ofile, settings, label):
        '''
        Writes the bnx-header
        '''
        ofile.write('# omsim Version:\t' + settings.version + '\n')
        ofile.write('# BNX File Version:\t' + settings.bnx_version + '\n')
        ofile.write('# Label Channels:\t' + '1' + '\n')
        for i in range(len(settings.enzymes)):
                if settings.enzymes[i]['label'] == label:
                        ofile.write('# Nickase Recognition Site ' + str(i + 1) + ':\t' + settings.enzymes[i]['pattern'] + '\n')
        ofile.write('# Bases per Pixel:\t' + '500' + '\n')
        ofile.write('# Min Molecule Length (Kb):\t' + str(settings.min_mol_len) + '\n')
        ofile.write('# Label SNR Filter Type:\t' + '\n')
        ofile.write('# Min Label SNR:\t' + '\n') #avg signal to noise ratio for new chip is ~12
        ofile.write('# Software Version:\t' + '\n')
        ofile.write('#rh\t' + 'SourceFolder\tInstrumentSerial\tTime\tNanoChannelPixelsPerScan\tStretchFactor\tBasesPerPixel\tNumberofScans\tChipId\tFlowCell\tLabelSNRFilterType\tMinMoleculeLength\tMinLabelSNR\tRunId\n')
        ofile.write('# Run Data\t' + '\n') #TODO
        ofile.write('# Number of Molecules:	34292' + '\n')
        ofile.write('#0h LabelChannel	MoleculeID	Length	AvgIntensity	SNR	NumberofLables	OriginalMoleculeId	ScanNumber	ScanDirection	ChipId	Flowcell	RunId	GlobalScanNumber' + '\n')
        ofile.write('#0f int	 int	 float	float	float	int	int	int	int	string	int	int	int' + '\n')
        ofile.write('#1h LabelChannel	LabelPositions[N]' + '\n')
        ofile.write('#1f int	float' + '\n')
        ofile.write('#Qh QualityScoreID	QualityScores[N]' + '\n')
        ofile.write('#Qf string	float[N]' + '\n')
        ofile.write('# Quality Score QX11: Label SNR for channel 1' + '\n')
        ofile.write('# Quality Score QX12: Label Intensity for channel 1' + '\n')

def sim_qx11():#TODO
        return 10

def sim_qx12():#TODO
        return 10

def get_backbone_info(moleculeID, length, count):
        info = []
        info.append(0)          #backboneLabelChannel   #0
        info.append(moleculeID) #ID                     #1
        info.append(length)     #length                 #2
        info.append(0)          #avgIntensity           #3
        info.append(0)          #SNR                    #4
        info.append(count)      #NumberofLables         #5
        info.append(moleculeID) #OriginalMoleculeId     #6
        info.append(1)          #ScanNumber             #7
        info.append(-1)         #ScanDirection          #8
        info.append('unknown')  #ChipId                 #9
        info.append(1)          #Flowcell               #10
        info.append(1)          #RunId                  #11
        info.append(1)          #GlobalScanNumber       #12
        return info

def write_bnx_entry(info, nicks, ofile, label):
        info = get_backbone_info(info[0], info[1], len(nicks))
        backbone = ''
        backbone += str(info[0]) + '\t'                         #backboneLabelChannel   0
        backbone += str(info[1]) + '\t'                         #ID                     1
        backbone += str('{0:.2f}'.format(info[2])) + '\t'       #length                 219254.00
        backbone += str('{0:.2f}'.format(info[3])) + '\t'       #avgIntensity           0.00
        backbone += str('{0:.2f}'.format(info[4])) + '\t'       #SNR                    0.00
        backbone += str(info[5]) + '\t'                         #NumberofLables         15
        backbone += str(info[6]) + '\t'                         #OriginalMoleculeId     1
        backbone += str(info[7]) + '\t'                         #ScanNumber             1
        backbone += str(info[8]) + '\t'                         #ScanDirection          -1
        backbone += str(info[9]) + '\t'                         #ChipId                 unknown
        backbone += str(info[10]) + '\t'                        #Flowcell               1
        backbone += str(info[11]) + '\t'                        #RunId                  1
        backbone += str(info[12]) + '\t'                        #GlobalScanNumber       1
        channel = '1'
        q1 = 'QX11'
        q2 = 'QX12'
        for pos in nicks:
                if pos[1]['label'] == label:
                        channel += '\t' + '{0:.2f}'.format(pos[0])
                        q1 += '\t' + '{0:.4f}'.format(sim_qx11())
                        q2 += '\t' + '{0:.4f}'.format(sim_qx12())
        ofile.write(backbone + '\n')
        ofile.write(channel + '\n')
        ofile.write(q1 + '\n')
        ofile.write(q2 + '\n')
