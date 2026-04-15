import zombie_utils
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("matrix_file_path")
parser.add_argument("output_file")
parser.add_argument("--max_d", type=float, default=0.2)
args = parser.parse_args()

ids, data = zombie_utils.read_matrix(args.matrix_file_path)
matrix_values = np.array(data)

# build tree
Z = linkage(matrix_values, method='average')

# cut into groups
max_d = args.max_d
clusters = fcluster(Z, max_d, criterion='distance') 

# write cluster result into file
output_file = "./../build/hierarchy_clusters_results.txt"
with open(output_file, 'w') as f:
    f.write("Gene_ID\tCluster_ID\n")
    for i in range (len(ids)):
        f.write(f"{ids[i]}\t{clusters[i]}\n")
