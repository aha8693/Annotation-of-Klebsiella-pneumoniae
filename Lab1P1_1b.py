import sys

"""
Input: DNA string (may include mix of upper and lowercase)
Funtion: convert input DNA string into reversed complement DNA string
Output: reversed complement DNA string
"""

# Checking whether the input is in valid format (DNA string)
def checkBase(letter):
    possible_letters = ['A', 'T', 'C', 'G']
    if not letter.upper() in possible_letters:
        return False
    return True


line = sys.stdin.readline().strip()
base_dict = {'A':'T', 'T':'A', 'G':'C', 'C': 'G'}
output = ""

for i in range(len(line)-1, -1, -1):
    if (not checkBase(line[i])):
        sys.exit("Invalid base detected")
    # Upper-case base
    if ord(line[i]) < 91: 
        output += base_dict[line[i].upper()]
    # Lower-case base 
    else:
        output += base_dict[line[i].upper()].lower()

print(output)