#!/bin/bash
while getopts ":a:" opt; do
   case $opt in
     a)
       OPT_1=$OPTARG
       echo "-a is triggered for the sam file, goodstuff." >&2
       ;;
   esac
done
bwa mem -R "@RG\tID:FLOWCELL1.LANE1\tPL:ILLUMINA\tLB:test\tSM:PA01" VDV_NC_006494.fasta ../$OPT_1.R1.trimmed.fastq.gz ../$OPT_1.R2.trimmed.fastq.gz -t 32 >$OPT_1.sam
java -jar ~/prog_scripts/picard/picard.jar SortSam I=$OPT_1.sam O=$OPT_1.sort.bam SORT_ORDER=coordinate
java -jar ~/prog_scripts/picard/picard.jar MarkDuplicates I=$OPT_1.sort.bam O=$OPT_1.dedup.bam METRICS_FILE=$OPT_1.metrics.txt
java -jar ~/prog_scripts/picard/picard.jar BuildBamIndex INPUT=$OPT_1.dedup.bam
java -jar ~/prog_scripts/GenomeAnalysisTK.jar -T RealignerTargetCreator -R VDV_NC_006494.fasta -I $OPT_1.dedup.bam -o $OPT_1.list
java -jar ~/prog_scripts/GenomeAnalysisTK.jar -T IndelRealigner -R VDV_NC_006494.fasta -I $OPT_1.dedup.bam -targetIntervals $OPT_1.list -o $OPT_1.real.bam
java -jar ~/prog_scripts/GenomeAnalysisTK.jar -T HaplotypeCaller -R VDV_NC_006494.fasta -I $OPT_1.real.bam -o $OPT_1.raw.vcf
echo "removing some tempcrap"
rm $OPT_1.sam
rm $OPT_1.sort.bam
rm $OPT_1.dedup.bam
rm $OPT_1.metrics.txt
rm $OPT_1.real.bam
rm *.bai
rm $OPT_1.list
echo "done haha"
