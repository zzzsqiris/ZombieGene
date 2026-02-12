def blast_filter(infile, outfile, min_query_len=50, min_identity=80, len_fraction=0.2, min_align_len=100): #alignmnent length
    with open(outfile, 'w') as f_out:

        query_pass = False
        query_id = ""
        # protein_pass = False
        id_pass = False
        fraction_pass = False
        identity_pass = False
        alignment_len_pass = False
        X_pass = False
        temp_store = []

        with open(infile) as f:
            for line in f:
                line = line.rstrip()
                # find new query
                if line.startswith("Query="):
                    query_pass = False
                    query_id = line.split("=")[1].strip().split(".")[0]
                    temp_store = [line]
                    continue
                
                # query length filter
                if line.startswith("Length=") and not query_pass:
                    query_len = int(line.split("=")[1])
                    if query_len >= min_query_len:
                        query_pass = True
                        # print(temp_store)
                        # print(line)
                    continue
                if not query_pass:
                    continue
                
                # reach new protein
                if line.startswith(">"):
                    # protein_pass = False
                    id_pass = False
                    fraction_pass = False
                    identity_pass = False
                    alignment_len_pass = False
                    X_pass = False
                    temp_store = [line]

                    # filter out same id
                    prot_id = line.replace(">", "").strip().split(".")[0]
                    if prot_id != query_id:
                        id_pass = True
                    continue
                
                #if not protein_pass:
                temp_store.append(line)

                # check protein fraction length
                if line.startswith("Length="):
                    prot_len = int(line.split("=")[1])
                    lower_bound = query_len * (1 - len_fraction)
                    upper_bound = query_len * (1 + len_fraction)
                    if prot_len <= upper_bound and prot_len >= lower_bound:
                        fraction_pass = True
                    continue
                
                # check identity
                if line.startswith(" Identities"):
                    parts = line.split()
                    # check alignment length
                    alignment_len = parts[2]
                    alignment_length = int(alignment_len.split('/')[-1])
                    if alignment_length >= min_align_len:
                        alignment_len_pass = True

                    x = parts[3]
                    x = x.replace(",", "")
                    x = x.replace("(", "")
                    x = x.replace("%", "")
                    x = x.replace(")", "")
                    identity = int(x)
                    if identity >= min_identity:
                        identity_pass = True
                    continue
                    
                # check X
                if line.startswith("Sbjct"):
                    if "X" in line:
                        X_pass = True
                
                # if all pass, print
                if id_pass and fraction_pass and identity_pass and alignment_len_pass and X_pass:
                    #protein_pass = True
                    # print ("\n".join(temp_store))
                    header = f"Query= {query_id}\nLength= {query_len}\n"
                    block_content = header + "\n".join(temp_store)
                    
                    f_out.write(block_content + "\n\n")
                    id_pass = False
                    temp_store = []
                continue
    return


def build_matrix(id_set, pair_data):
    sorted_ids = sorted(list(id_set))
    matrix = []
    header = ["ID"] + sorted_ids
    matrix.append(header)

    for id1 in sorted_ids:
        row = [id1]
        for id2 in sorted_ids:
            if id1 == id2:
                row.append(0.0)
            else:
                val = pair_data.get((id1, id2))
                if val is None:
                    val = pair_data.get((id2, id1))
                if val is not None:
                    row.append(val)
                else:
                    row.append(1.0)
        matrix.append(row)
    return matrix

# read in matrix
def read_matrix(file_path):
    ids = []
    all_dist = []
    with open(file_path, 'r') as f:
        header = f.readline().strip().split('\t')
        ids = header[1:]
        
        for line in f:
            row = line.strip().split('\t')
            row_dist = [] 
            for x in row[1:]:
                row_dist.append(float(x))
            
            all_dist.append(row_dist)
    return ids, all_dist