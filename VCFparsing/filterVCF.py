#WD
#Tested on Mac / python 3.6.5
#Assumes your VCF's to be sitting in subfolder VCF
import sys
import getopt
import os
def parser(inputfile, input2):
    sampleslist = []
    fastalist = []
    with open(inputfile) as headers:
        for line in headers:
            samline = line.strip()
            sampleslist.append(samline)
    print("samplelist parsed.")
    with open(input2) as fasters:
        for line in fasters:
            fasline = line.strip()
            fastalist.append(fasline)
    print("fastalist parsed.")
    writecounter = 0
    filetracker = 0
    for sample in sampleslist:
        for fasta in fastalist:
            outname = sample + '.' + fasta + '.VCF'
            outlist = []
            vcfstring = "vcf/" + sample + ".QUAL20.vcf"
            with open(vcfstring) as vcffile:
                filetracker += 1
                for line in vcffile:
                    if fasta in line:
                        outlist.append(line)
            if len(outlist) != 0:
                with open(outname, "w") as f:
                    for line in outlist:
                        f.write(line)
                f.close()
                writecounter += 1
    print(str(writecounter) + ' VCF files written. Total times file is opened:' + str(filetracker))
def main(argv):
    inputfile = ''
    input2 = ''
    try:
        opts,args = getopt.getopt(argv,"h:i:f:", ["ifile=","ofile="])
    except getopt.GetoptError:
        print('Need sample list (-i), fastasurvivorlist (-f) and VCF under relative subfolder vcf/sample.QUAL20.vcf')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Need sample list (-i), fastasurvivorlist (-f) and VCF under relative subfolder vcf/sample.QUAL20.vcf')
            sys.exit(2)
        if opt == '-i':
            inputfile = arg
        if opt == '-f':
            input2 = arg
    if inputfile == '':
        print('I need a sample list(-i)')
        sys.exit(2)
    if input2 == '':
        print('I need a fastasurvivorlist (-f)')
        sys.exit(2)
    parser(inputfile,input2)
if __name__ == "__main__":
    main(sys.argv[1:])
