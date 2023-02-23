import fileinput
import sys

def calculate_helper(seq):
    """
    Input: a string of DNA sequence 
    Funtion: For every 3 DNAs (1 codon), calculate its frequency
    Output: a dictionary of {codon:frequency} for {key:value}
    """
    seq_str = "".join(seq)
    prob_dict = {}
    length = len(seq_str)
    for i in range(0, length, 3):
        codon = str(seq_str[i:i+3])
        if not codon in prob_dict:
            prob_dict[codon] = 1
        else:
            prob_dict[codon] += 1
    return prob_dict

def update(temp_dict, final_prob_dict):
    """
    Input: temp_dict) dictionary for one specific ORFs - {codon: frequnecy} for {key:value}
           final_prob_dict) dictionary for whole ORFs
    Funtion: Update final_prob_dict by adding frequency from temp_dict
    Output: return updated final_prob_dict
    """
    for key in temp_dict.keys():
        if key in final_prob_dict:
            final_prob_dict[key] += temp_dict[key]
        else:
            final_prob_dict[key] = temp_dict[key]
    return final_prob_dict

def calculate(orfseq):
    """
    Input: a file of ORFs sequence 
    Funtion: Calculate 61 codons' probability in the input sequence file
    Output: Print 61 codons and their probability in stdout
    """
    final_prob_dict = {}
    seq = []
    total_length = 0

    lines = orfseq.read().splitlines()
    for i in range(len(lines)):
        if '>' in lines[i]:
            # Edge case - First ORF
            if i == 0:
                # Just to make sure that this ORF is composed of 3x DNA (codons)
                length = int(lines[i].split()[3][4:])
                assert(length%3 == 0)
                # Sum up ORF's lengths for the probability calculation at the end
                total_length += length
                continue
            
            # Count each codon's frequency for this ORF, store it into a temporary dictionary.
            temp_dict = calculate_helper(seq)
            # Update the final dictionary with the previously made dictionary.
            final_prob_dict = update(temp_dict, final_prob_dict)
            # Reset DNA sequnece to store another ORF
            seq = []

            length = int(lines[i].split()[3][4:])
            assert(length%3 == 0)
            total_length += length
            continue
        
        # Sum up all the DNA sequences without new line into one list
        seq.append(lines[i].rstrip())

        # Edge case - last ORF
        if i == len(lines) - 1:
            temp_dict = calculate_helper(seq)
            final_prob_dict = update(temp_dict, final_prob_dict)

    # Sort codons by converting keys into list
    key_list = list(final_prob_dict.keys())
    key_list.sort()

    # A codon is made out of 3 DNAs (Total_length = number of all the DNAs)
    total_length /= 3
    for key in key_list:
        # Print 61 codons and relative probability
        print("{}\t{}".format(key, final_prob_dict[key]/total_length))

if __name__ == "__main__":
    calculate(sys.stdin)