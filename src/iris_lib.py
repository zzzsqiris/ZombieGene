PAIRS = {
    "A": "T", "T": "A", "C": "G", "G": "C",
    "a": "t", "t": "a", "c": "g", "g": "c",
}

def complement (seq):
    comp_seq = ""
    if not isinstance(seq, str):
        seq = "".join(seq)
    for nt in seq:
        comp_seq += (PAIRS[nt])
    return comp_seq

def rev_comp(seq):
    if not isinstance(seq, str):
        seq = "".join(seq)
    comp_seq = complement(seq)
    rev_comp_seq = comp_seq[::-1]
    return rev_comp_seq
