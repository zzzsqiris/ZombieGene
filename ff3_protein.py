# check protein length and identity percentage
# import file
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("infile")
parser.add_argument("--length_threshold", type=int, default=200, metavar='<int>')
parser.add_argument("--identity_threshold", type=int, default=50, metavar='<int>')
args = parser.parse_args()

# set threshold, initalized storage and checker
length_threshold = args.length_threshold
identity_threshold = args.identity_threshold

prot_temp_store = []
lengthcheck = False
identitycheck = False
protein = False

# Filter out query with low hit
with open(args.infile) as f:
    for line in f:
        line = line.rstrip()
        #if line == "":
            #continue

        # new query
        if line.startswith("Query="):
            if prot_temp_store and lengthcheck and identitycheck:
                print("\n".join(prot_temp_store))
                prot_temp_store = []
                lengthcheck = False
                identitycheck = False
            protein = False
            print(line, "\n")
        
        if line.startswith("Length=") and protein == False:
            print(line, "\n")
        
        # new protein
        if line.startswith(">"):
            protein = True
            if prot_temp_store and lengthcheck and identitycheck:
                print("\n".join(prot_temp_store))
            lengthcheck = False
            identitycheck = False
            prot_temp_store = []
            prot_temp_store.append(line)
            continue

        # check protein length
        if line.startswith("Length=") and protein == True:
            prot_temp_store.append(line)
            length = int(line.split("=")[1])
            if length > length_threshold:
                lengthcheck = True
            continue

        # check protein identity percentage
        if line.startswith(" Identities"):
            prot_temp_store.append(line)
            x = line.split(" ")[4]
            x = x.replace(",", "")
            x = x.replace("(", "")
            x = x.replace("%", "")
            x = x.replace(")", "")
            identity = int(x)
            if identity > identity_threshold:
                identitycheck = True
        
        # get protein seq
        elif protein == True:
            prot_temp_store.append(line)
        
        continue

    