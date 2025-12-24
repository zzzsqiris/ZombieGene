import argparse
parser = argparse.ArgumentParser()
parser.add_argument("infile")
args = parser.parse_args()

hit_threshold = 5
length_threshold = 200
identity_threshold = 50
Q_temp_store = []
P_temp_store = []
hit = 0
lengthcheck = False
identitycheck = False

# Filter out query with low hit
with open(args.infile) as f:
    for line in f:
        line = line.rstrip()
        if line == "":
            continue
        # find new Query
        if line.startswith("Query="):
            # print previous if reach hit threshold
            if Q_temp_store and hit > hit_threshold :
                print("\n".join(Q_temp_store))
            # initialized counting
            Q_temp_store = [line]
            hit = 0
            continue
        
        # count by ">"
        if line.startswith(">"):
            hit += 1
            if P_temp_store and lengthcheck and identitycheck:
                Q_temp_store +=(P_temp_store)
            lengthcheck = False
            identitycheck = False
            P_temp_store = []
            P_temp_store.append(line)
            continue
        if line.startswith("Length="):
            P_temp_store.append(line)
            length = int(line.split("=")[1])
            if length > length_threshold:
                lengthcheck = True
            continue
        if line.startswith(" Identities"):
            P_temp_store.append(line)
            x = line.split(" ")[4]
            x = x.replace(",", "")
            x = x.replace("(", "")
            x = x.replace("%", "")
            x = x.replace(")", "")
            identity = int(x)
            if identity > identity_threshold:
                identitycheck = True
        
        P_temp_store.append(line)

    