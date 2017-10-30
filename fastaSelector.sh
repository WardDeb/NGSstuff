#!/bin/bash

# ----------------------------------------------------------------
#
# fastaSelector v1.2
# Author: Tim Dierckx
# 
#
# This script is supplied "AS IS" without any warranties or support, without even implied fitness for a particular purpose.
# The author assumes no responsibility or liability for the use of the software.
#
# The author is painfully aware that this script does not play nice with a standard unix pipe.
# The author is also painfully aware that the script is rather slow. (A 4.2 Mb fasta is processed in ~2-3 minutes.)
# Text parsing is not something you should do in bash!
#
# Revision history: 
# 26-11-2015	Created 
# 11-12-2015    Changed the grep calls to avoid usage of the -P (perl-like regexes). Mac OSX doesn't use the GNU grep implementation and lacks this option.
#               the script now also keeps track of how many sequences meet the requirements.
#15-12-2015	Changed the ${LENGTHS[$counter]:8:-4} to a cut command because this functionality isn't present in OS X bash.
#		Really starting to regret choosing to implement this in shell scripting for portability. Perl or Python would've been better.
# ----------------------------------------------------------------

#Set Script Name variable
SCRIPT=`basename ${BASH_SOURCE[0]}`

#Initialize variables to empty strings.
COVERAGE_MIN=""
COVERAGE_MAX=0
LENGTH_MIN=""
LENGTH_MAX=0
INPUT_FASTA=""
OUTPUT_FASTA=""

#Set fonts for Help.
NORM=`tput sgr0`
BOLD=`tput bold`
REV=`tput smso`

#Help function
function HELP {
  echo -e \\n"Help documentation for ${BOLD}${SCRIPT}.${NORM}"\\n
  echo -e "${REV}Basic usage:${NORM} ${BOLD}$SCRIPT -i input.fasta -o output.fasta -c minCoverage -d maxCoverage -l minLength -m maxLength${NORM}"\\n
  echo -e "The -i -o -c and -l flags are mandatory and must be explicitely specified. -d and -m flags are optional."\\n
  echo "${REV}-i${NORM}  --Input fasta file. Sequences must be SINGLE LINES. No linebreaks are permitted."
  echo "${REV}-o${NORM}  --Output fasta file. Output will be appended to this file if it exists."
  echo "${REV}-c${NORM}  --Minimum coverage of accepted sequences."
  echo "${REV}-d${NORM}  --Maximum coverage of accepted sequences."
  echo "${REV}-l${NORM}  --Minimum length of accepted sequences."
  echo "${REV}-m${NORM}  --Maximum length of accepted sequences."
  echo -e "${REV}-h${NORM}  --Displays this help message."\\n
  echo -e "Example: ${BOLD}$SCRIPT -i scaffolds.fasta -o scaffolds.selected.fasta -l 100 -m 500 -c 0.5 -d 1.0"\\n
  exit 1
}

#Check the number of arguments. If none are passed, print help and exit. 
#If less than eight parameters are passed, then some required options were missed. (Why eight? Because -i -o -c and -l are mandatory)
NUMARGS=$#
#echo -e \\n"Number of arguments: $NUMARGS"
if [ $NUMARGS -eq 0 ]; then
  HELP
fi
if [ $NUMARGS -lt 8 ]; then
  HELP
fi

### Start getopts code ###

#Parse command line flags
#If an option should be followed by an argument, it should be followed by a ":".
#Notice there is no ":" after "h". The leading ":" suppresses error messages from
#getopts. This is required to get my unrecognized option code to work.

while getopts :c:d:l:m:h:i:o: FLAG; do
  case $FLAG in
    c)  #set option "c"
      COVERAGE_MIN=$OPTARG
      echo "Minimum coverage: $OPTARG"
      ;;
    d)  #set option "d"
      COVERAGE_MAX=$OPTARG
      echo "Maximum coverage: $OPTARG"
      ;;
    l)  #set option "l"
      LENGTH_MIN=$OPTARG
      echo "Minimum length: $OPTARG"
      ;;
    m)  #set option "m"
      LENGTH_MAX=$OPTARG
      echo "Maximum length: $OPTARG"
      ;;
    i)  #set option "i"
      INPUT_FASTA=$OPTARG
      echo "Input file: $OPTARG"
      ;;
    o)  #set option "o"
      OUTPUT_FASTA=$OPTARG
      echo "Output file: $OPTARG"
      ;;
    h)  #show help
      HELP
      ;;
    \?) #unrecognized option - show help
      echo -e \\n"The flag -${BOLD}$OPTARG${NORM} is not a valid option."
      HELP
      #If you just want to display a simple error message instead of the full
      #help, remove the 2 lines above and uncomment the 2 lines below.
      #echo -e "Use ${BOLD}$SCRIPT -h${NORM} to see the help documentation."\\n
      #exit 2
      ;;
  esac
done

shift $((OPTIND-1))  #This tells getopts to move on to the next argument.

### End getopts code ###


#Future code to make the script also accept less options and use intelligent default values.
if [ "$LENGTH_MIN" == "" ]; then
  echo -e \\n"Minimum Required Length Argument Absent"
  HELP
fi
if [ "$LENGTH_MAX" == "" ]; then
  echo -e \\n"Maximum Allowed Length Argument absent"
fi
if [ "$COVERAGE_MIN" == "" ]; then
  echo -e \\n"Minimum Coverage Required Argument absent"
  HELP
fi
if [ "$COVERAGE_MAX" == "" ]; then
  echo -e \\n"Maximum Allowed Coverage Argument absent"
fi
if [ "$INPUT_FASTA" == "" ]; then
  echo -e \\n"Input Fasta File Argument absent"
  HELP
fi
if [ "$OUTPUT_FASTA" == "" ]; then
  echo -e \\n"Output Fasta File Argument absent"
  HELP
fi


### Main ###

touch $OUTPUT_FASTA

# grep all lengths and put them into an array, grep all coverages and put them into an array. Test each array's i'th position for compliance with the limits, then grab the 2*ith and 2*i+1th line and put those into the output

#construct arrays
#line number maybe not needed, if counter variable is kept
#Problem: Mac OSX doesn't use the GNU implementation of grep, so the -P option isn't present.
#LENGTHS=($(grep -Po "(?<=_length_)[0-9]+(?=_cov)" $INPUT_FASTA))
#LENGTHS_LINENUM=($(grep -Pon "(?<=_length_)[0-9]+(?=_cov)" $INPUT_FASTA | cut -f1 -d: ))
#COVERAGES=($(grep -Po "(?<=_cov_)[0-9\.]+(?=_ID)" $INPUT_FASTA))
#COVERAGES_LINENUM=($(grep -Pon "(?<=_cov_)[0-9\.]+(?=_ID)" $INPUT_FASTA | cut -f1 -d: ))

#construct arrays
#changed previous implementation using the substring of a variable selection using ${LENGTHS[$counter]:8:-4} to a cut command.
LENGTHS=($(grep -o "_length_.*_cov" $INPUT_FASTA | cut -d '_' -f 3))
LENGTHS_LINENUM=($(grep -on "_length_.*_cov" $INPUT_FASTA | cut -f1 -d: ))

COVERAGES=($(grep -o "_cov_.*_ID" $INPUT_FASTA | cut -d '_' -f 3))
COVERAGES_LINENUM=($(grep -on "_cov_.*_ID" $INPUT_FASTA | cut -f1 -d: ))



#quick sanity check if there are an equal amount of Lengths and Coverages
if [ ${#LENGTHS[@]} -ne ${#COVERAGES[@]} ]; then
  echo -e \\n"ERROR: Unequal amounts of lengths and coverages found in $INPUT_FASTA."
  exit 1
fi

#for each item in the lengths and coverages array, test if they meet the requirements set in the parameters.
# if the requirements are met, then append the line to the output file
counter=0
writtenlines=0
#four different cases: 1) only minima are set, maxes are both 0 2) only both minima + max length are set, 3) only both minima + max cov are set 4) all four parameters are set.
#as it turns out, bash doesn't support testing floating point numbers. *le sigh*
#The heart and soul of the script here: the seds, if the length and coverage exeeds or equals the minumums set in the options, then write the line to the output.
#this could probably be written as a function and then called though.
echo "Working..."
while [ $counter -lt ${#LENGTHS[@]} ]; do
  if [ "$(echo "$LENGTH_MAX == 0" | bc)" -eq "1" ] && [ "$(echo "$COVERAGE_MAX == 0" | bc)" -eq "1" ]; then
    if [ ${LENGTHS[$counter]} -ge $LENGTH_MIN ] && [ "$(echo "${COVERAGES[$counter]} >= $COVERAGE_MIN" | bc)" -eq "1" ] ; then
      sed -n ${LENGTHS_LINENUM[$counter]}p "$INPUT_FASTA" >> $OUTPUT_FASTA
      sed -n $((${LENGTHS_LINENUM[$counter]}+1))p "$INPUT_FASTA" >> $OUTPUT_FASTA
      writtenlines=$((writtenlines+1))
    fi
  elif [ "$(echo "$LENGTH_MAX == 0" | bc)" -eq "1" ]; then
    if [ ${LENGTHS[$counter]} -ge $LENGTH_MIN ] && [ "$(echo "${COVERAGES[$counter]} >= $COVERAGE_MIN" | bc)" -eq "1" ] && [ "$(echo "${COVERAGES[$counter]} <= $COVERAGE_MAX" | bc)" -eq "1" ] ; then
      sed -n ${LENGTHS_LINENUM[$counter]}p "$INPUT_FASTA" >> $OUTPUT_FASTA
      sed -n $((${LENGTHS_LINENUM[$counter]}+1))p "$INPUT_FASTA" >> $OUTPUT_FASTA
      writtenlines=$((writtenlines+1))
    fi
  elif [ "$(echo "$COVERAGE_MAX == 0" | bc)" -eq "1" ]; then
    if [ ${LENGTHS[$counter]} -ge $LENGTH_MIN ] && [ "$(echo "${COVERAGES[$counter]} >= $COVERAGE_MIN" | bc)" -eq "1" ] && [ ${LENGTHS[$counter]} -le $LENGTH_MAX ] ; then
      sed -n ${LENGTHS_LINENUM[$counter]}p "$INPUT_FASTA" >> $OUTPUT_FASTA
      sed -n $((${LENGTHS_LINENUM[$counter]}+1))p "$INPUT_FASTA" >> $OUTPUT_FASTA
      writtenlines=$((writtenlines+1))
    fi
  else
    if [ ${LENGTHS[$counter]} -ge $LENGTH_MIN ] && [ "$(echo "${COVERAGES[$counter]} >= $COVERAGE_MIN" | bc)" -eq "1" ] && [ ${LENGTHS[$counter]} -le $LENGTH_MAX ] && [ "$(echo "${COVERAGES[$counter]} <= $COVERAGE_MAX" | bc)" -eq "1" ] ; then
      sed -n ${LENGTHS_LINENUM[$counter]}p "$INPUT_FASTA" >> $OUTPUT_FASTA
      sed -n $((${LENGTHS_LINENUM[$counter]}+1))p "$INPUT_FASTA" >> $OUTPUT_FASTA
      writtenlines=$((writtenlines+1))
    fi
  fi
  counter=$((counter+1))
done





### End Main ###
echo "Kept $writtenlines fasta sequences."
echo "Work Complete."
exit 0
