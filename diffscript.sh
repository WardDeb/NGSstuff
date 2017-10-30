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
cat $OPT_1.m8 | cut -f1 | sort -u > assnodes.txt
filterbyname.sh in=$OPT_1.scaffolds.fasta out=unassignednodes.scaffolds.fasta names=assnodes.txt
mv unassignednodes.scaffolds.fasta $OPT_1.unassignednodes.scaffolds.fasta
rm assnodes.txt