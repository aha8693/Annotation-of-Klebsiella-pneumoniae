import sys

"""
output: a list [attribute1, attribute2]
"""
def search(next_line, ffaa):
    f_faa = open(ffaa, "r")
    output = ["."]*2
    accession = next_line.split()[0]
    output[0] = accession 
    for gene_info in f_faa.readlines():
        if accession in gene_info:
            gene_full_info = gene_info.split()[1:]
            for i in range(len(gene_full_info)):
                if '[' in gene_full_info[i]:
                    output[1] = " ".join(gene_full_info[:i])
                    return output
                else:
                    output[1] = " ".join(gene_full_info)
            return output
    return output
    f_faa.seek(0)

"""
[0seqname, 1source, 2feature, 3start, 4end, 5score*, 
 6strand, 7frame*, 8attribute1, 9attribute2]

"""

def convert(fmummer, ffaa, output):
    f = open(output, "w")
    f_mummer = open(fmummer, "r")
    

    lines = f_mummer.read().splitlines()
    for i in range(len(lines)):
        field = ["."] * 10
        if '>' in lines[i]:
            field[0] = lines[i].split()[1]
            field[1] = 'MUMmer4' # source
            field[2] = "CDS" #feature
            field[6] = "+"
            if 'Reverse' in lines[i]:
                field[6] = "-"
            try:
                nextline = lines[i+1]
            except IndexError:
                f.write("\t".join(map(str, field[:8])))
                f.write("\tmatch=none;")
                f.write("\n")
                continue
                
            if not '>' in nextline:
                search_result = search(nextline, ffaa)
                field[8] = search_result[0]
                field[9] = search_result[1]
                field[3] = int(nextline.split()[2])
                field[4] = field[3] + int(nextline.split()[3]) - 1
            
            f.write("\t".join(map(str, field[:8])))
            if field[8] == ".":
                f.write("\tmatch=none;")
                f.write("\n")
            else: 
                f.write("\tmatch={}; \"{}\"".format(field[8], field[9]))
                f.write("\n")
    f.close()
    


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Not enough argument")
        sys.exit()
    if not sys.argv[2].endswith('.faa'):
        print("Invalid file extension")
        sys.exit()
        # Cannot handle error for mummer file type, since the instruction
        # has not specified which file extension to use. 
    convert(*sys.argv[1:])