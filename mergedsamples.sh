#!/usr/bin/env bash

set -e

while getopts ":a:" opt; do
  case $opt in
    a)
      OPT_1=$OPTARG
      echo "-a was triggered, Parameter: $OPTARG" >&2
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

/home/viroom/SPAdes-3.8.1-Linux/bin/spades.py -t 32 -k 21,33,55,77 -s $OPT_1.trimmed.fastq.gz -o $OPT_1

cd $OPT_1
mv scaffolds.fasta $OPT_1.scaffolds.fasta
mv contigs.fasta $OPT_1.contigs.fasta

/home/viroom/diamond/diamond blastx -d /home/viroom/NGS_data/DIAMONDDAT/nrfil -q $OPT_1.scaffolds.fasta -a $OPT_1 -p 32 --sensitive -c 1
/home/viroom/diamond/diamond view -d /home/viroom/NGS_data/DIAMONDDAT/nrfil -a $OPT_1.daa -o $OPT_1.m8
rm $OPT_1.daa

bwa index $OPT_1.scaffolds.fasta
bwa mem $OPT_1.scaffolds.fasta ../$OPT_1.trimmed.fastq.gz -t 32 > map.sam
samtools faidx $OPT_1.scaffolds.fasta
samtools view -SbT $OPT_1.scaffolds.fasta map.sam > $OPT_1.bam
samtools sort $OPT_1.bam $OPT_1
samtools index $OPT_1.bam

samtools idxstats $OPT_1.bam | cut -f1,3 > $OPT_1.magnitudes
ktImportBLAST -o $OPT_1.html $OPT_1.m8,$OPT_1 $OPT_1:$OPT_1.magnitudes,$OPT_1magn
