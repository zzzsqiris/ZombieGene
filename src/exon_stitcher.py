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
cmd_compare = f"blastp -query {x_marked_fa} -db {x_marked_db} -out {blast_results} -evalue 1e-10"
os.system(cmd_compare)

# blast filter
# zombie = zombie_utils.blast_filter(blast_results)
zombie_output_file = args.save_path + "zombie.txt" # 自动定义文件名
zombie_blocks = zombie_utils.blast_filter(blast_results)

#with open(zombie_output_file, 'w') as f:
#    for block in zombie_blocks:
#        f.write(block + "\n\n")

# extract protein id pairs, E-value
pair_data = {}
id_set = set()

for block in zombie_blocks:
    lines = block.split('\n')
    query_id = ""
    protein_id = ""
    
    for line in lines:
        if line.startswith("Query="):
            query_id = line.split("=")[1].strip().split(".")[0]
            id_set.add(query_id)
            
        elif line.startswith(">"):
            protein_id = line.replace(">", "").strip().split(".")[0]
            id_set.add(protein_id)
            
        elif "Expect =" in line:
            line = line.split("Expect =")
            line = line[1].strip()
            e_val = line.split(",")[0].strip()
            e_val = float(e_val)

            if (query_id, protein_id) not in pair_data:
                pair_data[(query_id, protein_id)] = e_val
