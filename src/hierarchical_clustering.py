import zombie_utils
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
import matplotlib.pyplot as plt

matrix_file_path = "./../build/wholegenome_matrix.txt"
ids, data = zombie_utils.read_matrix(matrix_file_path)
matrix_values = np.array(data)

# build tree
Z = linkage(matrix_values, method='average')

# cut into groups
max_d = 0.3
clusters = fcluster(Z, max_d, criterion='distance') 

# write cluster result into file
output_file = "./../build/hierarchy_clusters_results.txt"
with open(output_file, 'w') as f:
    f.write("Gene_ID\tCluster_ID\n")
    for i in range (len(ids)):
        f.write(f"{ids[i]}\t{clusters[i]}\n")


# --- subtree for graping purpose ---
# get top 5 groups
counter = {}
for group_num in clusters:
    if group_num not in counter:
        counter[group_num] = 0
    counter[group_num] += 1
sorted_counter = sorted(counter.items(), key=lambda item: item[1], reverse=True)

top_group = []
for i in range(5):
    top_group.append(sorted_counter[i][0])

top_index = []
for i in range(len(clusters)):
    if clusters[i] in top_group:
        top_index.append(i)

sub_data = []
for i in top_index:
    row = []
    for j in top_index:
        row.append(matrix_values[i][j])
    sub_data.append(row)
sub_matrix = np.array(sub_data)

Z_top5 = linkage(sub_matrix, method='average')

# plot tree
dendrogram(Z_top5, labels=[ids[i] for i in top_index], orientation='left')
plt.show()