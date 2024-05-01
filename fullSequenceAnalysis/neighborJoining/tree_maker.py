# uses Biopython & matplotlib to plot phylogenetic tree from tree.txt produced by neighbor-joining.

from Bio import Phylo
import matplotlib.pyplot as plt

# Parse the Newick string to create a Phylo tree object.
tree = Phylo.read("fullSequence-output/tree.txt", "newick")

# Set up a matplotlib figure.
fig = plt.figure(figsize=(15, 10), dpi=100)
axes = fig.add_subplot(1, 1, 1)


Phylo.draw(tree, do_show=False, axes=axes, branch_labels=lambda c: c.branch_length)

axes.set_title('Phylogenetic Tree', fontsize=24)

# setting style.
for line in axes.get_lines():
	line.set_linewidth(3)
plt.setp(axes.get_xticklabels(), fontsize=20)
plt.setp(axes.get_yticklabels(), fontsize=20)

# Saving the figure to a JPEG file.
plt.savefig("fullSequence-output/tree.jpg", format='jpg', dpi=300)

plt.close(fig)
