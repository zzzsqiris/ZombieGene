import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("target_dir")
args = parser.parse_args()

target_dir = args.target_dir
all_files = os.listdir(target_dir)
all_files.sort()

for filename in all_files:
    if filename.startswith('.'): 
        continue
    
    file_path = os.path.join(target_dir, filename)
    same_x_pos = True
    
    with open(file_path, 'r') as f:
        current_block = {}
        
        for line in f:
            line = line.strip()
            if not line or line.startswith("CLUSTAL") or ("*" in line) or (":" in line):
                if current_block:
                    first_id = list(current_block.keys())[0]
                    reference_pattern = current_block[first_id]

                    for seq_id in current_block:
                        if current_block[seq_id] != reference_pattern:
                            same_x_pos = False
                            break

                    current_block = {}
                
                if not same_x_pos:
                    break
                continue

            parts = line.split()
            if len(parts) >= 2:
                seq_id = parts[0]
                seq_text = parts[1]
                
                length = len(seq_text)
                x_positions = []
                for i in range(length):
                    char = seq_text[i]
                    
                    if char == 'X':
                        x_positions.append(i)
                current_block[seq_id] = x_positions

    if not same_x_pos:
        print(filename)