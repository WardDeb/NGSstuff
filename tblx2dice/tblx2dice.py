#WD
#Tested on Mac / python 3.6.5
import sys,getopt
from scipy.spatial.distance import squareform
import pandas as pd
from collections import defaultdict
import numpy as np
import networkx as nx
def graph(inputfile):
    graphdic = {}
    tracker = []
    with open(inputfile) as blasfile:
        for line in blasfile:
            blasline = line.strip().split()
            if float(blasline[2]) > 30 and float(blasline[4]) > 30:
                quer = str(blasline[0])
                subj = str(blasline[1])
                couplestring = quer + ' ' + subj
                revstring = subj + ' ' + quer
                if couplestring not in tracker and revstring not in tracker:
                    if quer not in graphdic:
                        graphdic[quer] = [subj]
                        tracker.append(couplestring)
                        tracker.append(revstring)
                    else:
                        if subj not in graphdic[quer]:
                            graphdic[quer].append(subj)
                            tracker.append(couplestring)
                            tracker.append(revstring)
    graphx = nx.Graph(graphdic)
    nx.write_graphml(graphx,'graph.xml')
def blxparser(inputfile,outputfile):
    parsedic = {}
    selfdic = {}
    survivors = []
    with open(inputfile) as blasfile:
        for line in blasfile:
            blasline = line.strip().split()
            if float(blasline[2]) > 30 and float(blasline[4]) > 30:
                couplestring = str(blasline[0]) + ' ' + str(blasline[1])
                revstring = str(blasline[1]) + ' ' + str(blasline[0])
                bit = float(blasline[11])
                if revstring not in parsedic:
                    if couplestring in parsedic:
                        oldbit = parsedic[couplestring]
                        newbit = float(oldbit) + bit
                        parsedic[couplestring] = newbit
                    else:
                        parsedic[couplestring] = bit
    for i in parsedic:
        spltstr = i.split(" ")
        if spltstr[0] == spltstr[1]:
            selfdic[spltstr[0]] = parsedic[i]
    for i in selfdic:
        spltstr = i.split(" ")
        survivors.append(spltstr[0])
    qvect = []
    svect = []
    distvec = []
    distdic = {}
    for i in parsedic:
        spltstr = i.split(" ")
        if spltstr[0] in survivors and spltstr[1] in survivors and spltstr[0] != spltstr[1]:
            ABbit = float(parsedic[i])
            AAbit = float(selfdic[spltstr[0]])
            BBbit = float(selfdic[spltstr[1]])
            finbit = ((2 * ABbit)/(AAbit + BBbit))
            qvect.append(spltstr[0])
            svect.append(spltstr[1])
            distvec.append(finbit)
            leistje = (str(spltstr[0]),str(spltstr[1]))
            distdic[leistje] = finbit
    nestdic = defaultdict(dict)
    for (q,s), value in distdic.items():
        nestdic[q][s] = value
        nestdic[s][q] = value
    df = pd.DataFrame(nestdic)
    np.fill_diagonal(df.values, 0)
    df = df.dropna()
    df.to_csv(outputfile)
def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts,args = getopt.getopt(argv,"hi:o:", ["ifile=","ofile="])
    except getopt.GetoptError:
        print('I need an inputfile (-i) (tblx, outfmt6), and outputname (-o).')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('I need an inputfile (-i) (tblx, outfmt6), and outputname (-o).')
            sys.exit(2)
        if opt == '-i':
            inputfile = arg
        if opt == '-o':
            outputfile = arg
    if inputfile == '':
        print('I need an inputfile')
        sys.exit(2)
    if outputfile == '':
        print('I need an outputfile')
        sys.exit(2)
#    blxparser(inputfile,outputfile)
    graph(inputfile)
if __name__ == "__main__":
    main(sys.argv[1:])
