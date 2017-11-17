#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21:00:09 2017
Tool that puts all fasta sequ's in same ORF
@author: WD
This reverse complements sequence in a fasta file if the biggest ORF is found in the reverse strand
Keep in mind that IUPAC degenerate codes are not supported, only N
"""
from Bio import SeqIO
from Bio.Seq import Seq
import os
print('Give the name of the fasta file, including extension')
fasta = str(input())
print('How would you like to call the output? (include fasta extension)')
nameout = str(input())
#os.chdir("/Users/WD/Bioinf/")
#fasta = "Unctest.fasta"
count = 0
changecount = 0
seqfin = []
for seqrecord in SeqIO.parse(fasta, "fasta"):
    count +=1
    totallength = len(seqrecord.seq) - len(seqrecord.seq) % 3
    ORFlen = {}
    sequence = Seq(str(seqrecord.seq[0:totallength]))
    seqrevcomp = sequence.reverse_complement()
    ORF1 = max(len(i) for i in str(sequence.translate()).split('*'))
    ORF2 = max(len(i) for i in str(sequence[1:(totallength-2)].translate()).split('*'))
    ORF3 = max(len(i) for i in str(sequence[2:(totallength-1)].translate()).split('*'))
    ORF4 = max(len(i) for i in str(seqrevcomp.translate()).split('*'))
    ORF5 = max(len(i) for i in str(seqrevcomp[1:(totallength-2)].translate()).split('*'))
    ORF6 = max(len(i) for i in str(seqrevcomp[2:(totallength-1)].translate()).split('*'))
    ORFplus = [ORF1, ORF2, ORF3]
    ORFmin = [ORF4, ORF5, ORF6]
    if max(ORFmin) > max(ORFplus):
        changecount +=1
        seqrecord.seq = seqrecord.seq.reverse_complement()
    seqfin.append(seqrecord)
if changecount == 0:
    print('All sequences are in forward orientation, no output generated!')
else:
    print('In total' + ' '+ str(changecount) +' '+'out of' + ' ' + str(count)+ ' '+ 'sequences reverse complemented')
    SeqIO.write(seqfin,nameout,'fasta')
    print('Output generated: ' + str(nameout))
