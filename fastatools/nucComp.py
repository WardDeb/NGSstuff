from Bio import SeqIO
import argparse
import os
import csv

def slider(seq, win, step=1):
    seqlen = len(seq)
    for i in range(0,seqlen,step):
        j = seqlen if i+win>seqlen else i+win
        yield seq[i:j]
        if j==seqlen: break

def main():
    parser = argparse.ArgumentParser(description='Calculate nucleotide composition in fasta file.')
    parser.add_argument('-i', type=str, required=True,
                        help='point to fastafile')
    parser.add_argument('--window', type=int, default=100, required=False,
                        help='Size of the sliding window.')
    args = parser.parse_args()

    if not os.path.exists(args.i):
        print('fasta file not found.')
        sys.exit()

    for seqrecord in SeqIO.parse(args.i, 'fasta'):
        outBase = seqrecord.id
        tempList = []
        seq = seqrecord.seq
        tempList.append(['A','C','T','G','GC'])
        for subseq in slider(seq, args.window,1):
            countA = subseq.count('A')
            countC = subseq.count('C')
            countT = subseq.count('T')
            countG = subseq.count('G')
            countGC = (countC + countG)
            tempList.append([
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
