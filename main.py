# run this file if you want to just use command line.
# Automates main_fullSequence.py followed by main_GeneAnalysis.py.

import subprocess
import sys

def run_main_scripts(script_path, *args):
    try:
        # Constructing the command with the script path and any additional arguments..
        command = ['python3', script_path] + list(args)
        subprocess.run(command, check=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute {script_path} with arguments {args}. Error: {e}")

def main():
    # Correct number of arguments are provided -- checking here.
    if len(sys.argv) < 3:
        print("Usage: python3 main.py <path_to_input_file> <reference_genome>")
        sys.exit(1)
    
    # First argument: path to the input file
    input_file = sys.argv[1]
    # Second argument: reference genome
    reference_genome = sys.argv[2]

    # Paths to the main scripts.
    main_full_sequence_script = 'main_fullSequence.py'
    main_gene_analysis_script = 'main_GeneAnalysis.py'


    # Execute main_fullSequence.py.
    run_main_scripts(main_full_sequence_script, input_file, reference_genome)

    # Execute main_GeneAnalysis.py.
    run_main_scripts(main_gene_analysis_script, input_file, reference_genome)

if __name__ == "__main__":
    main()

