def fasta_parse(ifname):
        infile = open(ifname)
        key = ''
        val = ''
        for line in infile:
                if line.startswith('>'):
                        if key:
                                yield key, val
                        key, val = line[1:].rstrip().split()[0], ''
                elif key:
                        val += line.rstrip()
        if key:
                yield key, val
