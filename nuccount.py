#!/usr/bin/env python
#you need the regex module!
from __future__ import division
#also json module for easy writing
import json
import regex as re
#define the overlapping counter
def count_overlapping(text, search_for):
    return len(re.findall(search_for, text, overlapped=True))
from collections import defaultdict
frequs = defaultdict(list)
with open('total.fasta') as file:
  datalist = []
  for line in file:
    if line.startswith('>'):
      datalist.append([line.strip()[1:], ''])
    else:
      datalist[-1][1] += line.strip()
test = [(data[0],data[1].count('C')/len(data[1]), data[1].count('G')/len(data[1]), data[1].count('A')/len(data[1]), data[1].count('T')/len(data[1]), count_overlapping(data[1],'GC')/(len(data[1])), count_overlapping(data[1],'GA')/(len(data[1])), count_overlapping(data[1],'GT')/(len(data[1])), count_overlapping(data[1],'GG')/(len(data[1])), count_overlapping(data[1],'CC')/(len(data[1])), count_overlapping(data[1],'CA')/(len(data[1])), count_overlapping(data[1],'CT')/(len(data[1])), count_overlapping(data[1],'CG')/(len(data[1])), count_overlapping(data[1],'TC')/(len(data[1])), count_overlapping(data[1],'TA')/(len(data[1])), count_overlapping(data[1],'TT')/(len(data[1])), count_overlapping(data[1],'TG')/(len(data[1])), count_overlapping(data[1],'AC')/(len(data[1])), count_overlapping(data[1],'AA')/(len(data[1])), count_overlapping(data[1],'AT')/(len(data[1])), count_overlapping(data[1],'AG')/(len(data[1]))) for data in datalist]
print(test)
codons =['sample','C','G','A','T','GC','GA','GT','GG','CC','CA','CT','CG','TC','TA','TT','TG','AC','AA','AT','AG']
json.dump(test, open("freqtable.txt",'w'))
json.dump(codons, open("order.txt",'w'))
