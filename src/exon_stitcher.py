import argparse
import gzip
import korflab
import iris_lib
import zombie_utils
import os

parser = argparse.ArgumentParser()
parser.add_argument("gff3_file")
parser.add_argument("fa_file")
parser.add_argument("save_path")
args = parser.parse_args()

# extract ID, chr, sign, pos from gff3 file
d = {}
with gzip.open(args.gff3_file, 'rt') as f:
    for line in f:
        if line.startswith("#"):
            continue
        line = line.rstrip()
        line = line.split('\t')
        if line [2] != 'CDS':
            continue
        
        chr = line[0]
        sign = line[6]
        start = int(line[3])
        end = int(line[4])
        attributes = line[8].split(';')
        ID = ""
        for attr in attributes:
            if attr.startswith("locus_tag="):
                ID = attr.split("=")[1]
        if ID not in d:
            d[ID] = [chr, sign, []]
        d[ID][2].append((start, end))

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
x_marked_fa = args.save_path + ".fa"
with open(x_marked_fa, 'w') as f_out:
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
        f_out.write(f">{ID.split(',')[0]}\n")
        f_out.write(f"{linked_protein}\n")

# build BLAST data base
x_marked_db = args.save_path + "X_marked_db"
cmd_makedb = f"makeblastdb -in {x_marked_fa} -dbtype prot -out {x_marked_db}"
os.system(cmd_makedb)

# BLAST compare
blast_results = args.save_path + "X_marked.blast.out"
cmd_compare = f"blastp -query {x_marked_fa} -db {x_marked_db} -out {blast_results} -evalue 1e-10 -num_threads 4"
os.system(cmd_compare)

# blast filter
zombie_output_file = args.save_path + "zombie.txt"
zombie_utils.blast_filter(blast_results, zombie_output_file)

# extract protein id pairs, E-value
pair_data = {}
id_set = set()

with open(zombie_output_file, 'r') as f:
    query_id = ""
    protein_id = ""
    
    for line in f:
        line = line.strip()
        if line.startswith("Query="):
            query_id = line.split("=")[1].strip().split(".")[0]
            id_set.add(query_id)
            
        elif line.startswith(">"):
            protein_id = line.replace(">", "").strip().split(".")[0]
            id_set.add(protein_id)
            
        elif "Identities =" in line:
            line = line.split("(")
            line = line[1].split("%")[0] 
            identity_val = int(line) / 100
            
            distance = 1 - (identity_val)

            if (query_id, protein_id) not in pair_data:
                pair_data[(query_id, protein_id)] = round(distance, 4)

matrix_file = args.save_path + "_matrix.txt"
with open(matrix_file, 'w') as f:
    matrix = zombie_utils.build_matrix(id_set, pair_data)
    for row in matrix:
        line = "\t".join(map(str, row)) + "\n"
        f.write(line)