import sys

def convert(fglimmer, fgtf):
    f = open(fgtf, "w")
    rf = open(fglimmer, "r")
    seqname = "."
    for line in rf.readlines():
        # source, feature, start, end, score, strand, frame, attribute
        gtf_args = ["."] * 8
        if '>' == line.split()[0][0]:
            seqname = line.split()[0][1:] #seqname
            if not seqname:
                seqname = "."
            continue
        gtf_args[0] = "glimmer3" #source
        gtf_args[1] = "CDS" #feature
        
        # Handling empty column "." in the .predict file
        column_counter = 0
        try:
            column_counter = 2
            gtf_args[2] = int(line.split()[1]) #start
            column_counter = 3
            gtf_args[3] = int(line.split()[2]) #end
            gtf_args[4] = line.split()[4] #score
            gtf_args[5] = line.split()[3][0] #strand
        except ValueError:
            if column_counter == 2:
                try:
                    gtf_args[3] = int(line.split()[2])
                except ValueError: # Both start and end values are missing
                    gtf_args[2] = "."
                    gtf_args[3] = "."
                else: # Only start value is missing
                    gtf_args[2] = "."
            if column_counter == 3: # Only end value is missing
                gtf_args[3] = "."
            gtf_args[4] = line.split()[4] #score
            gtf_args[5] = line.split()[3][0] #strand
        else:
            if gtf_args[2] > gtf_args[3]:
                if line.split()[3][0] == '-':
                    # reverse the order
                    gtf_args[2] = line.split()[2]
                    gtf_args[3] = line.split()[1]
                else: #circular
                    continue # Exclude this gene
        
        try:
            gtf_args[6] = int(line.split()[3][1:]) - 1 #frame
        except ValueError:
            gtf_args[6] = "."
        
        gtf_args[7] = "transcript_id \"{}\"".format(line.split()[0]) #attribute
        f.write('{}\t'.format(seqname))
        f.write('\t'.join(map(str, gtf_args)))
        f.write("\n")
    f.close()



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Not enough argument")
        sys.exit()
    convert(*sys.argv[1:])


