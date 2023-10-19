# downloads (almost) all public BNX files from NCBI
wget https://ftp.ncbi.nlm.nih.gov/pub/supplementary_data/bionanomaps.csv
grep -o "https.*bnx" bionanomaps.csv > bionanobnx.csv
wget -nc -i bionanobnx.csv -P public-bnx-files
