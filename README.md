# web_blast

This program is used for NCBI web blast.
For various reasons, we may want to obtain the latest database blast result information, which is consistent with the NCBI result.

# about api
below url for more infomation :

https://ncbi.github.io/blast-cloud/dev/api.html

# usage

python web_blast.py [program] [database] [query]

  program should be one of megablast, blastn, blastp, rpsblast, blastx, tblastn, tblastx
  database  should be one of nr, cdd, nt
       
  **for example**:     
       python web_blast.py blastp nr protein.fasta
       
       python web_blast.py rpsblast cdd protein.fasta
       
       python web_blast.py megablast nt dna1.fasta dna2.fasta
