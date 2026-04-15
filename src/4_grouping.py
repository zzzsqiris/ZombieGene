import zombie_utils
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("cluster_result")
parser.add_argument("x_marked_fa")
parser.add_argument("output_dir")
args = parser.parse_args()

cluster_result = args.cluster_result
x_marked_fa = args.x_marked_fa
output_dir = args.output_dir

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

protein_dict = zombie_utils.read_fasta(x_marked_fa)

family_dict = {}
f = zombie_utils.smart_open(cluster_result)
f.readline()
for line in f:
    line = line.strip()
    gene_id, group_num = line.split('\t')
    if group_num not in family_dict:
        family_dict[group_num] = []
    family_dict[group_num].append(gene_id)
    
for group_num, gene_list in family_dict.items():
    if len(gene_list) < 3:
        continue
    else:
        out_file_name = os.path.join(output_dir, f"group_{group_num}.fa")
        with open (out_file_name, 'w') as f_out:
            for gene in gene_list:
                f_out.write(f">{gene}\n{protein_dict[gene]}\n")
