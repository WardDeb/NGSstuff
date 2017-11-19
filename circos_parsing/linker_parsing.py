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
        print(countup)
        #df[row,col] = countup
        df.at[row,col] = countup
    print(df)
    df.to_csv("DFtest.tsv", sep='\t')

