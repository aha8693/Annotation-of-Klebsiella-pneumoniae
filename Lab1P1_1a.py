import sys

"""
Input: FASTQ file
Funtion: convert FASTQ file to FASTA file
        Note) this program assumes the input could be either multi- or single-FASTQ file
Output: FASTA file
"""
# Checking if intput is an invalid file 
try:
    filename = sys.stdin
except Exception:
    sys.exit("error occured")

linenumb = 1
base = ['A','G','T','C','a','g','t','c']
for line in filename.readlines():
    # Line1: Sequence identifier 
    if linenumb==1 and line[0]=='@':
        print('>', line[1:], sep="", end="")
        linenumb += 1
        continue
    # Line2: Raw sequence letters
    elif linenumb==2 and line[0] in base:
        print(line, end="")
        linenumb += 1
        continue
    # Line3: Markers with optional sequence identifier
    elif linenumb==3 and line[0]=='+':
        linenumb += 1
        continue
    # Line4: Quality values labeled in ASCII order
    # !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
    elif linenumb == 4:
        linenumb = 1
        continue
    
    # Catching different format - invalid input file
    else:
        sys.exit("Invalid FASTQ format")