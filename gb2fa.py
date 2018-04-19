from Bio import SeqIO
import sys,getopt

def main(argv):
    inputfile = ''
    outputfile = ''
    n = ''
    try:
        opts,args = getopt.getopt(argv,"hi:o:", ["ifile=","ofile="])
    except getopt.GetoptError:
        print('I need an inputfile (fasta, -i), and outputname (fasta, -o)')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('I need an inputfile (fasta, -i), and outputname (fasta, -o)')
            sys.exit(2)
        if opt == '-i':
            inputfile = arg
        if opt == '-o':
            outputfile = arg
    print('Inputfile = ' + str(inputfile))
    print('Outpufile = ' + str(outputfile))
    SeqIO.convert(inputfile, "genbank", outputfile, "fasta")
if __name__ == "__main__":
    main(sys.argv[1:])
