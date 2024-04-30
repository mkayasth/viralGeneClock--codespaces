# genetic_distances calculated separately for each gene by main_NJ.py from geneAnalysis folder.

import csv
import sys

# function to read the genetic distances from the file.
# separate genetic distances for each gene for one input submission.
def read_genetic_distances(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter='\t')  # Assuming tab-delimited file
        headers = next(reader)  # Assuming the first row contains headers
        matrix = {row[0]: row[1:] for row in reader}  # Create a dict for each row
    return headers, matrix

# Main function
def main(reference_substr):
    # File path for the genetic distances
    distance_file = "geneAnalysis-output/genetic_distances.txt"
    
    # Path for the output CSV file. main will remove csv files.
    output_file = "geneAnalysis-output/genetic_distances.csv"
    
    # Read the genetic distance matrix
    headers, matrix = read_genetic_distances(distance_file)
    
    # Find the full name of the reference strain in the headers. Unique part of the strain name will do.
    reference_strain = None
    for header in headers:
        if reference_substr in header:
            reference_strain = header
            break
    
    # Check if reference strain was found.
    if not reference_strain:
        print(f"No strain containing '{reference_substr}' found in the distance matrix.")
        return
    
    # Index of the reference strain in each row
    ref_index = headers.index(reference_strain)
    
    # Collect genetic distances to reference strain, excluding reference vs. reference
    distances_to_ref = {}
    for strain, distances in matrix.items():
        if strain != reference_strain:  # Exclude reference vs. reference comparison.
            distances_to_ref[strain] = distances[ref_index - 1]  # Adjust for correct indexing.
    
    # Writing genetic distance information to a CSV file.
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Strain", "Genetic Distance to " + reference_strain])
        for strain, distance in distances_to_ref.items():
            writer.writerow([strain, distance])
    
  
# Run the main function with command line argument.
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: genetic_distances <reference_strain_part>")
        sys.exit(1)
    
    reference_substr = sys.argv[1]
    main(reference_substr)

