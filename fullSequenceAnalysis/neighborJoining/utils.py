# # Neighbor joining algorithm code from www.github.com/anicksaha/neighbor_joining.

def read_fasta_file(filename):
    """
    Function that reads the given fasta file and gets the sequences.
    """
    sequences = {}
    ids = []
    with open(filename) as f:
        lines = f.read().splitlines()
    curr = None
    for index, line in enumerate(lines):
        if line.startswith('>'):
            curr = line[1:]
            ids.append(curr)
        else:
            sequences[curr] = line
    return ids, sequences

def get_distance(seq1, seq2):
    """
    Function to calculate the distance between two sequences as a helper.
    """
    total = len(seq1)
    mismatch = 0
    for i in range(total):
        if seq1[i] != seq2[i]:
            mismatch += 1
    if mismatch == 0:
        return 0
    return mismatch / float(total)

def get_distance_matrix(ids, sequences):
    """
    Function to get the overall distance matrix for all the sequences.
    """
    total = len(ids)
    matrix = [[0] * total for _ in range(total)]
    for i, id1 in enumerate(ids):
        for j, id2 in enumerate(ids):
            if i != j:
                matrix[i][j] = get_distance(sequences[id1], sequences[id2])
    return matrix

def write_distance_matrix(ids, matrix, filename):
    """
    Writes the distance matrix to a file.
    """
    num_ids = len(ids)
    with open(filename, 'w') as f:
        # First append the row of ids.
        f.write('\t' + '\t'.join(ids) + '\n')
        for i in range(num_ids):
            f.write(ids[i] + '\t' + '\t'.join(map(str, matrix[i])) + '\n')

def write_newick_file(seqIds, root, filename):
    """
    Uses post order traversal to write the newick file.
    """
    def postorder_traversal(node):
        if not node.children:
            return seqIds[int(node.id) - 1]
        visited = []
        for child, distance in node.children.items():
            visited.append(postorder_traversal(child) + ':' + str(distance))
        return '(' + ','.join(visited) + ')'
    
    newick = postorder_traversal(root) + ';'
    with open(filename, 'w') as f:
        f.write(newick)

def preOrder(root, visited=None):
    """
    Uses preorder traversal to traverse the tree and collect edge information.
    """
    if visited is None:
        visited = []
    if root is None or root.children is None:
        return visited
    for child, distance in root.children.items():
        visited.append((root.id, child.id, distance))
        preOrder(child, visited)
    return visited

def write_edge_file(root, filename):
    """
    Writes the edge information to a file.
    """
    visited = preOrder(root)
    with open(filename, 'w') as f:
        for (parent, child, distance) in visited:
            f.write(f'{parent}\t{child}\t{str(distance)}\n')

