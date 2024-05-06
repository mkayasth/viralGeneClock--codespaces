from Bio import Entrez, SeqIO
import requests

# replace with YOUR email id. This here is mine:
Entrez.email = "mkayasth@ramapo.edu"

# mapping accession numbers to strain names
accession_to_strain = {
    "NC_045512": "Wuhan",
    "OR075545": "XBB.1.16",
    "OQ608429": "XBB.1.5",
    "OR598953": "EG.5",
    "PP292788": "AY.3",
    "OR813619": "BA.2.86",
    "OR829491": "CH.1.1",
    "PP250483": "BF.10",
    "PP316714": "JN.1",
    "PP435534": "HV.1"
}

output_file = "sample_input.fasta"

with open(output_file, 'w') as outfile:
    for accession, strain_name in accession_to_strain.items():
        try:
            handle = Entrez.efetch(db="nucleotide", id=accession, rettype="fasta", retmode="text")
            record = SeqIO.read(handle, "fasta")
            
            # replacing the header with the strain name
            record.id = strain_name
            record.description = strain_name
            
            # writing the modified sequence to the output file
            SeqIO.write(record, outfile, "fasta")
            handle.close()
            print(f"Successfully fetched and added {strain_name}")
        except Exception as e:
            print(f"Failed to fetch {accession} ({strain_name}): {e}")

print("Success! All sequences have been written to:", output_file)
