from Bio import SeqIO
import argparse

def slider(seq, win, step=1):
    seqlen = len(seq)
    for i in range(0,seqlen,step):
        j = seqlen if i+win>seqlen else i+win
        yield seq[i:j]
        if j==seqlen: break

y = []
i = 1
windowslice = 100


#GC percentage calculation per slide:
for seqrecord in SeqIO.parse("RREWT.fasta", 'fasta'):
    templist = []
    seq = seqrecord.seq
    print ("A"+'\t'+"C"+'\t'+"T"+'\t'+"G"+'\t'+"GC")
    for subseq in slider(seq, windowslice,1):
        countA = subseq.count('A')
        countC = subseq.count('C')
        countT = subseq.count('T')
        countG = subseq.count('G')
        countGC = countC + countG
        print (str(countA/windowslice)+'\t'+str(countC/windowslice)+'\t'+str(countT/windowslice)+'\t'+str(countG/windowslice)+'\t'+str(countGC/windowslice))
