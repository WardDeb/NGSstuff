#python3
from Bio import SeqIO
from Bio.Seq import Seq
import os
#print('Give the name of the fasta file, including extension')
#fasta = str(input())
#print('How would you like to call the output?')
#nameout = str(input())
fasta = str("Virsortercat12.len10000.fna")
counter = 1
for seqrecord in SeqIO.parse(fasta, "fasta"):
    strid = seqrecord.id
    print('chr - '+ strid.split('_')[1]+strid.split('_')[2]+'_'+ strid.split('_')[0]+ ' ' + str(counter) + ' 0 ' + str(len(seqrecord.seq)) + ' black')
    counter += 1 
