#python3
#For now window length = 500, can be variable, still to implement.
from Bio import SeqIO
from Bio.Seq import Seq
from Bio import SeqUtils
import os
#print('Give the name of the fasta file, including extension')
fasta = str("phages_nuc.fasta")
#print('How would you like to call the output?')
#nameout = str(input())
count = 0
changecount = 0
gcstat = []
for seqrecord in SeqIO.parse(fasta, "fasta"):
    count +=1
    GC = SeqUtils.GC(seqrecord.seq)
    print(str(seqrecord.id) + ' ' + str(GC))
