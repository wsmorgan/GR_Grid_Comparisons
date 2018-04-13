aflow <- read.delim("../data/R_workspace/MP_irkpd.csv",header=F,sep="\t")
froy <- read.delim("../data/R_workspace/SC_irkpd.csv",header=F,sep="\t")
muel <- read.delim("../data/R_workspace/GR_irkpd.csv",header=F,sep="\t")
library("scales")
mycol=c("green","red","blue")
opa.a <- 0.2
span.sm <- 0.5

x<-aflow
x<-log10(x)
ff1<-loess.smooth(x[,1],x[,2],span=span.sm,evaluation=200)

x<-froy
x<-log10(x)
ff2<-loess.smooth(x[,1],x[,2],span=span.sm,evaluation=200)

x<-muel
x<-log10(x)
ff3<-loess.smooth(x[,1],x[,2],span=span.sm,evaluation=200)

write.csv(ff1,file="../data/R_workspace/MP_irkpd_loess.csv",row.names=FALSE)
write.csv(ff2,file="../data/R_workspace/SC_irkpd_loess.csv",row.names=FALSE)
write.csv(ff3,file="../data/R_workspace/GR_irkpd_loess.csv",row.names=FALSE)