import os
import subprocess
import argparse

# 设置参数解析
parser = argparse.ArgumentParser()
parser.add_argument("input_dir")
parser.add_argument("output_dir")
args = parser.parse_args()

input_dir = args.input_dir
output_dir = args.output_dir

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
