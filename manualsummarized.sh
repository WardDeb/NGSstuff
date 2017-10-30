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

ktClassifyBLAST $OPT_1.man5.m8 -o $OPT_1.man5.tab
awk 'NR==FNR { a[$1]=$2; next} $1 in a {print $0,"\t"a[$1]}' $OPT_1.man5.magnitudes $OPT_1.man5.tab > $OPT_1.man5.magnitudes.tab
python /home/viroom/scripts/SummarizeRanks.py -i $OPT_1.man5.magnitudes.tab -1 $OPT_1.man5.SummarizedByFamily.tab -2 $OPT_1.man5.SummarizedBySubfamily.tab -3 $OPT_1.man5.SummarizedByGenus.tab -4 $OPT_1.man5.SummarizedBySpecies.tab