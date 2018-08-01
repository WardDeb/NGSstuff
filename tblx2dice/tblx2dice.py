#WD
#Tested on Mac / python 3.6.5
#TODO: leave clique calc for sofisticated algorithm
# Parse a simple txt list and spew out distance matrix by crossing against given blast file
import sys,getopt
from scipy.spatial.distance import squareform
import pandas as pd
from collections import defaultdict
import numpy as np
import networkx as nx
from networkx.algorithms.approximation import clique
#def graph(inputfile):
#    graphdic = {}
#    tracker = []
#    linetracker = 1
#    print("Parsing the blastfile to generate network...")
#    num_lines = sum(1 for line in open(inputfile))
#    edgelist = []
#    selftrack = []
#    with open(inputfile) as blasfile:
#        for line in blasfile:
#            print("Reading line: " + str(linetracker) + " out of " + str(num_lines))
#            linetracker += 1
#            blasline = line.strip().split()
#            if float(blasline[2]) > 0 and float(blasline[4]) > 0:
#                quer = str(blasline[0])
#                subj = str(blasline[1])
#                sublist = [quer, subj]
#                if quer not in graphdic:
#                    graphdic[quer] = [subj]
#                else:
#                    if subj not in graphdic[quer]:
#                        graphdic[quer].append(subj)
#                if sublist not in edgelist:
#                    edgelist.append(sublist)
#                if quer == subj:
#                    selftrack.append(quer)
    #for k,v in graphdic.items():
    #    print(v)
    #    for i in range(0,len(v)):
    #        edgelist.append([k,v[i]])
    #        nodelist.append(k)
    #        nodelist.append(v[i])
#    graphx = nx.MultiGraph()
#    graphx.add_edges_from(edgelist)
#    for i in edgelist:
#        comb = i[0] + ' ' + i[1]
#        print(comb)
    #print(graphx.nodes())
    #print("number of nodes:")
    #print(len(graphx))
    #print("nodes of self loops:")
    #print(list(nx.nodes_with_selfloops(graphx)))
    #nx.write_graphml(graphx,'graph.xml')
    #print("Graph written")
    #print(len(selftrack))
    #print(selftrack)
    #cliq = list(clique.max_clique(graphx))
    #print(cliq)
    #global larglist
    #larglist = list(cliq)
def blxparser(inputfile,outputfile):
    parsedic = {}
    selfdic = {}
    survivors = []
    with open(inputfile) as blasfile:
        for line in blasfile:
            blasline = line.strip().split()
            if float(blasline[2]) > 0 and float(blasline[4]) > 0:
                if blasline[0] in larglist and blasline[1] in larglist:
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
    print(selfdic)
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
    print(nestdic)
    df = pd.DataFrame(nestdic)
    np.fill_diagonal(df.values, 0)
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
#    graph(inputfile)
#    blxparser(inputfile,outputfile)
if __name__ == "__main__":
    main(sys.argv[1:])
