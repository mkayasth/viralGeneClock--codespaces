# uses Biopython & matplotlib to plot phylogenetic tree from tree.txt produced by neighbor-joining.

from Bio import Phylo
import matplotlib.pyplot as plt

# Parsing the Newick string to create a Phylo tree object.
tree = Phylo.read("fullSequence-output/tree.txt", "newick")


fig = plt.figure(figsize=(20, 15), dpi=300)
axes = fig.add_subplot(1, 1, 1)

# formatting the branch labels to 3 significant figures.
def format_branch_length(clade):
    if clade.branch_length is not None:
        return f"{clade.branch_length:.3g}"


Phylo.draw(tree, do_show=False, axes=axes, branch_labels=format_branch_length)


axes.set_title('Phylogenetic Tree', fontsize=26)

# Setting style for the tree lines.
for line in axes.get_lines():
    line.set_linewidth(3)

for lbl in axes.findobj(match=lambda obj: isinstance(obj, plt.Text)):
    lbl.set_fontsize(16)
    



# Saving the figure to a JPEG file.
plt.savefig("fullSequence-output/tree.jpg", format='jpg', dpi=300)

plt.close(fig)
