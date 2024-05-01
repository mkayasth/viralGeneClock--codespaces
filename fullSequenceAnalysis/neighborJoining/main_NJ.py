# Neighbor joining algorithm code from www.github.com/anicksaha/neighbor_joining.

from node import Node
import neighbour_joining
import utils
import bootstrap
import sys

def main(filename):

    output_directory = 'fullSequence-output/'
    
    # First step is to read the file and get the sequences
    ids, sequences = utils.read_fasta_file(filename)

    # Then generate the distance matrix
    distance_matrix = utils.get_distance_matrix(ids, sequences)

    # write the distances.txt file (distance matrix)
    distance_matrix_filename = output_directory + 'genetic_distances.txt'
    utils.write_distance_matrix(ids, distance_matrix, distance_matrix_filename)
    
    # This is used to number nodes in the tree to be constructed
    sequence_counter = 120
    # Run the nei saitu algorithm. Returns the root of the tree
    root = neighbour_joining.nei_saitou(ids, distance_matrix, sequence_counter)
    
    # Writing the edge file
    # edge_file_filename = output_directory + 'edge_file.txt'
    # utils.write_edge_file(root, edge_file_filename)

   
    # Writing the newick file
    newick_file_filename = output_directory + 'tree.txt'
    utils.write_newick_file(ids, root, newick_file_filename)

    # bootstrap calculations
    percentages = bootstrap.bootstrap(root, ids, sequences)
    

if __name__ == '__main__':
	# this always runs on the output produced by Muscle. so hardcoded the input file.
    hardcoded_path = 'fullSequence-output/fullSequence_aligned_sequences.ffn'
    main(hardcoded_path)
