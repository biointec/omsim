#!/bin/bash

#input paramaters
min_mol_len=${1:-150}
avg_mol_len=${2:-90}
sd_mol_len=${3:-85}

#sample 100mbp according to the above constraints
python size.py $min_mol_len $avg_mol_len $sd_mol_len

#draw a plot of the sampled lengths, requires gnuplot 5
gnuplot plotsizes

#print the input and resulting average and standard deviation
echo "minimal molecule length:     ${min_mol_len} kbp"
echo "sampling average:            ${avg_mol_len} kbp"
echo "sampling standard deviation: ${sd_mol_len} kbp"
echo
avg=$(echo "scale=0;$(awk 'BEGIN{s=0;}{s=s+$1;}END{print s/NR;}' size.out)/1000" | bc)
echo "average:                     ${avg} kbp"
sd=$(echo "scale=0;$(awk '{delta = $1 - avg; avg += delta / NR; mean2 += delta * ($1 - avg); } END { print sqrt(mean2 / NR); }' size.out)/1000" | bc)
echo "standard deviation:          ${sd} kbp"
