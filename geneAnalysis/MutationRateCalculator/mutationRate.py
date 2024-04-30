# Divide genetic distance to the reference strain (for gene) with branch length to the reference strain (for the whole sequence).

import csv

def read_csv_data(file_path, is_genetic_distance=False):
    data = {}
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            strain = row[0]
            if is_genetic_distance:
                # Use the full strain name including the protein for genetic distances.
                data[strain] = float(row[1])
            else:
                # Use the base strain name for branch lengths.
                base_strain = strain.split('|')[0]
                data[base_strain] = float(row[1])
    return data

def combine_and_calculate_mutation_rate(branch_length_file, genetic_distance_file, output_file):
    # Read branch lengths using base strain names and genetic distances using full names.
    branch_lengths = read_csv_data(branch_length_file)
    genetic_distances = read_csv_data(genetic_distance_file, is_genetic_distance=True)
    
    with open(output_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Strain", "Branch Length", "Genetic Distance", "Approximate Mutation Rate"])

        # Iterate over genetic distances since it has the full names.
        for full_strain, genetic_distance in genetic_distances.items():
            base_strain = full_strain.split('|')[0]  # Get the base strain name for matching
            branch_length = branch_lengths.get(base_strain)

            # If branch length is available, calculate mutation rate!!
            if branch_length:
                mutation_rate = genetic_distance / branch_length
                writer.writerow([full_strain, branch_length, genetic_distance, mutation_rate])

# File paths for the input and output files. CSV files are removed by main scripts.
branch_length_file = 'geneAnalysis-output/branch_length.csv'
genetic_distance_file = 'geneAnalysis-output/genetic_distances.csv'
output_file = 'geneAnalysis-output/mutation_rates.csv'

# combine the data and calculate mutation rates.
combine_and_calculate_mutation_rate(branch_length_file, genetic_distance_file, output_file)


