#WD
#Tested on Mac / python 3.6.5
import sys,getopt
def blxparser(inputfile):
    parsedic = {}
    with open(inputfile) as blasfile:
        for line in blasfile:
            blasline = line.strip().split()
            if float(blasline[2]) > 30 and float(blasline[4]) > 30: 
                key,value = str(blasline[0]),str(blasline[1])
                if key not in parsedic:
                    parsedic[key] = [value]
                if key in parsedic and value != parsedic[key]:
                    parsedic[key].append(value)
        for line in blasfile:
            blasline = line.strip().split()
            if float(blasline[2] > 30 and float(blasline[4]) > 30:
                
    for i in parsedic:
        print(i, parsedic[i])
def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts,args = getopt.getopt(argv,"hi:o:", ["ifile=","ofile="])
    except getopt.GetoptError:
        print('I need an inputfile (-i) (tblx, outfmt6), and outputname (-o).')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('I need an inputfile (-i) (tblx, outfmt6), and outputname (-o).')
            sys.exit(2)
        if opt == '-i':
            inputfile = arg
        if opt == '-o':
            outputfile = arg
    if inputfile == '':
        print('I need an inputfile')
        sys.exit(2)
    if outputfile == '':
        print('I need an outputfile')
        sys.exit(2)
    blxparser(inputfile)
if __name__ == "__main__":
    main(sys.argv[1:])
