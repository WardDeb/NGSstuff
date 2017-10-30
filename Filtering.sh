#!/usr/bin/env bash
#Initialize variables to default values.
OPT_1=-1
OPT_2=-1
OPT_3=-1
OPT_4=-1
OPT_f=0
#Set fonts for Help.
NORM=`tput sgr0`
BOLD=`tput bold`
REV=`tput smso`
cyan='\e[1;36m'
NC='\e[0m' # No Color

#Help function
function HELP {
  echo -e "Thank you Mark Zeller for the awesome fonts and help function!"\\n
  echo -e "This script will specifically select out all those contigs not annotated by DIAMOND, from a fasta file."
  echo -e "You can also immediately filter the output by minimum and maximum length of contigs, as well as coverage"
  echo -e "Following switches are recognized:"
  echo -e "Required:"
  echo -e "Filename: 'argument'.scaffolds.fasta"
  echo -e "1: exclude the contigs assigned by diamond, default = 0 (keep all contigs)"
  echo -e "Optional:"
  echo -e "Minimum length of scaffold/contig"
  echo -e "Maximum length of scaffold/contig"
  echo -e "Minimum coverage of scaffold/contig"
  echo -e "Maximum coverage of scaffold/contig"\\n
  exit 1
}

#Check the number of arguments. If none are passed, print help and exit.
NUMARGS=$#
if [ $NUMARGS -eq 0 ]; then
  HELP
fi


while getopts :a:f:1:2:3:4: FLAG; do
  case $FLAG in
    a)
      OPT_a=$OPTARG
      echo "-a was triggered, Filename= $OPTARG" >&2
      ;;
    f)
      OPT_f=$OPTARG
      echo "filter yes or no? $OPTARG" >&2
      ;; 
    1)
      OPT_1=$OPTARG
      echo "Minimum length of contig= $OPTARG" >&2
      ;;
    2)
      OPT_2=$OPTARG
      echo "Maximum length of contig= $OPTARG" >&2
      ;;
    3)
      OPT_3=$OPTARG
      echo "Minimum coverage of contig= $OPTARG" >&2
      ;;
    4)
      OPT_4=$OPTARG
      echo "Maximum coverage of contig= $OPTARG" >&2
      ;;
  esac
done
#Check if filterbyname is installed. If no, quit and exit
if ! type "filterbyname.sh" > /dev/null; then
  echo -e "You have not installed the bbmap toolkit. Tough luck"
  exit 1
fi

if [[ "$OPT_f" = "1" ]]; then
       if [ -z "$OPT_a.m8" ]; then
          echo -e "Hey mate, i cannot find the m8" >&2
          exit 1
       fi
       if [ -z "$OPT_a.scaffolds.fasta"]; then
          echo -e "Cannot find the scaffolds file" >&2
          exit 1
       fi
       cat $OPT_a.m8 | cut -f1 | sort -u > assnodes.txt
       filterbyname.sh in=$OPT_a.scaffolds.fasta out=unassignednodes.scaffolds.fasta names=assnodes.txt
       mv unassignednodes.scaffolds.fasta $OPT_a.unassignednodes.scaffolds.fasta
       rm assnodes.txt
       grep '>' $OPT_a.unassignednodes.scaffolds.fasta > unnodesname.txt 
fi
#We need to round of the coverage column or we will be screwed bigtime!
if [[ "$OPT_f" = "0" ]]; then
   grep '>' $OPT_a.scaffolds.fasta > unnodesname.txt
fi
mv unnodesname.txt unnodes.txt
sed 's/^.//' unnodes.txt > unnodesname.txt
rm unnodes.txt
awk -F '[_]' '{print $6}' unnodesname.txt > coveragetable.txt
awk '{printf("%.f\n",$0)}' coveragetable.txt > coveragetable_round.txt
paste unnodesname.txt coveragetable_round.txt -d _ | awk -F '[_]' '{ print $1"_"$2"_"$3"_"$4"_"$5"_"$NF"_"$7"_"$8; }' > testertje.txt
rm unnodesname.txt
rm coveragetable.txt
rm coveragetable_round.txt
mv testertje.txt unnodesname.txt

if [[ "$OPT_1" != "-1" ]]; then
	cat unnodesname.txt | awk -v minl=$OPT_1 -F '[_]' '$4>=minl {print $0}' > MINLnames.txt
	rm unnodesname.txt
	mv MINLnames.txt unnodesname.txt
fi

if [[ "$OPT_2" != "-1" ]]; then
	cat unnodesname.txt | awk -v maxl=$OPT_2 -F '[_]' '$4<=maxl {print $0}' > MINLnames.txt
	rm  unnodesname.txt
	mv MINLnames.txt unnodesname.txt
fi

if [[ "$OPT_3" != "-1" ]]; then
	cat unnodesname.txt | awk -v minc=$OPT_3 -F '[_]' '$6>=minc {print $0}' > MINLnames.txt
	rm  unnodesname.txt
	mv MINLnames.txt unnodesname.txt
fi

if [[ "$OPT_4" != "-1" ]]; then
	cat unnodesname.txt | awk -v maxc=$OPT_4 -F '[_]' '$6<=maxc {print $0}' > MINLnames.txt
	rm  unnodesname.txt
	mv MINLnames.txt unnodesname.txt
fi

cut -d '_' -f1-5 unnodesname.txt > unnodespattern
if [[ "$OPT_f" = "0" ]]; then
       filterbyname.sh in=$OPT_a.scaffolds.fasta out=filunass.fasta names=unnodespattern include=t substring=t
       mv filunass.fasta $OPT_a.filtered.scaffolds.fasta
fi
if [[ "$OPT_f" = "1" ]]; then
       filterbyname.sh in=$OPT_a.unassignednodes.scaffolds.fasta out=filunass.fasta names=unnodespattern include=t substring=t
       mv filunass.fasta $OPT_a.unassignednodes.filtered.scaffolds.fasta
fi
rm unnodesname.txt
rm unnodespattern
echo -e "Done"
