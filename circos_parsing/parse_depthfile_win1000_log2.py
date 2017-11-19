#python3
from math import log2
num_lines = sum(1 for line in open("fulldepth.depth"))
with open("fulldepth.depth") as f:
    tempnumbers = []
    count = 0
    fullnode = ""
    keeper = 0
    fullcounty = 0
    for line in f:
        fullcounty +=1
        count +=1
        if count == 1:
            fullnode = line.split("\t")[0]
            node = str(fullnode.split(sep="_")[0] + fullnode.split(sep="_")[1] + '_' + fullnode.split(sep="_")[8])
            check = line.split("\t")[2]
            tempnumbers.append(int(check))
            #print(tempnumbers)
        if fullnode == line.split ("\t")[0]:
            if (count < 1000 and count != 1):
                check = line.split("\t")[2]
                tempnumbers.append(int(check))
            if count == 1000:
                check = line.split("\t")[2]
                tempnumbers.append(int(check))
                avg = round(sum(tempnumbers)/len(tempnumbers),2)
                start = (int(keeper)*1000)+1
                stop = (int(keeper)*1000)+1000
                print(str(node) + ' ' + str(start) + ' ' + str(stop)+ ' ' +str(round(log2(avg),2)))
                keeper += 1
                count = 0
        if fullnode != line.split("\t")[0]:
            avg = round(sum(tempnumbers)/len(tempnumbers),2)
            start = (int(keeper)*1000)+1
            stop = (int(keeper)*1000)
            stopreal = stop + int(count)
            if start == stop:
                print("Shit man one contig is x+1 big :'(, can't deal")
                break
            print(str(node) + ' ' + str(start) + ' ' + str(stopreal)+ ' ' +str(round(log2(avg),2)))
            keeper = 0
            count = 0
        if fullcounty == num_lines:
            check = line.split("\t")[2]
            tempnumbers.append(int(check))
            avg = round(sum(tempnumbers)/len(tempnumbers),2)
            start = (int(keeper)*1000)+1
            stop = (int(keeper)*1000)
            count +=1
            stopreal = stop + int(count)
            if start == stop:
                print("Shit man one contig is x+1 big :'(, can't deal")
                break
            print(str(node) + ' ' + str(start) + ' ' + str(stopreal)+ ' ' +str(round(log2(avg),2))) 
