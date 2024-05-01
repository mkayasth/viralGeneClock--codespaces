<h1> AdvBIIN-Project: ViralGeneClock. </h1>

<h2> Introduction </h2>
Using ViralGeneClock, the users can deposit the whole genome sequence (WGS) of different strains of a virus. The tool then examines the evolutionary relationship of the strains, and also estimates the relative mutation rates of the genes across these strains. It leverages Prokka for viral genome annotation, Muscle for multiple sequence alignment of each gene for different strains and the Neighbor Joining Algorithm for determining genetic distances and branch lengths. ViralGeneClock utilizes the genetic distance and branch length data to then provide relative mutation rates for each annotated gene. This is primarily a Linux tool developed through the Linux subsystem; the environment for running ViralGeneClock can be simulated using Github's Codespaces.<br> <br>

The final .zip folder is emailed to the provided address. Outputs from the full genome analysis is saved in the folder <b>fullSequence-output</b>. Results from gene-specific analyses are saved in the folder <b> geneAnalysis-output</b>, and the output for relative mutation rates is saved in the folder <b>avg_mutation_rate_final</b>.


