# Automates ProkkaMuscle.py. For each .ffn gene file, runs neighbor-joining (main_NJ.py from geneAnalysis and mutationRateCalculator (geneAnalysis.py).

import subprocess
import glob
import sys
import os
import shutil

# check if the script is run with the required arguments.
if len(sys.argv) < 3:
    print("Usage: python3 main_GeneAnalysis.py <path_to_full_genome_file> <reference_strain>")
    sys.exit(1)

# first argument after the script name is the full genome file path.
full_genome_path = sys.argv[1]

# second argument is the reference strain.
reference_strain = sys.argv[2]

# Path to the folder containing the .ffn files.
folder_path = 'geneAnalysis-output'

# run prokkaMuscle.py once, providing the full genome file path as an argument.
subprocess.run(['python3', 'geneAnalysis/prokkaMuscle.py', full_genome_path], check=True)

# list of all .ffn files in the folder using global library.
ffn_files = glob.glob(f'{folder_path}/*.ffn')

# Remove the pre-existing output folder first, if it exists :)
if os.path.exists('avg_mutation_rate_final') and os.path.isdir('avg_mutation_rate_final'):
    shutil.rmtree('avg_mutation_rate_final')

for ffn_file in ffn_files:
    # running neighbor_joining.py for each .ffn file, passing the file as an argument.
    subprocess.run(['python3', 'geneAnalysis/neighborJoining/main_NJ.py', ffn_file], check=True)
    print(f"Neighbor joining algorithm completed for", ffn_file + "." )
    
    # running geneAnalysis.py for each .ffn file, passing the file and reference strain as arguments.
    subprocess.run(['python3', 'geneAnalysis/geneAnalysis.py', reference_strain], check=True)
    print("geneAnalysis algorithm completed for", ffn_file + ".")



