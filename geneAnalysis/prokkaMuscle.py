# run Prokka, annotate gene, group genes across strains together and then run Muscle on each gene file. 
# Prepares for neighbor-joining.

import os
import sys
from Bio import SeqIO
import subprocess
from collections import defaultdict
import argparse
import shutil

def remove_whitespace(input_file, output_file):
    # NJ algorithm needs whitespace to be removed to function.   
    with open(input_file, 'r') as f:
        lines = f.readlines()

    sequences = []
    current_sequence = ""

    for line in lines:
        if line.startswith(">"):
            if current_sequence:
                sequences.append(current_sequence)
            current_sequence = line.strip().rstrip() + '\n'
        else:
            current_sequence += line.strip().rstrip()

    if current_sequence:
        sequences.append(current_sequence)

    with open(output_file, 'w') as f:
        for sequence in sequences:
            f.write(sequence + '\n')

def remove_whitespace_and_run_muscle(input_file, muscle_executable='./muscle3.8.31_i86linux32'):
    # runs remove_whitespace before and after running MUSCLE.
    
    cleaned_file_pre = f"{input_file}_pre_cleaned.ffn"
    muscle_output_file = f"{input_file}_aligned.ffn"
    
    # Pre-MUSCLE cleaning.
    remove_whitespace(input_file, cleaned_file_pre)
    
    # Run MUSCLE.
    muscle_cmd = [muscle_executable, '-in', cleaned_file_pre, '-out', muscle_output_file]
    subprocess.run(muscle_cmd, check=True)

    # Post-MUSCLE cleaning.
    remove_whitespace(muscle_output_file, input_file)  # Overwrite the input (final desired filename)
    
    # cleanup intermediate files.
    os.remove(cleaned_file_pre)
    os.remove(muscle_output_file)

def annotate_and_group_genes(input_fasta, muscle_executable='./muscle3.8.31_i86linux32'):
# Prokka annotates viral genes. This function groups each gene across the strains together in a .ffn file in geneAnalysis-output.

    output_dir = "geneAnalysis-output"

    # Ensure the output directory exists and is empty before running.
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    intermediate_dir = os.path.join(output_dir, "intermediate_files")
    os.makedirs(intermediate_dir, exist_ok=True)
    
    strains = []
    gene_names = defaultdict(int)
    
    for record in SeqIO.parse(input_fasta, "fasta"):
        strain_name = record.id
        temp_fasta = os.path.join(intermediate_dir, f"{strain_name}.fasta")
        with open(temp_fasta, "w") as temp:
            SeqIO.write(record, temp, "fasta")
        
        prokka_output = os.path.join(intermediate_dir, strain_name)
        prokka_cmd = ["prokka", temp_fasta, "--outdir", prokka_output, "--prefix", strain_name, "--kingdom", "Viruses", "--force"]
        subprocess.run(prokka_cmd)
        
        # new ffn file for each gene.
        ffn_file = os.path.join(prokka_output, f"{strain_name}.ffn")
        genes = list(SeqIO.parse(ffn_file, "fasta"))
        strains.append((strain_name, genes))
    
    for gene_idx in range(max(len(genes) for _, genes in strains)):
        grouped_genes = []
        for strain_name, strain_genes in strains:
            if gene_idx < len(strain_genes):
                gene = strain_genes[gene_idx]
                description_parts = gene.description.split()
                if 'hypothetical' in description_parts:
                # if Prokka can't name the protein, call it hypothetical_protein.	
                    protein_name = "hypothetical_protein"
                else:
                # take the last two names; most protein names have two words in them.
                # this potentially messes name of some protein names. Use Prokka output to verify which protein exactly.
                    protein_name = "".join(description_parts[-2:])
                gene.id = f"{strain_name}|{protein_name}"
                gene.description = ""
                grouped_genes.append(gene)

        if grouped_genes:
            base_gene_name = grouped_genes[0].id.split('|')[-1].strip().rstrip()
            gene_names[base_gene_name] += 1
            count = gene_names[base_gene_name]
            output_file_name = f"{base_gene_name}{('_' + str(count)) if count > 1 else ''}.ffn"
            output_file_path = os.path.join(output_dir, output_file_name)
            
            with open(output_file_path, "w") as outfile:
                SeqIO.write(grouped_genes, outfile, "fasta")
            
            remove_whitespace_and_run_muscle(output_file_path, muscle_executable)

    shutil.rmtree(intermediate_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Annotate genomes, group genes, and multiple alignment of sequences.")
    parser.add_argument("input_fasta", help="The input FASTA file containing genome sequences.")
    parser.add_argument("--muscle", help="Path to the Muscle executable", default="./muscle3.8.31_i86linux32")
    
    args = parser.parse_args()
    
    if not os.path.isfile(args.input_fasta):
        sys.exit(f"Error: Input file '{args.input_fasta}' not found.")
    
    annotate_and_group_genes(args.input_fasta, muscle_executable=args.muscle)

