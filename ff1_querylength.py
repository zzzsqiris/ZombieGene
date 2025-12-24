# Filter out short query
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("infile")
parser.add_argument("--query_length_threshold", type=int, default=200, metavar='<int>')
args = parser.parse_args()

query_length_threshold = args.query_length_threshold
temp_store = []
query = False
query_length = 0


with open(args.infile) as f:
    for line in f:
        line = line.rstrip()
        # find new Query
        if line.startswith("Query="):
            # check previous Query
            if temp_store and query_length > query_length_threshold:
                print("\n".join(temp_store))
            query_length = 0
            temp_store = [line]
            query = True
            continue

        # get Query length
        if line.startswith("Length=") and query == True:
            query_length = int(line.split("=")[1])
            temp_store.append(line)
            query = False
            continue

        temp_store.append(line)

        
