# Neighbor joining algorithm code from www.github.com/anicksaha/neighbor_joining.

from node import Node
import neighbour_joining
import utils
import bootstrap
import sys

def main(filename):

    # First step is to read the file and get the sequences
    ids, sequences = utils.read_fasta_file(filename)

    # Then generate the distance matrix
    distance_matrix = utils.get_distance_matrix(ids, sequences)

    # write the distances.txt file (distance matrix)
    distance_matrix_filename = 'geneAnalysis-output/genetic_distances.txt'
    utils.write_distance_matrix(ids, distance_matrix, distance_matrix_filename)
    
    # This is used to number nodes in the tree to be constructed
    sequence_counter = 120
    # Run the nei saitu algorithm. Returns the root of the tree
    root = neighbour_joining.nei_saitou(ids, distance_matrix, sequence_counter)
    
    # Writing the edge file
    edge_file_filename = 'edges.txt'
    # utils.write_edge_file(root, edge_file_filename)
    
    # Writing the newick file
    
    # we will only use one tree.txt -- obtained from fullSequence comparison.
    
    # newick_file_filename = 'tree.txt'
    # utils.write_newick_file(ids, root, newick_file_filename)
 
    # bootstrap calculations
    percentages = bootstrap.bootstrap(root, ids, sequences)
    # bootstrap.write_bootstrap(percentages)
    

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3.11 main_NJ.py <path_to_ffn_file>")
        sys.exit(1)  # Exit the script indicating error.

    ffn_file_path = sys.argv[1]
    main(ffn_file_path)

