import argparse
import gzip
import korflab

parser = argparse.ArgumentParser()
parser.add_argument("position_file")
parser.add_argument("fa_file")
args = parser.parse_args()

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


with open(args.position_file) as f:
    for line in f:
        line = line.rstrip()
        parent, chr_num, pos_str = line.split("\t")
        
        # convert position string to int list
        pos_str = pos_str.strip("[]")
        pos_str = pos_str.split("), (")
        pos = []
        for pair in pos_str:
            pair = pair.replace("(", "").replace(")", "")
            start, end = pair.split(",")
            pos.append((int(start), int(end)))

        chr_seq = chr_dict[chr_num]
        extron_seq = []
        for start, end in pos:
            extron_seq.append(chr_seq[start-1:end])

        # translate
        protein_seq = []
        leftover = ""
        for exon in extron_seq:
            # reverse comp
            new_seq = ""
            for base in exon:
                if base == "A":
                    new_seq += "T"
                elif base == "T":
                    new_seq += "A"
                elif base == "C":
                    new_seq += "G"
                elif base == "G":
                    new_seq += "C"
            exon = new_seq[::-1]

            exon = leftover + exon
            remainder = len(exon) % 3

            if remainder == 0:
                leftover = ""
            else:
                leftover = exon[-remainder:]
                exon = exon[:-remainder]
            
            protein_seq.append(korflab.translate(exon))

        linked_protein = "X".join(protein_seq)
        print(parent, chr_num, linked_protein)