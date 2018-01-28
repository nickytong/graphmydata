



CompleteRandomization(N=60,K=3,Alloratio=c(1,1,1),seed=3)
CompleteRandomization(N=1000,K=3,Alloratio=c(1,2,1),seed=3)
CompleteRandomization(N=60,K=2,Alloratio=c(1,2),seed=4)


# how to check blocksieze 5 failure; blocksize being a tuple?
BlockRandomization(N=60,K=2,Alloratio=c(1,2),blocksize=6,seed=2)
BlockRandomization(N=60,K=3,Alloratio=c(1,1,1),blocksize=5,seed=2)
BlockRandomization(N=60,K=3,Alloratio=c(3,2,1),blocksize=6,seed=3)
BlockRandomization(N=60,K=2,Alloratio=c(1,1),blocksize=c(2,4),seed=4)
BlockRandomization(N=50,K=2,Alloratio=c(1,1),blocksize=c(2,4),seed=4)

StratifiedCompleteRandomization(N=c(30,30,30),K=3,Alloratio=c(1,1,1),seed=1)
StratifiedCompleteRandomization(N=c(20,30,20),K=3,Alloratio=c(1,1,1),seed=1)
StratifiedCompleteRandomization(N=c(60,30,120),K=3,Alloratio=c(1,2,1),seed=1)



result1 = CompleteRandomization(N=60,K=2,Alloratio=c(1,1),seed=4)
result2 = BlockRandomization(N=60,K=2,Alloratio=c(1,1),blocksize=2,seed=2)
result3 = StratifiedCompleteRandomization(N=c(20,30,20),K=2,Alloratio=c(1,1),seed=1)
result4 = StratifiedBlockRandomization(N=c(20,30,20),K=2,Alloratio=c(1,1),blocksize=2,seed=4)
StratifiedBlockRandomization(N=c(30,30,60),K=2,Alloratio=c(1,2),blocksize=6,seed=2)
StratifiedBlockRandomization(N=c(30,30,60),K=3,Alloratio=c(1,2,3),blocksize=6,seed=2)
StratifiedBlockRandomization(N=c(40,30,60),K=3,Alloratio=c(1,2,3),blocksize=6,seed=2)
StratifiedBlockRandomization(N=c(40,30,60),K=3,Alloratio=c(1,2,3),blocksize=6,seed=2)

nlevel=c(2,2,3)
F1=c(1, 2);F2=c(2, 1);F3=c(2, 3);group=c('', '')
patientID=letters[1:2]
newdf=data.frame(patientID,F1,F2,F3,group)
old1=MinimizationRandomization(K=3,nfactor=3,nlevel=c(2,2,3),Alloratio=c(1,2,1),seed=1,newdf=newdf,weight=c(1,1,1))
old1

# load json data
library(jsonlite)
x = read_json(file.path('jsonExamples', 'autosequentialout_8.json.output'), simplifyVector=TRUE)
markerNew = data.frame(x[1:4])
markerNew$group <- rep(NA, nrow(markerNew))
old1=MinimizationRandomization(K=2,nfactor=2,nlevel=c(2,2),Alloratio=c(1,1),seed=1,newdf=markerNew,weight=c(1,1))
old1
###
### Do NOT modify here: to be compared with Python result
###
nlevel=c(2,2,3)
F1=c(1, 2);F2=c(2, 1);F3=c(2, 3);group=c('', '')
patientID=letters[1:2]
newdf=data.frame(patientID,F1,F2,F3,group)
old1=MinimizationRandomization(K=3,nfactor=3,nlevel=c(2,2,3),Alloratio=c(1,2,1),seed=1,newdf=newdf,weight=c(1,1,1))
old1

F1=c(1,1);F2=c(2,1);F3=c(1,1);group=c(NA,NA)
patientID=c(3:4)
newdf=data.frame(patientID,F1,F2,F3,group)
old2=MinimizationRandomization(K=3,nfactor=3,nlevel=c(2,2,3),Alloratio=c(1,2,1),
                               seed=1,olddf=old1$assign,newdf=newdf,weight=c(1,1,1))

#### testing with weight
nlevel=c(2,2,3)
F1=c(1, 2);F2=c(2, 1);F3=c(2, 3);group=c('', '')
patientID=letters[1:2]
newdf=data.frame(patientID,F1,F2,F3,group)
old1=MinimizationRandomization(K=3,nfactor=3,nlevel=c(2,2,3),Alloratio=c(1,2,1),seed=1,newdf=newdf,weight=c(2,1,3))
old1

F1=c(1,1);F2=c(2,1);F3=c(1,1);group=c(NA,NA)
patientID=c(3:4)
newdf=data.frame(patientID,F1,F2,F3,group)
old2=MinimizationRandomization(K=3,nfactor=3,nlevel=c(2,2,3),Alloratio=c(1,2,1),
                               seed=1,olddf=old1$assign,newdf=newdf,weight=c(2,1,3))

###


### length(Alloratio) ==> K
### length(nlevel) ==> nfactor 
### works for capitalized feature name
nlevel=c(2,2,3)
F1=c(1);F2=c(2);F3=c(2);group=c('')
patientID=letters[1]
newdf=data.frame(patientID,F1,F2,F3,group)
old1=MinimizationRandomization(K=3,nfactor=3,nlevel=c(2,2,3),Alloratio=c(1,2,1),seed=1,newdf=newdf,weight=c(1,1,1))
old1

F1=c(2,1,1);F2=c(1,2,1);F3=c(3,1,1);group=c(NA,NA,NA)
patientID=c("b",3:4)
newdf=data.frame(patientID,F1,F2,F3,group)
old2=MinimizationRandomization(K=3,nfactor=3,nlevel=c(2,2,3),Alloratio=c(1,2,1),
                               seed=1,olddf=old1$assign,newdf=newdf,weight=c(1,1,1))
###
### fails for lowercase feature name
###
nlevel=c(2,2,3)
f1=c(1);f2=c(2);f3=c(2);group=c(NA)
patientID=letters[1]
newdf=data.frame(patientID,f_1=f1, f_2=f2,f_3=f3,group)
colnames(newdf) <- c("patientID", "f1", "f2", "f3", "group")

old1=MinimizationRandomization(K=3,nfactor=3,nlevel=c(2,2,3),Alloratio=c(1,2,1),seed=1,newdf=newdf,weight=c(1,1,1))
old1

f1=c(1,1);f2=c(2,1);f3=c(1,1);group=c(NA,NA)
patientID=3:4
newdf=data.frame(patientID,f1, f2,f3,group)
olddf <- old1$assign
#colnames(olddf) <- c("patientID", "F1", "F2", "F3", "group")
colnames(olddf) <- colnames(newdf) <- c("patientID", "f1", "f2", "f3", "group")
old2=MinimizationRandomization(K=3,nfactor=3,nlevel=c(2,2,3),Alloratio=c(1,2,1),
                               seed=1,olddf=olddf, newdf=newdf,weight=c(1,1,1))

#####################Not run
Neach=1000
F1=sample(1:2,Neach,replace=TRUE)
F2=sample(1:2,Neach,replace=TRUE)
F3=sample(1:3,Neach,replace=TRUE)
group=rep(NA,Neach)
patientID=1:Neach
newdf=data.frame(patientID,F1,F2,F3,group)
colnames(newdf) <- c("patientID", "f1", "f2", "f3", "group")
old3=MinimizationRandomization(K=2,nfactor=3,nlevel=c(2,2,3),Alloratio=c(1,1),
                               seed=1,olddf=old2$assign,newdf=newdf,weight=c(1,1,1))
old3$summary


Neach=100
F1=sample(1:2,Neach,replace=TRUE)
F2=sample(1:2,Neach,replace=TRUE)
F3=sample(1:3,Neach,replace=TRUE)
group=rep(NA,Neach)
patientID=1:Neach
newdf=data.frame(patientID,F1,F2,F3,group)
colnames(newdf) <- c("patientID", "f1", "f2", "f3", "group")
old4=MinimizationRandomization(K=2,nfactor=3,nlevel=c(2,2,3),Alloratio=c(1,1),
                               seed=1,olddf=old2$assign,newdf=newdf,weight=c(1,1,1))
old4$summary

Neach=100
F1=sample(1:2,Neach,replace=TRUE)
F2=sample(1:2,Neach,replace=TRUE)
F3=sample(1:3,Neach,replace=TRUE)
group=rep(NA,Neach)
patientID=1:Neach
newdf=data.frame(patientID,F1,F2,F3,group)
colnames(newdf) <- c("patientID", "f1", "f2", "f3", "group")
old5=MinimizationRandomization(K=2,nfactor=3,nlevel=c(2,2,3),Alloratio=c(1,1),
                               seed=1,olddf=old2$assign,newdf=newdf,weight=c(5,1,1))
old5$summary