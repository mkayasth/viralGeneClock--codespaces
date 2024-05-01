# automates genetic_distances.py > branch_length.py > mutationRate.py.
# calculates avg mutation rate for each gene and appends it to output file 'avg_mutation_rate_final/average_mutation_rates.txt' :)

import subprocess
import os
import csv
import sys

# check if a reference genome is provided as a command-line argument.
if len(sys.argv) < 2:
    print("Usage: python3.11 geneAnalysis.py <reference_genome>")
    sys.exit(1)

# get the reference genome from the command-line argument.
reference_genome = sys.argv[1]

# Paths to Python scripts for mutationRate calculations.
genetic_distances_script = 'geneAnalysis/MutationRateCalculator/genetic_distances.py'
branch_length_script = 'geneAnalysis/MutationRateCalculator/branch_length.py'
mutation_rate_script = 'geneAnalysis/MutationRateCalculator/mutationRate.py'

# Path to the final output CSV file from mutationRate.py
mutation_rate_csv = 'geneAnalysis-output/mutation_rates.csv'

# Path to the output text file where the average mutation rate will be appended.
average_mutation_rate_file = 'avg_mutation_rate_final/average_mutation_rates.txt'

# function to run a Python script with additional arguments, if needed.
def run_script(script_path, *args):
    subprocess.run(['python3.11', script_path, *args], check=True)

# Calculate the average mutation rate (for a protein ~~ by comparing all with reference strain).
def calculate_average_mutation_rate(csv_file): # avg of all strains compared to the reference genome from mutation_rates.csv.
    total_mutation_rate = 0
    count = 0
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Approximate Mutation Rate'] != 'N/A':
                total_mutation_rate += float(row['Approximate Mutation Rate'])
                count += 1
    average_mutation_rate = total_mutation_rate / count if count > 0 else 0
    return average_mutation_rate

# Function to append the average mutation rate to a text file.
def append_average_mutation_rate_to_file(file_path, protein_name, mutation_rate):
    # Ensure the directory exists first.
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # then, append to the file.
    with open(file_path, mode='a', encoding='utf-8') as file:
        file.write(f"Average mutation rate for {protein_name}: {mutation_rate}\n")
        
# function that cleans up any hypothetical_protein that Prokka could not annotate.
def clean_up_mutation_rates_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Filter out lines containing 'hypothetical_protein'
    cleaned_lines = [line for line in lines if 'hypothetical_protein' not in line.lower()]

    # Writing the cleaned lines back to the same file.
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(cleaned_lines)

# Run the scripts in order, including the reference genome as an argument for the first two scripts.
run_script(genetic_distances_script, reference_genome)
run_script(branch_length_script, reference_genome)
run_script(mutation_rate_script)  # mutationRate.py doesn't require the reference genome as an argument //

# Average mutation rate calculation.
average_mutation_rate = calculate_average_mutation_rate(mutation_rate_csv)

# Extracting the protein name.
with open(mutation_rate_csv, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # skip the header row.
    first_row = next(reader, None)  # read the first data row.
    protein_name = 'UnknownProtein'  # default value
    if first_row:
        strain_name = first_row[0]
        protein_name = strain_name.split('|')[1].split(',')[0] if '|' in strain_name else strain_name

# Append the average mutation rate to the text file
append_average_mutation_rate_to_file(average_mutation_rate_file, protein_name, average_mutation_rate)

# Clean the average mutation rates text file
clean_up_mutation_rates_txt(average_mutation_rate_file)

# After processing and calculations are done, delete the intermediate files.
os.remove('geneAnalysis-output/genetic_distances.csv')
os.remove('geneAnalysis-output/branch_length.csv')
os.remove('geneAnalysis-output/mutation_rates.csv')
