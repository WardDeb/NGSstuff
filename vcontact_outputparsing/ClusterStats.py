#WD
#Tested on Mac / python 3.6.5
import os
from os.path import isfile, join
from os import listdir
import sys,getopt
from pathlib import Path
import pandas as pd
import subprocess
import shutil
###TODO:
# 1. Add if statement that checks for output already present and aborts.
# 4. Incorporate Pvals & QUAL in VC_LCA.txt
# 5. In VC_LCA, make sure VC's are dropped in order
# 6. Internal / external weights?

def Clusstats(inputfile):
    Allnodes = []
    with open(inputfile) as clusfile:
        for line in clusfile:
            clus = line.split(",")[7].strip()
            if clus != 'Members':
                genomelist = clus.split(' ')
                clus1 = [w.replace('"','') for w in genomelist]
                clus2 = [w.replace('~','') for w in clus1]
                Allnodes.extend(clus2)
    countdict = {x:Allnodes.count(x) for x in Allnodes}
    TotalVC = 0
    NODE_only = 0
    REF_only = 0
    mixed = 0
    noNODE_OL = []
    noNODE_NOL = []
    allNODE_OL = []
    allNODE_NOL = []
    someNODE_OL = []
    someNODE_NOL = []
    percnoNODE_OL = ['VC# %OLREF #REFs']
    percnoNODE_NOL = ['VC# #REFs']
    percsomeNODE_OL = ['VC# %OLNODE %OLREF Clustersize #NODE #REF']
    percsomeNODE_NOL = ['VC# Clustersize #NODE #REF']
    percallNODE_OL = ['VC# %OLNODE #NODEs']
    percallNODE_NOL = ['VC# #NODEs']
    with open(inputfile) as clusfile:
        for line in clusfile:
            VC = 'VC' + line.split(",")[0]
            clus = line.split(",")[7].strip()
            if clus != 'Members':
                TotalVC += 1
                genomelist = clus.split(' ')
                clus1 = [w.replace('"','') for w in genomelist]
                clus2 = [w.replace('~','') for w in clus1]
                cluscount = [ countdict.get(item,item) for item in clus2 ]
                Nodenum = sum('_NODE_' in s for s in clus2)
                VCdic = dict(zip(clus2,cluscount))
                if Nodenum == len(clus2):
                    NODE_only += 1
                    if sum(cluscount)/len(clus2) == 1:
                        allNODE_NOL.append(VC)
                        appstr = VC + ' ' + str(len(clus2))
                        percallNODE_NOL.append(appstr)
                    if sum(cluscount)/len(clus2) != 1:
                        allNODE_OL.append(VC)
                        for key in list(VCdic.keys()):
                            if VCdic[key] == 1:
                                del VCdic[key]
                        OLperc = len(VCdic.keys())/len(clus2)
                        appstr = VC + ' ' +str(format(OLperc, '.2f'))+ ' ' + str(len(clus2))
                        percallNODE_OL.append(appstr)
                if Nodenum == 0:
                    REF_only += 1
                    if sum(cluscount)/len(clus2) == 1:
                        noNODE_NOL.append(VC)
                        appstr = VC + ' ' +str(len(clus2))
                        percnoNODE_NOL.append(appstr)
                    if sum(cluscount)/len(clus2) != 1:
                        noNODE_OL.append(VC)
                        for key in list(VCdic.keys()):
                            if VCdic[key] == 1:
                                del VCdic[key]
                        OLperc = len(VCdic.keys())/len(clus2)
                        appstr = VC + ' ' +str(format(OLperc, '.2f'))+ ' ' + str(len(clus2))
                        percnoNODE_OL.append(appstr)
                if Nodenum != 0 and Nodenum != len(clus2):
                    mixed += 1
                    if sum(cluscount)/len(clus2) == 1:
                        someNODE_NOL.append(VC)
                        numNODE = sum('_NODE_' in s for s in list(VCdic.keys()))
                        appstr = VC + ' ' + str(len(clus2)) + ' ' + str(numNODE) + ' ' +str(len(clus2)-numNODE)
                        percsomeNODE_NOL.append(appstr)
                    if sum(cluscount)/len(clus2) != 1:
                        someNODE_OL.append(VC)
                        for key in list(VCdic.keys()):
                            if VCdic[key] == 1:
                                del VCdic[key]
                        numOLNODE = sum('_NODE_' in s for s in list(VCdic.keys()))
                        numOLREF = len(VCdic.keys()) - numOLNODE
                        OLpercNODE = numOLNODE/len(clus2)
                        OLpercREF = numOLREF/len(clus2)
                        appstr = VC + ' ' +str(format(OLpercNODE, '.2f'))+ ' ' +str(format(OLpercREF, '.2f'))+ ' ' + str(len(clus2)) + ' ' +str(numOLNODE) + ' ' + str(numOLREF)
                        percsomeNODE_OL.append(appstr)
        print('TotalVC: '+str(TotalVC))
        print('VC with only NODES: '+str(NODE_only))
        print('VC with only REFs: '+str(REF_only))
        print('VC that contain both: '+str(mixed))
        print('noNODE_OL: '+str(len(noNODE_OL)))
        print('noNODE_NOL: '+str(len(noNODE_NOL)))
        print('someNODE_OL: '+str(len(someNODE_OL)))
        print('someNODE_NOL: '+str(len(someNODE_NOL)))
        print('allNODE_OL: '+str(len(allNODE_OL)))
        print('allNODE_NOL: '+str(len(allNODE_NOL)))
        print('\n')
        print('noNODE_OL: '+ '\t' +' '.join(noNODE_OL))
        print('noNODE_NOL: '+ '\t' +' '.join(noNODE_NOL))
        print('someNODE_OL: '+ '\t' +' '.join(someNODE_OL))
        print('someNODE_NOL: '+ '\t' +' '.join(someNODE_NOL))
        print('allNODE_OL: '+ '\t' +' '.join(allNODE_OL))
        print('allNODE_NOL: '+ '\t' +' '.join(allNODE_NOL))
        print('\n'.join(percnoNODE_OL))
        print('\n'.join(percnoNODE_NOL))
        print('\n'.join(percsomeNODE_OL))
        print('\n'.join(percsomeNODE_NOL))
        print('\n'.join(percallNODE_OL))
        print('\n'.join(percallNODE_NOL))
        if os.path.exists("Clusstats"):
            shutil.rmtree('Clusstats')
            print("Clusstats folder already exists, overwriting...")
        os.makedirs("Clusstats")
        text_file = open('Clusstats/noNODE_OL.txt', "w")
        text_file.write('\n'.join(percnoNODE_OL))
        text_file.close()
        text_file = open('Clusstats/noNODE_NOL.txt', "w")
        text_file.write('\n'.join(percnoNODE_NOL))
        text_file.close()
        text_file = open('Clusstats/someNODE_OL.txt', "w")
        text_file.write('\n'.join(percsomeNODE_OL))
        text_file.close()
        text_file = open('Clusstats/someNODE_NOL.txt', "w")
        text_file.write('\n'.join(percsomeNODE_NOL))
        text_file.close()
        text_file = open('Clusstats/allNODE_OL.txt', "w")
        text_file.write('\n'.join(percallNODE_OL))
        text_file.close()
        text_file = open('Clusstats/allNODE_NOL.txt', "w")
        text_file.write('\n'.join(percallNODE_NOL))
        text_file.close()

def dropOLREF(inputfile):
    Allnodes = []
    with open(inputfile) as clusfile:
        for line in clusfile:
            clus = line.split(",")[7].strip()
            if clus != 'Members':
                genomelist = clus.split(' ')
                clus1 = [w.replace('"','') for w in genomelist]
                clus2 = [w.replace('~',' ') for w in clus1]
                Allnodes.extend(clus2)
    countdict = {x:Allnodes.count(x) for x in Allnodes}
    with open(inputfile) as clusfile:
        if os.path.exists("NoOLClusters.csv"):
            os.remove("NoOlClusters.csv")
            print("NoOLClusters.csv already existed, overwriting...")
        TotalVC = 0
        Survivors = 0
        for line in clusfile:
            clus = line.split(",")[7].strip()
            VC = 'VC' + line.split(",")[0]
            if clus != 'Members':
                TotalVC += 1 
                genomelist = clus.split (' ')
                clus1 = [w.replace('"','') for w in genomelist]
                clus2 = [w.replace('~',' ') for w in clus1]
                cluscount = [ countdict.get(item,item) for item in clus2 ]
                VCdic = dict(zip(clus2,cluscount))
                for key in list(VCdic.keys()):
                    if VCdic[key] != 1:
                        del VCdic[key]
                for key in list(VCdic.keys()):
                    if '_NODE_' in str(key):
                        del VCdic[key]
                if len(VCdic.keys()) != 0:
                    Survivors += 1
                    with open('NoOLClusters.csv','a') as f:
                        VC = VC + ";"
                        writestring = VC + ','.join(list(VCdic.keys()))+'\n'
                        f.write(writestring)
        print(str(Survivors) + ' of in total: '+ str(TotalVC) + ' have survived, Outfile written: noOLClusters.csv')
def getLCA():
    if os.path.exists("Acclist"):
        shutil.rmtree('Acclist')
        print("Acclist folder already exists, overwriting...")
    os.makedirs("Acclist")
    with open('NoOLClusters.csv') as clusfile:
        dumpnames = pd.read_csv("names.dmp", sep="\t", usecols = [0,2], header=None)
        writenumber = 0
        for line in clusfile:
            members = line.split(";")[1]
            keeptrack = line.split(";")[0]
            listmem = members.split(",")
            clustergenomelist = []
            for genome in listmem:
                if "NODE" not in genome:
                     if genome == "Candidatus Liberibacter phage SC1":
                         tempgenome == "Liberibacter phage SC1"
                     if genome == "Candidatus Liberibacter phage SC2":
                         tempgenome == "Liberibacter phage SC2"
                     if genome == "T4-like Synechococcus phage S-MbCM100":
                         tempgenome == "Synechococcus phage S-MbCM100"
                     if genome == "T4-like Synechococcus phage metaG-MbCM1":
                         tempgenome == "Synechococcus phage metaG-MbCM1"
                     else:
                         tempgenome = genome.replace("~"," ")
                     clustergenomelist.append(tempgenome)
                vcstring = dumpnames[dumpnames[2].isin(clustergenomelist)]
                outputfile = "Acclist/" + str(keeptrack) + ".acc"
                if len(vcstring) != 0:
                    vcstring.to_csv(outputfile, header=False, sep="\t", index=False, columns=[2,0])
                    writenumber += 1
    accfiles = [f for f in listdir("Acclist") if isfile(join("Acclist", f))]
    dumpnodes = pd.read_csv("nodes.dmp", sep="\t", usecols =[0,2,4],header=None)
    for i in accfiles:
        file = "Acclist/" + str(i)
        with open(str(file)) as accfile:
            taxstr = []
            for line in accfile:
                acc = str(line.strip().split("\t")[1])
                accline = dumpnodes.loc[dumpnodes[0] == int(acc)]
                ranks = str(accline.iloc[0][4])
                def recursnodedum (acc, accline, dumpnodes,ranks,norankcounter=0):
                    if len(accline) > 1:
                        print("Holy shite, double hits found!! Possible error!! CHECK FOLLOWING ENTRY:")
                        print(accline)
                        sys.exit(2)
                    if acc == "1":
                        tax.append(acc)
                        if ranks == "no rank":
                            norankcounter += 1
                            rank.append(ranks+ "_" + str(norankcounter))
                        else:
                            rank.append(ranks)
                    if acc != "1":
                        tax.append(acc)
                        if ranks  == "no rank" or ranks[:-2] == "no rank":
                            norankcounter +=1
                            rank.append(ranks+ "_" + str(norankcounter))
                            acc = str(accline.iloc[0][2])
                            accline = dumpnodes.loc[dumpnodes[0] == int(acc)]
                            ranks = str(accline.iloc[0][4])
                            recursnodedum(acc, accline,dumpnodes,ranks,norankcounter)
                        else:
                            rank.append(ranks)
                            acc = str(accline.iloc[0][2])
                            accline = dumpnodes.loc[dumpnodes[0] == int(acc)]
                            ranks = str(accline.iloc[0][4])
                            recursnodedum(acc, accline,dumpnodes,ranks,norankcounter)
                rank = []
                tax = []
                recursnodedum(acc, accline, dumpnodes,ranks)
                taxliststring = line.strip().split("\t")[0] + ' '.join(tax)
                taxstr.append(taxliststring)
        nameout = "Acclist/"+i.split(".")[0] + "taxstring.txt"
        text_file = open(nameout, "w")
        text_file.write('\n'.join(taxstr))
        text_file.close()
    VC_LCA = []
    for i in accfiles:
        file = "Acclist/" + str(i)
        with open(str(file)) as accfile:
            VC = str(i.split(".")[0])
            taxstr = []
            for line in accfile:
                acc = str(line.strip().split("\t")[1])
                taxstr.append(acc)
            stdn = " ".join(taxstr)
            text_file = open("tmp.txt", "w")
            text_file.write(stdn)
            text_file.close()
            ps = subprocess.Popen(('cat', 'tmp.txt'), stdout=subprocess.PIPE)
            output = subprocess.check_output(('ktGetLCA','-s'), stdin=ps.stdout).strip().decode('ASCII')
            ps.wait()
            dumpnodes = pd.read_csv("nodes.dmp", sep="\t", usecols =[0,2,4],header=None)
            accline = dumpnodes.loc[dumpnodes[0] == int(output)]
            rank = str(accline.iloc[0][4])
            dumpnames = pd.read_csv("names.dmp", sep="\t", usecols = [0,2], header=None)
            rankname = dumpnames.loc[dumpnames[0] == int(output)]
            rankname2 = str(rankname.iloc[0][2])
            finstring = "\t".join([VC, output, rank, rankname2])
            VC_LCA.append(finstring)
            print(finstring)
    if os.path.exists("VC_LCA_NOLREF.tsv"):
        os.remove("VC_LCA_NOLREF.tsv")
        print("VC_LCA_NOLREF.tsv already exists, overwriting...")
    text_file = open("VC_LCA_NOLREF.tsv", "w")
    for f in sorted(VC_LCA):
        text_file.write(f + '\n')
    text_file.close()
def dropOLNODE(inputfile):
    Allnodes = []
    with open(inputfile) as clusfile:
        for line in clusfile:
            clus = line.split(",")[7].strip()
            if clus != 'Members':
                genomelist = clus.split(' ')
                clus1 = [w.replace('"','') for w in genomelist]
                clus2 = [w.replace('~',' ') for w in clus1]
                Allnodes.extend(clus2)
    countdict = {x:Allnodes.count(x) for x in Allnodes}
    with open(inputfile) as clusfile:
        TotalVC = 0
        Survivors = 0
        if os.path.exists("NonOL_Nodes.txt"):
            os.remove("NonOL_Nodes.txt")
            print("NonOL_Nodes.txt already exists, overwriting...")
        for line in clusfile:
            clus = line.split(",")[7].strip()
            VC = 'VC' + line.split(",")[0]
            if clus != 'Members':
                TotalVC += 1
                genomelist = clus.split (' ')
                clus1 = [w.replace('"','') for w in genomelist]
                clus2 = [w.replace('~',' ') for w in clus1]
                cluscount = [ countdict.get(item,item) for item in clus2 ]
                VCdic = dict(zip(clus2,cluscount))
                for key in list(VCdic.keys()):
                    if VCdic[key] != 1:
                        del VCdic[key]
                for key in list(VCdic.keys()):
                    if '_NODE_' not in str(key):
                        del VCdic[key]
                if len(VCdic.keys()) != 0:
                    Survivors += 1
                    with open('NonOL_Nodes.txt','a') as f:
                        VC = VC + ";"
                        writestring = VC + ','.join(list(VCdic.keys()))+'\n'
                        f.write(writestring)
        print(str(Survivors) + ' NODEs of in total: '+ str(TotalVC) + ' have survived, Outfile written: NonOL_Nodes.txt')
    namedVC = {}
    with open("VC_LCA_NOLREF.tsv") as namedfil:
        for line in namedfil:
            VC = line.split("\t")[0]
            tax = line.split("\t")[3].strip()
            namedVC[VC] = tax
    Namedlist = []
    with open("NonOL_Nodes.txt") as nonOLnode:
        for line in nonOLnode:
            VC = line.split(";")[0]
            genomes = line.split(";")[1].strip().split(",")
            if VC in namedVC.keys():
                for i in genomes:
                    print(VC + ' ' + i +" : " +namedVC[VC])
                    stringname = VC + ' ' + i + " : " + namedVC[VC]
                    Namedlist.append(stringname)
    if os.path.exists('Namednodes.txt'):
        os.remove('Namednodes.txt')
        print("Namednodes already exists, overwriting...")
    text_file = open('Namednodes.txt', "w")
    text_file.write('\n'.join(Namedlist))
    text_file.close() 
def Nodeclassifier(inputfile):
    Allnodes = []
    with open(inputfile) as clusfile:
        for line in clusfile:
            clus = line.split(",")[7].strip()
            if clus != 'Members':
                genomelist = clus.split(' ')
                clus1 = [w.replace('"','') for w in genomelist]
                clus2 = [w.replace('~','') for w in clus1]
                Allnodes.extend(clus2)
    countdict = {x:Allnodes.count(x) for x in Allnodes}
    noNODE_OL = []
    noNODE_NOL = []
    allNODE_OL = []
    allNODE_NOL = []
    someNODE_OL = []
    someNODE_NOL = []
    with open(inputfile) as clusfile:
        for line in clusfile:
            VC = 'VC' + line.split(",")[0]
            clus = line.split(",")[7].strip()
            if clus != 'Members':
                genomelist = clus.split(' ')
                clus1 = [w.replace('"','') for w in genomelist]
                clus2 = [w.replace('~','') for w in clus1]
                cluscount = [ countdict.get(item,item) for item in clus2 ]
                Nodenum = sum('_NODE_' in s for s in clus2)
                VCdic = dict(zip(clus2,cluscount))
                if Nodenum == len(clus2):
                    if sum(cluscount)/len(clus2) == 1:
                        allNODE_NOL.append(VC)
                    if sum(cluscount)/len(clus2) != 1:
                        allNODE_OL.append(VC)
                if Nodenum == 0:
                    if sum(cluscount)/len(clus2) == 1:
                        noNODE_NOL.append(VC)
                    if sum(cluscount)/len(clus2) != 1:
                        noNODE_OL.append(VC)
                if Nodenum != 0 and Nodenum != len(clus2):
                    if sum(cluscount)/len(clus2) == 1:
                        someNODE_NOL.append(VC)
                    if sum(cluscount)/len(clus2) != 1:
                        someNODE_OL.append(VC)
        print('noNODE_OL: '+ '\t' +' '.join(noNODE_OL))
        print('noNODE_NOL: '+ '\t' +' '.join(noNODE_NOL))
        print('someNODE_OL: '+ '\t' +' '.join(someNODE_OL))
        print('someNODE_NOL: '+ '\t' +' '.join(someNODE_NOL))
        print('allNODE_OL: '+ '\t' +' '.join(allNODE_OL))
        print('allNODE_NOL: '+ '\t' +' '.join(allNODE_NOL))
    Namedlist = []
    with open("NonOL_Nodes.txt") as nonOLnode:
        for line in nonOLnode:
            genomes = line.split(";")[1].strip().split(",")
            Namedlist.extend(genomes)
    with open(inputfile) as clusfile:
        clusdic = {}
        if os.path.exists("NonnamedNODES.txt"):
            os.remove("NonnamedNODES.txt")
            print("NonnamedNODES already exists, overwriting...")
        for line in clusfile:
           VC = 'VC' + line.split(",")[0]
           clus = line.split(",")[7].strip()
           if clus != 'Members':
               genomelist = clus.split(' ')
               clus1 = [w.replace('"','') for w in genomelist]
               clus2 = [w.replace('~','') for w in clus1]
               for i in clus2:
                   if '_NODE_' in i:
                       if i not in Namedlist:
                           if VC in noNODE_OL:
                               VCtype = "noNODE_OL"
                           if VC in noNODE_NOL:
                               VCtype = "noNODE_NOL"
                           if VC in someNODE_OL:
                               VCtype = "someNODE_OL"
                           if VC in someNODE_NOL:
                               VCtype = "someNODE_NOL"
                           if VC in allNODE_OL:
                               VCtype = "allNODE_OL"
                           if VC in allNODE_NOL:
                               VCtype = "allNODE_NOL"
                           if i in clusdic:
                               clusdic[i].append(VC + ' ' + VCtype)
                           else:
                               clusdic[i] = [VC + ' ' + VCtype]
        for i in clusdic.keys():
           with open("NonnamedNODES.txt", 'a') as f:
               f.write(i + ' ' + ','.join(clusdic[i]) + '\n')
def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts,args = getopt.getopt(argv,"hi:o:", ["ifile=","ofile="])
    except getopt.GetoptError:
        print('I need an inputfile (-i) (vcontact2, clusterfile), and outputname (-o).')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('I need an inputfile (-i) (vcontact2, clusterfile), and outputname (-o).')
            sys.exit(2)
        if opt == '-i':
            inputfile = arg
        if opt == '-o':
            outputfile = arg
        if opt == '-n':
            n = arg
    if inputfile == '':
        print('I need an inputfile')
        sys.exit(2)
    if outputfile == '':
        print('I need an outputfile')
        sys.exit(2)
    Clusstats(inputfile)
    dropOLREF(inputfile)
    getLCA()
    dropOLNODE(inputfile)
    Nodeclassifier(inputfile)
if __name__ == "__main__":
    main(sys.argv[1:])
