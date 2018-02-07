import os
with open('totaldepth.txt','r') as f:
    for line in f:
        oneid = str(line.split(sep="_")[1] + line.split(sep="_")[2] + '_' + line.split(sep="_")[0] + " "  +line.split("\t")[1] + " " + line.split("\t")[2])
        print(oneid)
