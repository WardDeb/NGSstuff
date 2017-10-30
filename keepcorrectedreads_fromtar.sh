#!/bin/bash
while getopts ":a:" opt; do
   case $opt in
     a)
        OPT_1=$OPTARG
        echo "a triggered"
        ;;
     esac
done
echo "Finding corrected reads"
tar xvf $OPT_1.tar.gz --wildcards *cor.fastq.gz
echo "unpacked! removing tarball"
rm $OPT_1.tar.gz
echo "Done!"
