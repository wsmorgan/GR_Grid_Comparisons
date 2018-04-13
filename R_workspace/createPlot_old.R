aflow <- read.delim("Aflow_metals_irreducible_kpd.csv",header=F,sep="\t")
froy <- read.delim("Froyen_metals_irreducible_kpd.csv",header=F,sep="\t")
muel <- read.delim("Mueller_metals_irreducible_kpd.csv",header=F,sep="\t")
library("scales")
mycol=c("green","red","blue")

pdf("ErrorComparison.pdf",height=5,width=7)
x<-aflow
plot(x[,1],x[,2],col=alpha(mycol[1],0.2),xlab="Number of Irreducible K Points",ylab="Error",log="xy")

ff1<-loess.smooth(x[,1],x[,2],span=0.5,evaluation=200)
lines(ff1$x,ff1$y,col=mycol[1],lwd=4)
x<-froy
x<-log10(x)
points(x[,1],x[,2],col=alpha(mycol[2],0.2))
ff2<-loess.smooth(x[,1],x[,2],span=0.5,evaluation=200)
lines(ff2$x,ff2$y,col=mycol[2],lwd=4)
x<-muel
x<-log10(x)
points(x[,1],x[,2],col=alpha(mycol[3],0.2))
ff3<-loess.smooth(x[,1],x[,2],span=0.5,evaluation=200)
lines(ff3$x,ff3$y,col=mycol[3],lwd=4)
lines(ff1$x,ff1$y,col=mycol[1],lwd=4)
lines(ff2$x,ff2$y,col=mycol[2],lwd=4)

legend(2000,1e-02,c("Aflow","Froyen","Mueller"),lwd=4,col=mycol)
dev.off()
