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

from datetime import datetime
from os import path

def write_bnx_header(ofile, settings, label, chip_settings):
        '''
        Writes the bnx-header
        '''
        ofile.write('# BNX File Version:\t' + settings.bnx_version + '\n')
        ofile.write('# Label Channels:\t' + '1' + '\n')
        for i in range(len(settings.enzymes)):
                if settings.enzymes[i]['label'] == label:
                        ofile.write('# Nickase Recognition Site ' + str(i + 1) + ':\t' + settings.enzymes[i]['pattern'] + '\n')
        ofile.write('# Bases per Pixel:\t' + str(int(chip_settings['bpp'])) + '\n')
        ofile.write('# Software Version:\tomsim-' + settings.version + '\n')
        #TODO: run_data
        rh = ''
        run_data = ''
        rh += 'SourceFolder\t'
        run_data += path.dirname(path.realpath(ofile.name)) + '/Detect Molecules\t'
        rh += 'InstrumentSerial\t'
        run_data += 'omsim-' + settings.version + '\t'
        rh += 'Time\t'
        run_data += str(datetime.now()) + '\t'
        rh += 'NanoChannelPixelsPerScan\t'
        run_data += str(int(chip_settings['size'] / chip_settings['scans'] / chip_settings['bpp'])) + '\t' # ~ 1to2 gbp divided by ~500 bpp, so about 2-4Mpixels per scan | total length divided by number of scans...
        rh += 'StretchFactor\t'
        run_data += str(chip_settings['stretch_factor']) + '\t'
        rh += 'BasesPerPixel\t' #500 with stretch .85, so about 425 / stretchfactor
        run_data += str(chip_settings['bpp']) + '\t'
        rh += 'NumberofScans\t'
        run_data += str(chip_settings['scans']) + '\t'
        rh += 'ChipId\t'
        run_data += str(chip_settings['chip_id']) + '\t'
        rh += 'FlowCell\t'
        run_data += str(chip_settings['flowcell']) + '\t'
        rh += 'LabelSNRFilterType\t'
        run_data += str(settings.label_snr_filter_type) + '\t'
        rh += 'MinMoleculeLength\t'
        run_data += str(int(settings.min_mol_len / 1000)) + '\t'
        rh += 'MinLabelSNR\t'
        run_data += str(settings.min_label_SNR) + '\t'
        rh += 'RunId'
        run_data += str(chip_settings['run_id']) + '\t'
        ofile.write('#rh\t' + rh + '\n')
        ofile.write('# Run Data\t' + run_data + '\n')
        ofile.write('# Number of Molecules:\t' + str(chip_settings['molecule_count']) + '\n')
        ofile.write('#0h\tLabelChannel\tMoleculeID\tLength\tAvgIntensity\tSNR\tNumberofLabels\tOriginalMoleculeId\tScanNumber\tScanDirection\tChipId\tFlowcell\tRunId\tGlobalScanNumber' + '\n')
        ofile.write('#0f\tint\tint\tfloat\tfloat\tfloat\tint\tint\tint\tint\tstring\tint\tint\tint' + '\n')
        ofile.write('#1h\tLabelChannel\tLabelPositions[N]' + '\n')
        ofile.write('#1f\tint\tfloat' + '\n')
        ofile.write('#Qh\tQualityScoreID\tQualityScores[N]' + '\n')
        ofile.write('#Qf\tstring\tfloat[N]' + '\n')
        ofile.write('# Quality Score QX11: Label SNR for channel 1' + '\n')
        ofile.write('# Quality Score QX12: Label Intensity for channel 1' + '\n')

def sim_qx11():#TODO
        return 10

def sim_qx12():#TODO
        return 10

def write_bnx_entry(info, nicks, ofile, label, chip_settings):
        count = 0
        channel = '1'
        Q1 = 0
        Q2 = 0
        q1 = 'QX11'
        q2 = 'QX12'
        for pos in nicks:
                if pos[1]['label'] == label:
                        count += 1
                        channel += '\t' + '{0:.2f}'.format(pos[0])
                        val = sim_qx11()
                        Q1 += val
                        q1 += '\t' + '{0:.4f}'.format(val)
                        val = sim_qx12()
                        Q2 += val
                        q2 += '\t' + '{0:.4f}'.format(val)
        moleculeID = info[0]
        length = info[1]
        scan = info[2]
        Q1 = Q1 / count if count > 0 else 0
        Q2 = Q2 / count if count > 0 else 0
        channel += '\t' + '{0:.2f}'.format(length)
        backbone = ''
        backbone += str(0) + '\t'                               #backboneLabelChannel   0
        backbone += str(moleculeID) + '\t'                      #ID                     1
        backbone += str('{0:.2f}'.format(length)) + '\t'        #length                 x.00
        backbone += str('{0:.2f}'.format(Q1)) + '\t'            #avgIntensity           10.00
        backbone += str('{0:.2f}'.format(Q2)) + '\t'            #SNR                    10.00
        backbone += str(count) + '\t'                           #NumberofLabels         count
        backbone += str(moleculeID) + '\t'                      #OriginalMoleculeId     1
        backbone += str(scan) + '\t'                               #ScanNumber             1
        backbone += str(-1) + '\t'                              #ScanDirection          -1
        backbone += str(chip_settings['chip_id']) + '\t'        #ChipId                 unknown
        backbone += str(1) + '\t'                               #Flowcell               1
        backbone += str(1) + '\t'                               #RunId                  1
        backbone += str(1)                                      #GlobalScanNumber       1
        ofile.write(backbone + '\n')
        ofile.write(channel + '\n')
        ofile.write(q1 + '\n')
        ofile.write(q2 + '\n')


