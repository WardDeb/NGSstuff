#python3
import pandas as pd
with open("hitnames.txt") as f:
    rows = []
    cols = []
    for line in f:
        row = line.split(" ")[0]
        col = line.split(" ")[1]
        rows.append(row)
        cols.append(col)
    rows = list(set(rows))
    cols = list(set(rows))
    df = pd.DataFrame(0,rows,columns=cols)
with open("hitnames.txt") as f:
    for line in f:
        row = line.split(" ")[0]
        col = line.split(" ")[1]
        countup = int(df.loc[row,col])
        countup += 1
        df.at[row,col] = countup
    df.to_csv("DFtest.tsv", sep='\t')
with open("hitnames.txt") as f:
    leeg = []
    for line in f:
        row = line.split(" ")[0]
        col = line.split(" ")[1]
        haha = row + ' ' + col + ' ' + str(df.loc[row,col])
        leeg.append(haha)
    leeg = list(set(leeg))
    for i in leeg:
        print(i)
        
