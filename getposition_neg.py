import argparse
import gzip

parser = argparse.ArgumentParser()
parser.add_argument("infile")
args = parser.parse_args()

#parent = []
start = 0
end = 0
d = {}
with gzip.open(args.infile, 'rt') as f:
    for line in f:
        line = line.rstrip()
        line = line.split('\t')
        if line [2] != 'CDS' or line[6] != '-':
            continue
        
        chr = line[0]   
        cur_parent = line[8].split("=")[1]
        start = int(line[3])
        end = int(line[4])
        if cur_parent not in d:
            d[cur_parent] = [chr, []]
        d[cur_parent][1].append((start, end))
        

    for parent in d:
        chr, pos = d[parent]
        print (parent, chr, pos, sep = '\t')

        

        
