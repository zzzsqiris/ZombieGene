import argparse
import zombie_utils

parser = argparse.ArgumentParser()
parser.add_argument("zombie_filter_file", help="The output from blast_filter (zombie.txt)")
parser.add_argument("output_matrix", help="Path to save the generated matrix file")
args = parser.parse_args()

# extract protein id pairs, E-value
pair_data = {}
id_set = set()

with open(args.zombie_filter_file, 'r') as f:
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

with open(args.output_matrix, 'w') as f:
    matrix = zombie_utils.build_matrix(id_set, pair_data)
    for row in matrix:
        line = "\t".join(map(str, row)) + "\n"
        f.write(line)