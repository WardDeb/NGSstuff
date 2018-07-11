from Bio import SeqIO
import sys,getopt

def main(argv):
    inputfile = ''
    outputfile = ''
    n = ''
    try:
        opts,args = getopt.getopt(argv,"hi:o:n:", ["ifile=","ofile=","size="])
    except getopt.GetoptError:
        print('I need an inputfile (fasta, -i), an outputname (fasta, -o) and a minimun length of sequences (number, -n)')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('I need an inputfile (fasta, -i), an outputname (fasta, -o) and a minimun length of sequences (number, -n)')
            sys.exit(2)
        if opt == '-i':
            inputfile = arg
        if opt == '-o':
            outputfile = arg
        if opt == '-n':
            n = arg
    print('Inputfile = ' + str(inputfile))
    print('Outpufile = ' + str(outputfile))
    print('Minimumsize = ' + str(n))
    fasta = SeqIO.parse(open(inputfile),'fasta')
    filtered = []
    count = 0
    countfil = 0
    for seq in fasta:
        count +=1
        if len(seq.seq) > int(n):
            filtered.append(seq)
            countfil += 1
    SeqIO.write(filtered, outputfile, 'fasta')
    print('File written.')
    print('Output is called: '+ str(outputfile))
    print(str(countfil) + ' out of ' + str(count) + ' total contigs retained.')
if __name__ == "__main__":
    main(sys.argv[1:])
