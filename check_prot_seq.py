import argparse
parser = argparse.ArgumentParser()
parser.add_argument("prot_seq_file")
parser.add_argument("my_prot_seq_file")
args = parser.parse_args()

def cmp (seq1, seq2):
    # remove X in seq2
    no_X_seq2 = []
    for i in range(len(seq2)):
        if seq2[i] != "X":
            no_X_seq2.append(seq2[i])
    # compare
    for i in range(max(len(seq1), len(no_X_seq2))):
        if seq1[i] == no_X_seq2[i]:
            continue
        else:
            print(prot_id ,"error at pos", i)
            print("seq1", "".join(seq1))
            print("seq2", "".join(no_X_seq2))
            break
    print("correct seq")

# build protein seq dictionary
prot_dict = {}
with open(args.prot_seq_file) as f1:
    for line in f1:
        line = line.rstrip()
        if line.startswith(">"):
            prot_id = line.replace(">", "")
            continue
        else:
            prot_dict[prot_id] = line

# go through my protein seq and compare
with open(args.my_prot_seq_file) as f2:
    for line in f2:
        line = line.rstrip()
        id, chr, seq2 = line.split(" ")
        prot_id = id.split(",")[0]
        try:
            seq1 = prot_dict[prot_id]
            cmp (seq1, seq2)
        except:
            print(prot_id, "error")
        
