#Idea is to take a fastq file (single end) and return a random subset of this, defined by N (input).
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import random
import sys,getopt
import pandas
import warnings
warnings.filterwarnings("ignore")
def main(argv):
   inputfile = ''
   outputfile = ''
   n = ''
   r = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:n:k:r:",["ifile=","ofile=","permutationstep=","kmer","iter"])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile> -n <samplesize> -k <kmer>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-n", "--samplesize"):
         n = arg
      elif opt in ("-k", "--kmer"):
         k = arg
      elif opt in ("-r", "--iter"):
         r = arg
   print 'Input file is :', inputfile
   print 'Output file is :', outputfile
   print 'take samples in steps of :', n
   print 'Kmer to use:', k
   print 'Iterations/kmer:', r
   with open(str(inputfile)) as f:
       sequs = []
       numseq = 0
       for seq in SeqIO.parse(inputfile,"fastq"):
           seqlist = [seq.id, seq.seq]
           sequs.append(seqlist)
           numseq +=1
       print(numseq)
       steps = (range(int(n),int(numseq),int(n)))
       finlist = []
       permdic = {}
       stepcounter = 0
       for x in steps:
           num_of_kmers = []
           counter = 0
           stepcounter +=1
           print('step ' + str(stepcounter) + ' of ' + str(len(steps)))
           for i in range(int(r)):
               randomsam = random.sample(sequs,int(x))
               kmerdict = {}
               counter +=1
               print('iteration ' + str(counter) + ' of ' + str(r))
               for record in randomsam:
                   seq = record[1]
                   for i in range(len(seq) - int(k) + 1):
                       kmer = seq[i:i+int(k)]
                       if kmerdict.has_key(kmer):
                           kmerdict[kmer] += 1
                       else:
                           kmerdict[kmer] = 1
               num_of_kmers.append(len(kmerdict.keys()))
           name = "permsize_" + str(x)
           permdic[name] = num_of_kmers
       print(permdic)
       pd = pandas.DataFrame.from_dict(permdic)
       pd.to_csv("output.csv")
if __name__ == "__main__":
    main(sys.argv[1:])
