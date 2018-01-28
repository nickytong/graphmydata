
library(randomizeR)
library(SRS)
########################################################################
### Name: Complete randomization
### Purpose: 
### Argument :
# N: number of total sample size  
# K: number of treatment arm
# ratio: vector of size K. It is the ratio of patient allocation to each treatment arm
# seed: random seed. The default is seed to be 1.
### Value
# A list containing the following components:
# allocation: a vection for allocation
# summary: summary of allocation
######################################################################
CompleteRandomization<-function(N=N,K=K,Alloratio=Alloratio,seed=1){
  ###Complete randomization
  allocation=genSeq(crPar(N, K = K, ratio =Alloratio, groups = LETTERS[1:K]),seed=seed)@M
  return(list(allocation=allocation,summary=table(allocation)))
}

########################################################################
### Name: Block randomization
### Purpose: 
### Argument :
# N: number of total sample size  
# K: number of treatment arm
# ratio: vector of size K. It is the ratio of patient allocation to each treatment arm
# seed: random seed. The default is seed to be 1.
# blocksize: vector. If length is 1, the block size is fixed. If length>1, it is random block size.
### Value
# A list containing the following components:
# allocation: a vection for allocation
# summary: summary of allocation
######################################################################
BlockRandomization<-function(N=N,K=K,Alloratio=Alloratio,blocksize=blocksize,seed=1){
  if(length(blocksize)==1) {
    bc=rep(blocksize,N/blocksize)
  } else{
    maxblocknum=N/min(blocksize)
    blocksizeselect=sample(blocksize,maxblocknum,replace=TRUE)
    cumseq=cumsum(blocksizeselect)
    cumseq=ifelse(cumseq<N,-Inf,cumseq)
    numblock=which.min(abs(cumseq-N))
    bc=blocksizeselect[1:numblock]
  }
  allocation=genSeq(pbrPar(bc, K = K, ratio = Alloratio, groups = LETTERS[1:K]),seed=seed)@M
  allocation=allocation[1:N]
  return(list(allocation=allocation,summary=table(allocation)))
}


########################################################################
### Name: Stratified complete randomization
### Purpose: 
### Argument :
# N: vector, number of total sample size for each strata  
# K: number of treatment arm
# ratio: vector of size K. It is the ratio of patient allocation to each treatment arm
# seed: random seed. The default is seed to be 1.
# blocksize: vector. If length is 1, the block size is fixed. If length>1, it is random block size.
### Value
# A list containing the following components:
# allocation: a vection for allocation
# summary: summary of allocation
######################################################################
StratifiedCompleteRandomization<-function(N=N,K=K,Alloratio=Alloratio,seed=seed){
  numstrata=length(N)
  allocation=NULL
  for(i in 1:numstrata) 
    allocation=rbind(allocation,cbind(rep(i,N[i]),as.vector(CompleteRandomization(N=N[i],K=K,Alloratio=Alloratio,seed=seed+i)$allocation)))
  allocation=as.data.frame(allocation)
  colnames(allocation)=c("strata","allocation")
  return(list(allocation=allocation,summary=table(allocation$strata,allocation$allocation)))
}


########################################################################
### Name: Stratified block randomization
### Purpose: 
### Argument :
# N: vector, number of total sample size for each strata  
# K: number of treatment arm
# ratio: vector of size K. It is the ratio of patient allocation to each treatment arm
# seed: random seed. The default is seed to be 1.
# blocksize: vector. If length is 1, the block size is fixed. If length>1, it is random block size.
### Value
# A list containing the following components:
# allocation: a vection for allocation
# summary: summary of allocation
######################################################################
StratifiedBlockRandomization<-function(N=N,K=K,Alloratio=Alloratio,blocksize=blocksize,seed=seed){
  numstrata=length(N)
  allocation=NULL
  for(i in 1:numstrata) 
    allocation=rbind(allocation,cbind(rep(i,N[i]),as.vector(BlockRandomization(N=N[i],K=K,blocksize=blocksize,Alloratio=Alloratio,seed=seed+i)$allocation)))
  allocation=as.data.frame(allocation)
  colnames(allocation)=c("strata","allocation")
  return(list(allocation=allocation,summary=table(allocation$strata,allocation$allocation)))
}

  
########################################################################
### Name:  minimization randomization
### Purpose: 
### Argument :
# K: number of treatment arm
# nfactor: number of factors for randomization
# nlevel: vector of length nfactor. it is the number of levels corresponding to each factor
# ratio: vector of size K. It is the ratio of patient allocation to each treatment arm
# seed: random seed. The default is seed to be 1.
# olddf: dataframe. The old randomization information. the first nfactor column are the factors. 
#        the last column is the allocation
# newdf:  dataframe. The new randomization information. the first nfactor column are the factors. 
#        the last column is the allocation(set to be NA)
### Value
# A list containing the following components:
# allocation: a matrix for allocation
# summary: summary of allocation
######################################################################
MinimizationRandomization<-function(K=K,nfactor=nfactor,nlevel=nlevel,Alloratio=Alloratio,seed=seed,olddf=NULL,newdf=newdf){
##
  expt0 <- ClinicalExperiment(number.of.factors = nfactor,
                              number.of.factor.levels = nlevel,
                              number.of.treatments = K)
  r.obj <- new("PocockSimonRandomizer", expt0, as.integer(seed),tr.ratios=Alloratio)
  if(!is.null(olddf)) r.obj@tr.assignments=olddf
  r.obj@tr.assignments$Treatment=lapply(r.obj@tr.assignments$Treatment,function(input) paste("Tr",input,sep=""))
  #########################################################
  ### Generate a random Id for a subject (max 10000000)!
  #########################################################
  generateId <- function(oldf,i) {
    if(is.null(olddf)) return(paste(i,sep="")) else return(paste(i+nrow(olddf),sep=""))
  }
  
  ###########################################################################
  ###  ; if n is the number of factors, limits is a list
  ### of length n with each element being a vector of possible factor levels
  ###########################################################################
  ConvertFactors <- function(newdf) {
    as.character((newdf[,1:nfactor]))
  }
  r.objnew=r.obj
  for(i in 1:nrow(newdf))
    r.objnew <- randomize(r.objnew, generateId(olddf,i),ConvertFactors(newdf[i,]))
  r.objnew@tr.assignments$Treatment=lapply(r.objnew@tr.assignments$Treatment,function(input) as.numeric(unlist(strsplit(input,"Tr"))[2]))
  list(allocation=r.objnew@tr.assignments,summary=r.objnew@stateTable)
}