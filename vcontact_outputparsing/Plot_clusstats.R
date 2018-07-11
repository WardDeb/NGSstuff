#Vcontact cluster statistics
#Output generated from clusterstats.py
setwd("~/Bioinf/repo/bash_ngs/vcontact_outputparsing/refonly_eni/Clusstats")
allnode_NOL <- read.csv("~/Bioinf/repo/bash_ngs/vcontact_outputparsing/refonly_eni/Clusstats/allNODE_NOL.txt", sep="")
allnode_OL <- read.csv("~/Bioinf/repo/bash_ngs/vcontact_outputparsing/refonly_eni/Clusstats/allNODE_OL.txt", sep="")
somenode_NOL <- read.csv("~/Bioinf/repo/bash_ngs/vcontact_outputparsing/refonly_eni/Clusstats/someNODE_NOL.txt", sep="")
somenode_OL <- read.csv("~/Bioinf/repo/bash_ngs/vcontact_outputparsing/refonly_eni/Clusstats/someNODE_OL.txt", sep="")
nonode_NOL <- read.csv("~/Bioinf/repo/bash_ngs/vcontact_outputparsing/refonly_eni/Clusstats/noNODE_NOL.txt", sep="")
nonode_OL <- read.csv("~/Bioinf/repo/bash_ngs/vcontact_outputparsing/refonly_eni/Clusstats/noNODE_OL.txt", sep="")


#Plots
library(ggplot2)
pdf("Clusstats.pdf")

x <- c("allnode_NOL","allnode_OL","nonode_NOL","nonode_OL","somenode_NOL","somenode_OL")
y <- c(nrow(allnode_NOL),nrow(allnode_OL),nrow(nonode_NOL),nrow(nonode_OL),nrow(somenode_NOL),nrow(somenode_OL))
y <- as.numeric(paste(y))
statdf <- as.data.frame(cbind(x,y))
ggplot()+
  geom_point(aes(x=statdf$x,y=as.numeric(paste(statdf$y)))) +
  xlab("") + ylab("Number of clusters") + 
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) + 
  ggtitle("Number of clusters per category")
#Allnodes
allnode_NOL$VC. <- factor(allnode_NOL$VC., levels = allnode_NOL$VC.[order(allnode_NOL$X.NODEs)])
ggplot() + 
  geom_point(aes(x=allnode_NOL$VC., y=allnode_NOL$X.NODEs)) + 
  xlab("") + ylab("Number of Nodes")  + 
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) + 
  ggtitle("Allnodes, Non overlapping")

allnode_OL$VC. <- factor(allnode_OL$VC., levels = allnode_OL$VC.[order(allnode_OL$X.NODEs)])
ggplot() + 
  geom_point(size=1,aes(x=allnode_OL$VC., y=allnode_OL$X.NODEs)) + 
  geom_point(size=1,col = "red", aes(x=allnode_OL$VC., y=allnode_OL$X.OLNODE*100)) +
  xlab("") + ylab("Number of Nodes/ % of overlapping nodes")  + 
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) + 
  ggtitle("Allnodes, overlapping")
#No nodes
nonode_NOL$VC. <- factor(nonode_NOL$VC., levels = nonode_NOL$VC.[order(nonode_NOL$X.REFs)])
ggplot() + 
  geom_point(aes(x=nonode_NOL$VC., y=nonode_NOL$X.REFs)) + 
  xlab("") + ylab("Number of References")  + 
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) + 
  ggtitle("No nodes, Non overlapping")

nonode_OL$VC. <- factor(nonode_OL$VC., levels = nonode_OL$VC.[order(nonode_OL$X.REFs)])
ggplot() + 
  geom_point(size=1,aes(x=nonode_OL$VC., y=nonode_OL$X.REFs)) + 
  geom_point(size=1,col = "red", aes(x=nonode_OL$VC., y=nonode_OL$X.OLREF*100)) +
  xlab("") + ylab("Number of References/ % of overlapping References")  + 
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) + 
  ggtitle("No nodes, overlapping")

somenode_NOL$VC. <- factor(somenode_NOL$VC., levels=somenode_NOL$VC.[order(somenode_NOL$Clustersize)])
ggplot() + 
  geom_point(size=1,aes(x=somenode_NOL$VC., y=somenode_NOL$Clustersize)) + 
  geom_point(alpha = 0.5, size=1, col="red", aes(x=somenode_NOL$VC., y=somenode_NOL$X.NODE)) + 
  geom_point(alpha = 0.5, size=1, col="green", aes(x=somenode_NOL$VC., y=somenode_NOL$X.REF)) + 
  xlab("") + ylab("Clustersize, red=NODE, green=REF")  + 
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) + 
  ggtitle("some nodes, Non overlapping")

somenode_OL$VC. <- factor(somenode_OL$VC., levels=somenode_OL$VC.[order(somenode_OL$Clustersize)])
ggplot() + 
  geom_point(size=1,aes(x=somenode_OL$VC., y=somenode_OL$Clustersize)) + 
  geom_point(alpha = 0.5, size=1, col="red", aes(x=somenode_OL$VC., y=somenode_OL$X.NODE)) + 
  geom_point(alpha = 0.5, size=1, col="green", aes(x=somenode_OL$VC., y=somenode_OL$X.REF)) + 
  #geom_point(size=1,col = "blue", aes(x=somenode_OL$VC., y=somenode_OL$X.OLNODE*100)) +
  #geom_point(size=1,col = "brown", aes(x=somenode_OL$VC., y=somenode_OL$X.OLREF*100)) +
  xlab("") + ylab("Clustersize, red=NODE, green=REF")  + 
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) + 
  ggtitle("some nodes, overlapping")

ggplot() + 
  geom_point(size=1,aes(x=somenode_OL$VC., y=somenode_OL$Clustersize)) + 
  #geom_point(alpha = 0.5, size=1, col="red", aes(x=somenode_OL$VC., y=somenode_OL$X.NODE)) + 
  #geom_point(alpha = 0.5, size=1, col="green", aes(x=somenode_OL$VC., y=somenode_OL$X.REF)) + 
  geom_point(size=1,col = "red", aes(x=somenode_OL$VC., y=somenode_OL$X.OLNODE*100)) +
  geom_point(size=1,col = "green", aes(x=somenode_OL$VC., y=somenode_OL$X.OLREF*100)) +
  xlab("") + ylab("Clustersize, red=%OL NODE, green=% OL REF")  + 
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) + 
  ggtitle("some nodes, overlapping")

dev.off()
