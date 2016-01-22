rm -f *.faa
./extractCDS.py "$1" ../ref/*.faa
./fasta_script.py *.faa
./dmini.py > tree
njplot tree
