import argparse
import gzip
import korflab
import iris_lib

parser = argparse.ArgumentParser()
parser.add_argument("gff3_file")
parser.add_argument("fa_file")
args = parser.parse_args()

# extract ID, chr, sign, pos from gff3 file
d = {}
with gzip.open(args.gff3_file, 'rt') as f:
    for line in f:
        line = line.rstrip()
        line = line.split('\t')
        if line [2] != 'CDS':
            continue
        
        chr = line[0]   
        ID = line[8].split("=")[1]
        sign = line[6]
        start = int(line[3])
        end = int(line[4])
        if ID not in d:
            d[ID] = [chr, sign, []]
        d[ID][2].append((start, end))

    # for ID in d:
    #     chr, sign, pos = d[ID]
    #     print (ID, chr, sign, pos, sep = '\t')

# store chromosome seq into dictionary
chr_dict = {}
chr_num = ""
with gzip.open(args.fa_file, 'rt') as f:
    for line in f:
        line = line.rstrip()
        if line.startswith(">"):
            if chr_num:
                chr_dict[chr_num] = "".join(chr_seq)
            chr_num = line[1:].split()[0]
            chr_seq = []
        else:
            chr_seq.append(line)

    if chr_num:
        chr_dict[chr_num] = "".join(chr_seq)


# link the seq, mark intron with X
for ID in d:
    chr, sign, pos = d[ID]
    chr_seq = chr_dict[chr]
    extron_seq = []
    for start, end in pos:
        extron_seq.append(chr_seq[start-1:end])

    # translate
    protein_seq = []
    leftover = ""
    for exon in extron_seq:
        if sign == "-":
            exon = iris_lib.rev_comp(exon)
        exon = leftover + exon
        remainder = len(exon) % 3

        if remainder == 0:
            leftover = ""
        else:
            leftover = exon[-remainder:]
            exon = exon[:-remainder]
        
        protein_seq.append(korflab.translate(exon))

    linked_protein = "X".join(protein_seq)
    print(ID, chr, linked_protein)