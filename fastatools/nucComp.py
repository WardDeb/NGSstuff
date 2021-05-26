from Bio import SeqIO
import argparse
import os
import csv
import sys

def slider(seq, win, step=1):
    seqlen = len(seq)
    if win % 2 != 0:
        print("Window size has to be an even number")
        sys.exit()
    for i in range(0,seqlen,step): #i is 0-indexed, so add one.
        pos = i + 1
        halfWin = win/2
        if pos < halfWin:
            start = 1
            stop = pos + halfWin
        elif pos + halfWin > seqlen:
            start = pos - halfWin
            stop = seqlen
        else:
            start = pos - halfWin
            stop = pos + halfWin
        yield pos, seq[int(start):int(stop)]
        if pos + halfWin > seqlen:
            break

def main():
    parser = argparse.ArgumentParser(description='Calculate nucleotide composition in fasta file.')
    parser.add_argument('-i', type=str, required=True,
                        help='point to fastafile')
    parser.add_argument('--window', type=int, default=100, required=False,
                        help='Size of the sliding window. [default 100]. Needs to be an even number.')
    args = parser.parse_args()

    if not os.path.exists(args.i):
        print('fasta file not found.')
        sys.exit()

    for seqrecord in SeqIO.parse(args.i, 'fasta'):
        outBase = seqrecord.id
        tempList = []
        seq = seqrecord.seq
        tempList.append(['pos','A','C','T','G','GC'])
        for baseStep, subseq in slider(seq, args.window,1):
            countA = subseq.count('A')
            countC = subseq.count('C')
            countT = subseq.count('T')
            countG = subseq.count('G')
            countGC = (countC + countG)
            tempList.append([
                baseStep,
                countA/args.window,
                countC/args.window,
                countT/args.window,
                countG/args.window,
                countGC/args.window
            ])
        # Write out data.
        with open(outBase + '.csv', 'w', newline='') as oFile:
            writer = csv.writer(oFile)
            writer.writerows(tempList)
        print("{} is parsed. File is called {}".format(outBase, outBase + '.csv'))

if __name__ == "__main__":
    main()
