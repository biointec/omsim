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
from noise import Noise

class BNX:
        def __init__(self, settings, noise):
                self.settings = settings
                self.noise = noise
        
        def write_bnx_header(self, ofile, label, chip_settings):
                '''
                Writes the bnx-header
                '''
                ofile.write('# BNX File Version:\t' + self.settings.bnx_version + '\n')
                ofile.write('# Label Channels:\t' + '1' + '\n')
                for i in range(len(self.settings.enzymes)):
                        if self.settings.enzymes[i]['label'] == label:
                                ofile.write('# Nickase Recognition Site ' + str(i + 1) + ':\t' + self.settings.enzymes[i]['pattern'] + '\n')
                ofile.write('# Bases per Pixel:\t' + str(int(chip_settings['bpp'])) + '\n')
                ofile.write('# Software Version:\tomsim-' + self.settings.version + '\n')
                # TODO: run_data
                rh = ''
                run_data = ''
                rh += 'SourceFolder\t'
                run_data += path.dirname(path.realpath(ofile.name)) + '/Detect Molecules\t'
                rh += 'InstrumentSerial\t'
                run_data += 'omsim-' + self.settings.version + '\t'
                rh += 'Time\t'
                run_data += str(datetime.now()) + '\t'
                rh += 'NanoChannelPixelsPerScan\t'
                run_data += str(int(chip_settings['size'] / chip_settings['scans'] / chip_settings['bpp'])) + '\t'  # ~ 1to2 gbp divided by ~500 bpp, so about 2-4Mpixels per scan | total length divided by number of scans...
                rh += 'StretchFactor\t'
                run_data += str(chip_settings['stretch_factor']) + '\t'
                rh += 'BasesPerPixel\t'  # 500 with stretch .85, so about 425 / stretchfactor
                run_data += str(chip_settings['bpp']) + '\t'
                rh += 'NumberofScans\t'
                run_data += str(chip_settings['scans']) + '\t'
                rh += 'ChipId\t'
                run_data += str(chip_settings['chip_id']) + '\t'
                rh += 'FlowCell\t'
                run_data += str(chip_settings['flowcell']) + '\t'
                rh += 'LabelSNRFilterType\t'
                run_data += str(self.settings.label_snr_filter_type) + '\t'
                rh += 'MinMoleculeLength\t'
                run_data += str(int(self.settings.min_mol_len / 1000)) + '\t'
                rh += 'MinLabelSNR\t'
                run_data += str(self.settings.min_label_SNR) + '\t'
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
        
        
        def write_bnx_entry(self, info, nicks, ofile, chip_settings, stretch):
                count = 0
                channel = '1'
                Q1 = 0
                Q2 = 0
                q1 = 'QX11'
                q2 = 'QX12'
                for pos in nicks:
                        count += 1
                        channel += '\t' + '{0:.2f}'.format(pos * stretch)
                        val = self.noise.next_l_SNR()
                        q1 += '\t' + '{0:.4f}'.format(val)
                        val = self.noise.next_l_AI()
                        q2 += '\t' + '{0:.4f}'.format(val)
                moleculeID = info[0]
                length = info[1] * stretch
                scan = info[2]
                channel += '\t' + '{0:.2f}'.format(length)
                backbone = ''
                backbone += str(0) + '\t'                                               # backboneLabelChannel   0
                backbone += str(moleculeID) + '\t'                                      # ID                     1
                backbone += str('{0:.2f}'.format(length)) + '\t'                        # length                 x.00
                backbone += str('{0:.2f}'.format(self.noise.next_m_AI())) + '\t'     # avgIntensity           10.00
                backbone += str('{0:.2f}'.format(self.noise.next_m_SNR())) + '\t'    # SNR                    10.00
                backbone += str(count) + '\t'                                           # NumberofLabels         count
                backbone += str(moleculeID) + '\t'                                      # OriginalMoleculeId     1
                backbone += str(scan) + '\t'                                            # ScanNumber             1
                backbone += str(-1) + '\t'                                              # ScanDirection          -1
                backbone += str(chip_settings['chip_id']) + '\t'                        # ChipId                 unknown
                backbone += str(1) + '\t'                                               # Flowcell               1
                backbone += str(1) + '\t'                                               # RunId                  1
                backbone += str(scan)                                                   # GlobalScanNumber       1
                ofile.write(backbone + '\n')
                ofile.write(channel + '\n')
                ofile.write(q1 + '\n')
                ofile.write(q2 + '\n')
