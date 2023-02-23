import sys

"""
Input: Multi-FASTA file of an assembly or a set of DNA sequences
Funtion: Calculate N50 of input file
Output: N50 size
"""
# Checking if intput is an invalid file 
try:
    filename = sys.stdin
except Exception:
    sys.exit("error occured")

total_length = 0
contig = []
base = ['A','T','C','G','a','c','t','g']

for line in filename.readlines():
    # Catching sequence identifier
    if line[0] == '>':
        continue
    
    # Checking if input is in FASTA format or not
    # Checking is done loosely, as this program assumes that the input is FASTA (According to the direction)
    for i in range(5):
        if line[i] not in base:
            sys.exit("Not in a FASTA format")
    
    # Appending length of each contig and calculate total sum length of contigs
    contig.append(len(line))
    total_length += len(line)

contig.sort(reverse=True)
sum_length = 0
for length in contig:
    sum_length += length
    # If this length exceeds the 50% of total sum length, print it
    if sum_length > total_length/2:
        print("N50:", length)
        break
