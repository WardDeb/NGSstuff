#python3
num_lines = sum(1 for line in open("BP1.Depth"))
with open("BP1.depth") as f:
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
            if (count < 500 and count != 1):
                check = line.split("\t")[2]
                tempnumbers.append(int(check))
            if count == 500:
                check = line.split("\t")[2]
                tempnumbers.append(int(check))
                avg = round(sum(tempnumbers)/len(tempnumbers),2)
                start = (int(keeper)*500)+1
                stop = (int(keeper)*500)+500
                print(str(node) + ' ' + str(start) + ' ' + str(stop)+ ' ' +str(avg))
                keeper += 1
                count = 0
        if fullnode != line.split("\t")[0]:
            avg = round(sum(tempnumbers)/len(tempnumbers),2)
            start = (int(keeper)*500)+1
            stop = (int(keeper)*500)
            stopreal = stop + int(count)
            if start == stop:
                print("Shit man one contig is x+1 big :'(, can't deal")
                break
            print(str(node) + ' ' + str(start) + ' ' + str(stopreal)+ ' ' +str(avg))
            keeper = 0
            count = 0
        if fullcounty == num_lines:
            check = line.split("\t")[2]
            tempnumbers.append(int(check))
            avg = round(sum(tempnumbers)/len(tempnumbers),2)
            start = (int(keeper)*500)+1
            stop = (int(keeper)*500)
            count +=1
            stopreal = stop + int(count)
            if start == stop:
                print("Shit man one contig is x+1 big :'(, can't deal")
                break
            print(str(node) + ' ' + str(start) + ' ' + str(stopreal)+ ' ' +str(avg)) 
