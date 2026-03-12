import os
import subprocess

input_dir = "./../build/group"
output_dir = "./../build/multi_aln"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

files = [f for f in os.listdir(input_dir) if f.endswith(".fa")]

for filename in files:
    input_path = os.path.join(input_dir, filename)
    output_path = os.path.join(output_dir, filename.replace(".fa", ".txt"))
    
    cmd = [
        "clustalw2",
        f"-INFILE={input_path}",
        f"-OUTFILE={output_path}",
        "-OUTPUT=CLUSTAL",
        "-QUIET"
    ]

    subprocess.run(cmd, check=True)
