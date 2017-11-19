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
    length = len(seqrecord.seq)
    nowindow = length // 1000
    for i in range(1,(int(nowindow)+1)):
        test = SeqUtils.GC(seqrecord.seq[(i*1000)-1000:(i*1000)])
        oneid = str(seqrecord.id.split(sep="_")[0] + seqrecord.id.split(sep="_")[1] + '_' + seqrecord.id.split(sep="_")[8] ) +' ' + str((i*1000)-1000) + ' ' + str((i*1000)) + ' ' + str(test)
        print(oneid)
    testje = SeqUtils.GC(seqrecord.seq[((int(nowindow)*1000)):])
    twoid = str(seqrecord.id.split(sep="_")[0] + seqrecord.id.split(sep="_")[1] + '_' + seqrecord.id.split(sep="_")[8] ) + ' ' + str((nowindow*1000)) + ' ' + str(length) + ' ' + str(round(testje,1))
    print(twoid)
