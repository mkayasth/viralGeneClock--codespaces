# calculates branch length of each strain to reference strain from tree.txt (newick format) produced by the FULL SEQUENCE main_NJ.py.
# sum of each branch length to reference strain if not a direct relationship to reference strain.


import csv
from Bio import Phylo
import sys

def find_path_to_reference(tree, target_strain, reference_strain):
    # Simplify names for comparison, focusing on primary identifier.
    simplified_target_strain = target_strain.split('|')[0]
    simplified_reference_strain = reference_strain.split('|')[0]
    
    # Finding common ancestor based on simplified names.
    common_ancestor = tree.common_ancestor({"name": simplified_target_strain}, {"name": simplified_reference_strain})
    target_distance = tree.distance(simplified_target_strain, common_ancestor)
    reference_distance = tree.distance(simplified_reference_strain, common_ancestor)
    return target_distance + reference_distance

def main(reference_substr):
    # Paths for the input and output files.
    # output -- csv file will be deleted when run thru the main python scripts.
    tree_file = "fullSequence-output/tree.txt"
    output_file = "geneAnalysis-output/branch_length.csv"
    
    # Read the full-genome tree for branch length.
    tree = Phylo.read(tree_file, "newick")
    
    # Attempt to find the full name of the reference strain in the tree. Writing a part of reference strain unique will work.
    reference_strain = None
    for clade in tree.find_clades():
        if clade.name:
            simplified_clade_name = clade.name.split('|')[0]
            if reference_substr in simplified_clade_name:  # Improved matching logic.
                reference_strain = clade.name
                break
    
    if not reference_strain:
        # Early exit if reference strain is not found
        print(f"No strain containing '{reference_substr}' found in the tree.")
        return
    
    distances = []
    # Compute distances for all strains except the reference
    for clade in tree.find_clades():
        if clade.name and clade.name != reference_strain:
            distance_to_reference = find_path_to_reference(tree, clade.name, reference_strain)
            distances.append([clade.name, distance_to_reference])
    
    # Write distances to CSV.
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Strain", "Distance to " + reference_strain])
        writer.writerows(distances)
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: branch_length.py <reference_strain_part>")
        sys.exit(1)
    
    reference_substr = sys.argv[1]
    main(reference_substr)

