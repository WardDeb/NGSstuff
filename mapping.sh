#!/usr/bin/env bash
while getopts ":a:b:" opt; do
  case "$opt" in
    a)
      OPT_1=$OPTARG
      echo "-a was triggered, Parameter: $OPTARG" >&2
      ;;
    b)
      OPT_2=$OPTARG
      echo "-b was triggered, the reference is: $OPTARG" >&2
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

bwa index $OPT_2.fasta
bwa mem $OPT_2.fasta $OPT_1.R1.trimmed.fastq.gz $OPT_1.R2.trimmed.fastq.gz -t 32 > $OPT_1.sam
samtools faidx $OPT_2.fasta
samtools view -SbT $OPT_2.fasta $OPT_1.sam > $OPT_1.paired.bam

bwa mem $OPT_2.fasta $OPT_1.unpaired.trimmed.fastq.gz -t 32 > $OPT_1.unpaired.sam
samtools view -SbT $OPT_2.fasta $OPT_1.unpaired.sam > $OPT_1.unpaired.bam
samtools merge $OPT_1.sorted.bam $OPT_1.paired.bam $OPT_1.unpaired.bam
samtools sort $OPT_1.sorted.bam $OPT_1.sorted
samtools index $OPT_1.sorted.bam

echo -e "Finished: output file $OPT_1.sorted.bam"
