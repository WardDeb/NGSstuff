#WD
#Tested on Mac / python 3.6.5
#Assumes your VCF's to be sitting in subfolder VCF
#Also filters VCF on quality 20
import sys
import getopt
import os
from Bio import SeqIO
from Bio.Seq import Seq
def parser(gfffile, fastafile, vcffile):
    gffout = gfffile.strip().split('.')[0] + '.rev.gff'
    neglist = []
    fixlist = []
    keeptrack = 0
    totalline = 0
    with open(gfffile) as prot:
        for line in prot:
            totalline += 1
            if str(line.strip().split()[6]) == "-":
                neglist.append(line.strip())
        if len(neglist) == 0:
            print("No - strand products found, aborting the mission")
            sys.exit(2)
        global contiglength
        contiglength = int(neglist[0].split("_")[4])
        for orf in neglist:
            newstart = contiglength - int(orf.split()[4]) + 1
            newstop = contiglength - int(orf.split()[3]) + 1
            newlist = [orf.split()[0],orf.split()[1],orf.split()[2],str(newstart),str(newstop),"+",orf.split()[7],orf.split('\t')[8]]
            newstr = '\t'.join(newlist)
            fixlist.append(newstr)
            keeptrack += 1
    with open(gffout, "w") as f:
        for line in fixlist:
            line2 = line + "\n"
            f.write(line2)
    f.close()
    print("Fixed GFFfile written: " + str(keeptrack)+ " ORFs out of: " + str(totalline) + " were on negative strand")
    for sequ in SeqIO.parse(fastafile, "fasta"):
        fastaout = fastafile.strip().split('.')[0] + '.rev.fasta'
        seq2 = sequ.seq.reverse_complement()
        sequ.seq = seq2
        with open(fastaout,'w') as f:
            SeqIO.write(sequ,f,"fasta")
    print('revcomp fasta written')
    fixvcf = []
    with open(vcffile) as vcf:
        for line in vcf:
            if line[0] == "#":
                fixvcf.append(line.strip())
            else:
                posswitch = contiglength - int(line.split()[1]) + 1
                posswitchline = [line.split()[0],str(posswitch),line.split()[2],line.split()[3],line.split()[4],line.split()[5],line.split()[6],line.split()[7],line.split()[8]]
                newstr = '\t'.join(posswitchline)
                fixvcf.append(newstr)
    vcfout = vcffile.strip().replace(".vcf","") + '.rev.vcf'
    with open(vcfout,'w') as f:
        for line in fixvcf:
            line2 = line + "\n"
            f.write(line2)
    print("VCF written, Done")
def main(argv):
    gfffile = ''
    fastafile = ''
    vcffile = ''
    try:
        opts,args = getopt.getopt(argv,"h:g:f:v:", ["gfffile=","fastafile","vcffile"])
    except getopt.GetoptError:
        print('Need gfffile (-g), fastafile(-f) and vcffile(-v) ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Need gfffile (-g), fastafile(-f) and vcffile(-v)')
            sys.exit(2)
        if opt == '-g':
            gfffile = arg
        if opt == '-f':
            fastafile = arg
        if opt == '-v':
            vcffile = arg
    if gfffile == '':
        print('I need a gfffile(-g)')
        sys.exit(2)
    if fastafile == '':
        print('I need a fastafile (-f)')
        sys.exit(2)
    if vcffile == '':
        print('I need a vcffile (-v)')
        sys.exit(2)
    parser(gfffile,fastafile,vcffile)
if __name__ == "__main__":
    main(sys.argv[1:])
