import argparse
parser = argparse.ArgumentParser()
parser.add_argument("infile")
parser.add_argument("--hit_threshold", type=int, default=3, metavar='<int>')
args = parser.parse_args()

# hit_threshold = 3
hit_threshold = args.hit_threshold
Q_temp_store = []
hit = 0
protein = False

# Filter out query with low hit
with open(args.infile) as f:
    for line in f:
        line = line.rstrip()
        # find new Query
        if line.startswith("Query="):
            # print previous if reach hit threshold
            if Q_temp_store and hit > hit_threshold :
                print("\n".join(Q_temp_store))
            # initialized counting
            Q_temp_store = [line]
            hit = 0
            protein = False
            continue
        

        # count by ">"
        if line.startswith(">"):
            protein = True
            hit += 1
            Q_temp_store.append(line)
            continue

        Q_temp_store.append(line)

        