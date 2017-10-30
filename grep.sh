#!/usr/bin/env bash
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
cat $OPT_1.* > $OPT_1.FW.fq.gz
rm $OPT_1.R1.trimmed.fastq.gz
rm $OPT_1.R2.trimmed.fastq.gz
rm $OPT_1.unpaired.trimmed.fastq.gz
gunzip $OPT_1.FW.fq.gz
fastx_reverse_complement -z -i $OPT_1.FW.fq > $OPT_1.RV.fq.gz
gzip $OPT_1.FW.fq
cat $OPT_1.FW.fq.gz $OPT_1.RV.fq.gz > $OPT_1.grep.fq.gz
rm $OPT_1.FW.fq.gz
rm $OPT_1.RV.fq.gz
echo 'Done!'
