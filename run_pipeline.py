import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    # input file
    parser.add_argument("gff3_file", help="Path to the GFF3 file")
    parser.add_argument("fa_file", help="Path to the genome FASTA file")
    # output file
    parser.add_argument("project_name", help="Name for this trial (a folder will be created)")
    parser.add_argument("--base_dir", default="./build", help="Base directory for results (default: ./build)")
    args = parser.parse_args()

    # build output file directory
    trial_path = os.path.join(args.base_dir, args.project_name)
    
    if not os.path.exists(trial_path):
        os.makedirs(trial_path)

    # filename
    file_prefix = os.path.join(trial_path, args.project_name)
    
    # Step1: Stitch and Blast
    x_marked_fa = f"{file_prefix}.fa"
    print("\n Step1: Stitching exons and running BLAST")
    cmd1 = f"python3 src/1_stitch_and_blast.py {args.gff3_file} {args.fa_file} {file_prefix}"
    os.system(cmd1)


    # Step2: Build Matrix
    zombie_file = f"{file_prefix}zombie.txt"
    matrix_file = f"{file_prefix}_matrix.txt"
    print("\n Step2: Parsing BLAST results and building matrix")
    cmd2 = f"python3 src/2_build_matrix.py {zombie_file} {matrix_file}"
    os.system(cmd2)

    # Step 3: Hierarchical Clustering
    cluster_results = f"{file_prefix}_cluster_results.txt"
    print("\n Step3: Hierarchical Clustering...")
    cmd3 = f"python3 src/3_hierarchical_clustering.py {matrix_file} {cluster_results}"
    os.system(cmd3)

    # Step 4: Grouping
    group_dir = os.path.join(trial_path, "groups")
    print("\n Step 4: Grouping")
    cmd4 = f"python3 src/4_grouping.py {cluster_results} {x_marked_fa} {group_dir}"
    os.system(cmd4)

    # Step 5: Multiple Alignment
    alignment_dir = os.path.join(trial_path, "multi_aln")
    print("\n Step5: Running ClustalW alignments")
    cmd5 = f"python3 src/5_multialign.py {group_dir} {alignment_dir}"
    os.system(cmd5)

    # Step 6: Find Interesting Groups
    print("\n Step 6: Searching for groups with mismatched introns")
    cmd6 = f"python3 src/6_find_interesting_groups.py {alignment_dir}"
    os.system(cmd6)

if __name__ == "__main__":
    main()