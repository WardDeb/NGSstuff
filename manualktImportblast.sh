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

ktImportBLAST -o $OPT_1.man5.html $OPT_1.man5.m8,$OPT_1 $OPT_1.man5.m8:$OPT_1.man5.magnitudes,$OPT_1.magnitudes
