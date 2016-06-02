#!/bin/bash
cd ../..
./package.sh
./install.sh
cd test/ecoli

/usr/bin/time -v python2 -m omsim example.xml
bnx0=ecoli_output.label_0.1.bnx
bnx1=ecoli_output.label_1.1.bnx

for bnx in ${bnx0} ${bnx1}; do
        echo "" > ${bnx}.stats
        for c in 3 4 5; do
                echo -e "\n# column: "$c >> ${bnx}.stats
                grep "^0" ${bnx} | cut -f $c | qstats >> ${bnx}.stats
        done
        echo -e "\n# row: QX11" >> ${bnx}.stats
        grep "^QX11" ${bnx} | cut -f 2- | tr "\t" "\n" | grep -v "^$" | qstats >> ${bnx}.stats
        echo -e "\n# row: QX12" >> ${bnx}.stats
        grep "^QX12" ${bnx} | cut -f 2- | tr "\t" "\n" | grep -v "^$" | qstats >> ${bnx}.stats
done
