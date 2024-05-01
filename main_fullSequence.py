# Runs prokkaMuscleFullSequence.py, neighbor joining algorithm in the whole sequence.

import subprocess
import sys

def run_script(script_path, *args):
    # runs a given Python script using subprocess with additional arguments.
    try:
        # Include the script_path and any additional arguments in the command
        command = ['python3', script_path] + list(args)
        subprocess.run(command, check=True, text=True)
        print(f"Successfully ran {script_path} with args {args}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path} with args {args}: {e}")

def main():
    # checking number of required arguments.
    if len(sys.argv) < 3:
        print("Usage: python3 main_fullSequence.py <path_to_input_file> <reference_genome>")
        sys.exit(1)

    # The first argument after the script name is the path to the input file.
    input_file = sys.argv[1]
    # The second argument is the reference genome.
    reference_genome = sys.argv[2]

    # Defining the scripts and their corresponding arguments in a list of tuples
    scripts_with_args = [
        ('fullSequenceAnalysis/prokkaMuscleFullSequence.py', input_file, reference_genome),
        ('fullSequenceAnalysis/neighborJoining/main_NJ.py',),  # no additional args required. Input hardcoded within the file.
        ('fullSequenceAnalysis/neighborJoining/tree_maker.py',)  # no additional args required. Input hardcoded within the file.
    ]

    # Iterate through the scripts and their arguments, running them one by one.
    for script_tuple in scripts_with_args:
        script_path = script_tuple[0]
        args = script_tuple[1:]  # All the elements after the first one are the args ::
        run_script(script_path, *args)

if __name__ == "__main__":
    main()

