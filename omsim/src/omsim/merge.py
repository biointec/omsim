#!/usr/bin/python
"""
        Copyright (C) 2021 Giles Miclotte (giles.miclotte@ugent.be)
        This file is part of OMSim
"""

import os


def merge_bnx(out_bnx, in_bnxs):
    headers = []
    label = 0
    bnx_files = []
    for in_bnx in in_bnxs:
        label += 1
        bnx_files.append(open(in_bnx))

    # read headers
    last_lines = []
    for bnx_file in bnx_files:
        header = []
        while True:
            line = bnx_file.readline()
            if line[0] == '#':
                header.append(line)
            else:
                break
        last_lines.append(line)
        headers.append(header)

    out_bnx_file = open(out_bnx, 'w')
    # write header
    idx = 0
    for line in headers[0]:
        if line[:16] == '# Label Channels':
            out_bnx_file.write('# Label Channels:\t' + str(len(in_bnxs)) + '\n')
        elif line[:28] == '# Nickase Recognition Site 1':
            for label in range(0, len(in_bnxs)):
                out_bnx_file.write('# Nickase Recognition Site ' + str(label + 1) + headers[label][idx][28:])
        elif line[:3] == '#1h':
            for label in range(0, len(in_bnxs)):
                out_bnx_file.write('#' + str(label + 1) + headers[label][idx][2:])
                out_bnx_file.write('#' + str(label + 1) + headers[label][idx + 1][2:])
        elif line[:20] == '# Quality Score QX11':
            for label in range(0, len(in_bnxs)):
                out_bnx_file.write(headers[label][idx][:18] + str(label + 1) + headers[label][idx][19:-2] + str(label + 1) + '\n')
                out_bnx_file.write(headers[label][idx + 1][:18] + str(label + 1) + headers[label][idx + 1][19:-2] + str(label + 1) + '\n')
        elif line[:2] != '#1' and line[:15] != '# Quality Score':
            out_bnx_file.write(line)
        idx += 1

    # read and write entries in batches
    backbone = last_lines[0]
    entries = [
        {
            'backbone': backbone.split('\t'),
            'data': [],
            'snr': [],
            'intensity': [],
        }
    ]
    # fix nick count
    entries[0]['backbone'][5] = str(sum(int(x.split('\t')[5]) for x in last_lines))

    limit = 1000
    while True:
        label = 0
        for bnx_file in bnx_files:
            label += 1
            entries = read_entries(bnx_file, label, entries, limit)
        for idx in range(len(entries)):
            entry = entries[idx]
            out_bnx_file.write('\t'.join(entry['backbone']))
            for jdx in range(len(entry['data'])):
                out_bnx_file.write(entry['data'][jdx])
            for jdx in range(len(entry['data'])):
                out_bnx_file.write(entry['snr'][jdx])
            for jdx in range(len(entry['data'])):
                out_bnx_file.write(entry['intensity'][jdx])
        if len(entries) < limit:
            break
        entries = []

    # close and remove files
    for bnx_file in bnx_files:
        bnx_file.close()
    for in_bnx in in_bnxs:
        os.remove(in_bnx)


def read_entries(bnx_file, label, entries, limit):
    slabel = str(label)
    count = 0
    while True:
        line = bnx_file.readline()
        if line == '':
            break
        if line[0] == '0':
            if label == 1:
                entries.append({
                    'backbone': line.split('\t'),
                    'data': [],
                    'snr': [],
                    'intensity': [],
                })
            else:
                # fix nick count
                entries[count]['backbone'][5] = str(int(entries[count]['backbone'][5]) + int(line.split('\t')[5]))
        elif line[0] == '1':
            entries[count]['data'].append(slabel + line[1:])
        elif line[:4] == 'QX11':
            entries[count]['snr'].append('QX' + slabel + line[3:])
        elif line[:4] == 'QX12':
            entries[count]['intensity'].append('QX' + slabel + line[3:])
            count += 1
            if count == limit:
                break
    return entries
