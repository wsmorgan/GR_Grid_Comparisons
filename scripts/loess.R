aflow <- read.delim("../data/R_workspace/Aflow_metals_kpd.csv",header=F,sep="\t")
froy <- read.delim("../data/R_workspace/Froyen_metals_kpd.csv",header=F,sep="\t")
muel <- read.delim("../data/R_workspace/Mueller_metals_kpd.csv",header=F,sep="\t")
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

write.csv(ff1,file="../data/R_workspace/Aflow_kpd_loess.csv",row.names=FALSE)
write.csv(ff2,file="../data/R_workspace/Froyen_kpd_loess.csv",row.names=FALSE)
write.csv(ff3,file="../data/R_workspace/Muel_kpd_loess.csv",row.names=FALSE)