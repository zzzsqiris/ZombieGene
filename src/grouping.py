import zombie_utils
import os

cluster_result = "./../build/hierarchy_clusters_results.txt" 
x_marked_fa = "./../build/wholegenome.fa"  #./../build/save_path.fa
output_dir = "./../build/group"

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
