<h2> Introduction </h2>
Using ViralGeneClock, the users can deposit the whole genome sequence (WGS) of different strains of a virus. The tool then examines the evolutionary relationship of the strains, and also estimates the relative mutation rates of the genes across these strains. It leverages Prokka for viral genome annotation, Muscle for multiple sequence alignment of each gene for different strains and the Neighbor Joining Algorithm for determining genetic distances and branch lengths. ViralGeneClock utilizes the genetic distance and branch length data to then provide relative mutation rates for each annotated gene. This is primarily a Linux tool developed through the Linux subsystem; the environment for running ViralGeneClock can be simulated using Github's Codespaces.<br> <br>

The final .zip folder is emailed to the provided address. Outputs from the full genome analysis is saved in the folder <b>fullSequence-output</b>. Results from gene-specific analyses are saved in the folder <b> geneAnalysis-output</b>, and the output for relative mutation rates is saved in the folder <b>avg_mutation_rate_final</b>.

<h2> Installations </h2>
Create a new Github codespace, and clone the repository <i>mkayasth/viralGeneClock--codespaces</i> into your codespace. Using the terminal of the codespace, install the following dependencies:

<h3>1) Prokka:</h3>
Use the Bioconda channel to install Prokka: <br> <br>

 ```shell
conda install -c conda-forge -c bioconda -c defaults prokka
```

<h3>2) MUSCLE:</h3>
 
 ```shell
wget http://www.drive5.com/muscle/downloads3.8.31/muscle3.8.31_i86linux32.tar.gz
tar -zxvf muscle3.8.31_i86linux32.tar.gz
chmod +x muscle3.8.31_i86linux32
```

<h3>3) Python3 Dependencies:</h3>

```shell
pip install matplotlib
pip install biopython
pip install flask
pip install flask-mail
```

<h2> Usage </h2>
After completing necessary installations, run the web app with app.py :) <br> <br>

 ```shell
python3 app.py
```

Alternatively, you can use the command line interface with main.py (app.py calls main.py using the subprocess library). <br>

 ```shell
python3 main.py <input_fasta_file> <reference strain>
```
The <input_fasta_file> comprises the complete set of whole genome sequences (WGS) for the strains you intend to analyze. Each strain's FASTA header should be the name of the strain.
