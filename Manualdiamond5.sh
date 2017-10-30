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

cat $OPT_1.m8 | cut -f1 > $OPT_1.txt
sort -u $OPT_1.txt > $OPT_1.u.txt
test=$(head -1 $OPT_1.u.txt)
grep -m 5 $test $OPT_1.m8 > $OPT_1.man5.m8
sed '1d' $OPT_1.u.txt > tmpfile; mv tmpfile $OPT_1.u.txt 
while read line;do grep -m 5 $line $OPT_1.m8 >> $OPT_1.man5.m8; done < $OPT_1.u.txt
rm -rf $OPT_1.txt
rm -rf $OPT_1u.txt