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

samtools idxstats $OPT_1.sorted.bam | cut -f1,3 > $OPT_1.man5.magnitudes
