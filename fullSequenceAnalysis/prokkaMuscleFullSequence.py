# Runs Prokka and Muscle on the full sequence.

import os
from Bio import SeqIO
import subprocess
import argparse
import shutil

def clear_directory(directory):
    # Empties the specified directory of all files and folders.
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def extract_sequence(input_file, output_file, reference):
    # Extracts sequences that contain the provided reference in their FASTA header.
    with open(input_file, 'r') as original, open(output_file, 'w') as extracted:
        for record in SeqIO.parse(original, 'fasta'):
            if reference in record.id:
                SeqIO.write(record, extracted, 'fasta')
                break  # Stop after the first match

def run_prokka(sequence_file, output_directory, prefix):
    # Runs Prokka on a specified sequence file.
   
    prokka_cmd = [
        'prokka', '--force', sequence_file,
        '--outdir', output_directory,
        '--prefix', prefix,
        '--kingdom', 'Viruses'
    ]
    subprocess.run(prokka_cmd, check=True)
    # Return the path to the TSV file for potential future use
    return os.path.join(output_directory, f"{prefix}.tsv")

def remove_whitespace(input_file, output_file):
    """
    Removes unnecessary whitespaces from FASTA files. Need to run this before and AFTER MUSCLE>
    """
    with open(input_file, 'r') as f, open(output_file, 'w') as new_file:
        sequences = []
        current_sequence = ""
        for line in f:
            if line.startswith(">"):
                if current_sequence:
                    sequences.append(current_sequence)
                current_sequence = line.strip() + '\n'
            else:
                current_sequence += line.strip()
        if current_sequence:
            sequences.append(current_sequence)
        for sequence in sequences:
            new_file.write(sequence + '\n')
            
def remove_whitespace_and_run_muscle(input_file, output_directory, muscle_executable='muscle'):
    """
    Cleans input file, runs MUSCLE, and then cleans the MUSCLE output for further processing.
    """
    # File paths setup
    cleaned_input_file = os.path.join(output_directory, "input_cleaned.fasta")
    muscle_intermediate_output = os.path.join(output_directory, "muscle_output.fasta")
    final_cleaned_output = os.path.join(output_directory, "fullSequence_aligned_sequences.ffn")  # Corrected final output file name

    # Pre-MUSCLE cleaning.
    remove_whitespace(input_file, cleaned_input_file)
    
    # Run MUSCLE.
    muscle_cmd = [muscle_executable, '-in', cleaned_input_file, '-out', muscle_intermediate_output]
    subprocess.run(muscle_cmd, check=True)

    # Post-MUSCLE cleaning: Clean the MUSCLE output for neighbor-joining analysis
    remove_whitespace(muscle_intermediate_output, final_cleaned_output)
    
    # Cleanup intermediate files
    os.remove(cleaned_input_file)
    os.remove(muscle_intermediate_output)


def clear_directory_except(directory, keep_files):
    """
    Empties the specified directory of all files except those listed in keep_files.
    """
    for filename in os.listdir(directory):
        if filename not in keep_files:
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

def main():
    parser = argparse.ArgumentParser(description='Process sequences with Prokka and MUSCLE.')
    parser.add_argument('input_file', help='Input FASTA file containing multiple sequences.')
    parser.add_argument('reference', help='Reference ID for the sequence to annotate.')
    args = parser.parse_args()

    output_directory = "fullSequence-output"
    os.makedirs(output_directory, exist_ok=True)
    
    # Clear the output directory at the start
    clear_directory(output_directory)

    extracted_sequence_file = os.path.join(output_directory, f"{args.reference}_sequence.fasta")
    tsv_file = f"{args.reference}.tsv"
    muscle_output_file = "fullSequence_aligned_sequences.ffn"

    extract_sequence(args.input_file, extracted_sequence_file, args.reference)
    tsv_path = run_prokka(extracted_sequence_file, output_directory, args.reference)
    remove_whitespace_and_run_muscle(args.input_file, output_directory)

    # Final cleanup to keep only the TSV and aligned sequences file
    clear_directory_except(output_directory, [tsv_file, muscle_output_file])

    print(f"Annotation and alignment completed. Files kept: {tsv_file}, {muscle_output_file}")

if __name__ == "__main__":
    main()

