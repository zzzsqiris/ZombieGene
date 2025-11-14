import argparse
parser = argparse.ArgumentParser()
parser.add_argument("infile")
parser.add_argument("--protein_fraction", type=float, default=0.2, metavar='<float>')
args = parser.parse_args()

protein_fraction = args.protein_fraction

prot_temp_store = []
lengthcheck = False
protein = False

# Filter out query with low hit
with open(args.infile) as f:
    for line in f:
        line = line.rstrip()

        # new query
        if line.startswith("Query="):
            if prot_temp_store and lengthcheck:
                print("\n".join(prot_temp_store))
                prot_temp_store = []
                lengthcheck = False
            protein = False
            print(line, "\n")
        
        if line.startswith("Length=") and protein == False:
            query_length = int(line.split("=")[1])
            print(line, "\n")
        
        # new protein
        if line.startswith(">"):
            protein = True
            if prot_temp_store and lengthcheck == True:
                print("\n".join(prot_temp_store))
            lengthcheck = False
            prot_temp_store = []
            prot_temp_store.append(line)
            continue

        # check protein length
        if line.startswith("Length=") and protein == True:
            prot_temp_store.append(line)
            length = int(line.split("=")[1])
            if length <= (query_length * (1+protein_fraction)) and length >= (query_length * (1-protein_fraction)):
                lengthcheck = True
            continue

        # get protein seq
        elif protein == True:
            prot_temp_store.append(line)
        
        continue

    