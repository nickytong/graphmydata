# echo "deb http://cran.stat.ucla.edu/bin/linux/ubuntu xenial/" | sudo tee /etc/apt/sources.list.d/Rcurrent.list
# 

library(randomizeR)
library(SRS) # install.packages("SRS", repos="http://R-Forge.R-project.org")
library(foreach)
library(stringr)
options(stringsAsFactors=FALSE)

# make sure summary is returned as data frame, not table, for same Python parsing
table2df <- function(tab){
  #browser()
  if(length(dim(tab))==1){
    # not conditional table
    result <- data.frame(t(as.vector(tab)))
    colnames(result) <- names(tab)
  } else {
    # conditional table
    result <- as.data.frame.matrix(tab)
  }
  #result
  data.matrix(result) # AttrArray will presume both rowname and colname
}

## define utility functions to convert python passed data to R.
# olddf '' ==> NULL; named list (taggedList in python) to data frame
empty2na <- function(x){
  x[x==''] <- NA
  x
}
length2 <- function(x) length(as.vector(x))
empty2null <- function(x){
  if(length2(x)==1){
    if(x=='') x <- NULL
  } 
  x
}
list2df <- function(dat){
  if(is.list(dat) & !is.data.frame(dat)){
    dat <- data.frame(dat)
  }
  if(length(as.vector(dat))==1)
    return(dat)
  dat
}
# for result to matrix so that rowname/colname are preserved ===> AttrArray in python
df_force_mode <- function(df, modefunc, forcedf=FALSE){
  df <- data.frame(df)
  #res <- sapply(df, modefunc) # not consistent for 1 row df
  res <- foreach(col=1:ncol(df), .combine='cbind') %do% {
    modefunc(df[, col])
  }
  rownames(res) <- rownames(df)
  colnames(res) <- colnames(df)
  if(forcedf){
    res <- data.frame(res) # to tagged list/Py
  } else {
    res <- data.matrix(res) # to AttrArray/Py
  } 
  res
}


MinimizationSummary<-function(df,nlevel,K){
  nfactor=length(nlevel)
  summarytable=matrix(0,sum(nlevel),K)
  colnames(summarytable)=paste("group-",1:K,sep="")
  rownames(summarytable)=unlist(lapply(1:nfactor,function(j) paste("F",j,".",1:nlevel[j],sep="")))
  firstrow=1
  for(j in 1:nfactor){
    temp=table(df[,j+1],df[,nfactor+2])
    for(p in colnames(temp))
      for(q in rownames(temp) )
        summarytable[paste("F",j,".",q,sep=""),paste("group-",p,sep="")]=temp[q,p]
  }
  summarytable
}
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
# assign: a data frame for allocation.The column patientID is the patient sequence number.
#          The column group is the group that the patient is allocated to. 
# summary: summary of allocation
#### Note
#  If the N%%K is not 0, return 1000
######################################################################
CompleteRandomization<-function(N,K,Alloratio,seed=1){
  ###Complete randomization
  Alloratio=as.numeric(Alloratio)
  ##Input Error check####
  if(N%%K!=0) stop(sprintf('N (%d) must be a multiple of K (%d)!', N, K))
  if(N%%sum(Alloratio)!=0) stop(sprintf('N (%d) must be a multiple of sum of Alloratio  (%d)!', N, sum(Alloratio)))
  if(length(Alloratio)!=K) stop(sprintf("The length of Alloratio (%d)  must match K (%d)!",length(Alloratio),K))
  allocation=genSeq(crPar(N, K = K, ratio =Alloratio, groups = LETTERS[1:K]),seed=seed)@M+1
  ###return
  patientID=1:N
  assign=data.frame(patientID,allocation[1,])
  colnames(assign)=c("patientID","group")
  summarytable=table(assign$group)
  names(summarytable)=paste("group-",1:K,sep="")  
  smry <- df_force_mode(table2df(summarytable), as.integer)
  rownames(smry) <- ''
  #browser()
  return(list(assign=df_force_mode(data.frame(assign), as.character, forcedf=TRUE),summary=smry))
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
# assign: a data frame for allocation.The column patientID is the patient sequence number.
#          The column group is the group that the patient is allocated to. 
# summary: summary of allocation
######################################################################
BlockRandomization<-function(N,K,Alloratio,blocksize,seed=1){
  ####
  Alloratio=as.numeric(Alloratio)
  blocksize=as.numeric(blocksize)
  ##Input Error check####
  if(N%%K!=0) stop(sprintf('N (%d) must be a multiple of K (%d)!', N, K))
  if(N%%sum(Alloratio)!=0) stop(sprintf('N (%d) must be a multiple of sum of Alloratio  (%d)!', N, sum(Alloratio)))
  if(length(Alloratio)!=K) stop(sprintf("The length of Alloratio (%d)  must match K (%d)!",length(Alloratio),K))
  if(any(N%%blocksize!=0)) stop(sprintf('N (%d) must be a multiple of blocksize  (%d)!', N, blocksize))
  ####
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
  allocation=allocation[1:N]+1
  ### return
  patientID=1:N
  assign=data.frame(patientID,allocation)
  colnames(assign)=c("patientID","group")
  summarytable=table(assign[,'group'])
  names(summarytable)=paste("group-",1:K,sep="")  
  smry <- table2df(summarytable)
  rownames(smry) <- ''
  return(list(assign=df_force_mode(assign, as.character, forcedf=TRUE),summary=df_force_mode(smry, as.integer)))
}


########################################################################
### Name: Stratified complete randomization
### Purpose: 
### Argument :
# N: vector, number of total sample size for each strata  
# K: number of treatment arm
# Alloratio: vector of size K. It is the ratio of patient allocation to each treatment arm
# seed: random seed. The default is seed to be 1.
### Value
# A list containing the following components:
# assign: a data frame for allocation.The column patientID is the patient sequence number.
#          The column group is the group that the patient is allocated to. The column strata is the strata
# summary: summary of allocation
######################################################################
StratifiedCompleteRandomization<-function(N,K,Alloratio,seed=seed){
  ###
  Alloratio=as.numeric(Alloratio)
  N=as.numeric(N)
  numstrata=length(N)
  allocation=NULL
  for(i in 1:numstrata){ 
    if(N[i]%%K!=0) stop(sprintf('N (%d) in the strata %i must be a multiple of K (%d)!', N[i],i, K))
    if(N[i]%%sum(Alloratio)!=0) stop(sprintf('N (%d) in the strata %i must be a multiple of sum of Alloratio  (%d)!', N[i], i,sum(Alloratio)))
    if(length(Alloratio)!=K) stop(sprintf("The length of Alloratio (%d)  must match K (%d)!",length(Alloratio),K))
    allocation=rbind(allocation,cbind(rep(i,N[i]),as.vector(CompleteRandomization(N=N[i],K=K,Alloratio=Alloratio,seed=seed+i)$assign[,"group"])))
  }
  patientID=1:sum(N)
  assign=cbind(patientID,allocation)
  colnames(assign)=c("patientID","strata","group")
  summarytable=table(assign[,"strata"],assign[,"group"])
  colnames(summarytable)=paste("group-",1:K,sep="")  
  rownames(summarytable)=paste("strata-",1:numstrata,sep="")
  return(list(assign=df_force_mode(data.frame(assign), as.character, forcedf=TRUE),summary=df_force_mode(table2df(summarytable), as.integer)))
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
# # assign: a data frame for allocation.The column patientID is the patient sequence number.
#          The column group is the group that the patient is allocated to. The column strata is the strata
# summary: summary of allocation
######################################################################
StratifiedBlockRandomization<-function(N,K,Alloratio,blocksize,seed=seed){
  ###
  Alloratio=as.numeric(Alloratio)
  N=as.numeric(N)
  numstrata=length(N)
  allocation=NULL
  for(i in 1:numstrata){
    if(N[i]%%K!=0) stop(sprintf('N (%d) in the strata %i must be a multiple of K (%d)!', N[i],i, K))
    if(N[i]%%sum(Alloratio)!=0) stop(sprintf('N (%d) in the strata %i must be a multiple of sum of Alloratio  (%d)!', N[i], i,sum(Alloratio)))
    if(length(Alloratio)!=K) stop(sprintf("The length of Alloratio (%d)  must match K (%d)!",length(Alloratio),K))
    if(any(N[i]%%blocksize!=0)) stop(sprintf('N (%d) in the strata %i must be a multiple of blocksize  (%d)!', N[i], i,blocksize))
    allocation=rbind(allocation,cbind(rep(i,N[i]),as.vector(BlockRandomization(N=N[i],K=K,blocksize=blocksize,Alloratio=Alloratio,seed=seed+i)$assign[,"group"])))
  }
  patientID=1:sum(N)
  assign=cbind(patientID,allocation)
  colnames(assign)=c("patientID","strata","group")
  summarytable=table(assign[,"strata"],assign[,"group"])
  colnames(summarytable)=paste("group-",1:K,sep="")  
  rownames(summarytable)=paste("strata-",1:numstrata,sep="")
  return(list(assign=df_force_mode(data.frame(assign), as.character, forcedf=TRUE),summary=df_force_mode(table2df(summarytable), as.integer)))
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
#        the last column is the allocation ==> column 1 is forced to be patient ID
# newdf:  dataframe. The new randomization information. the first nfactor column are the factors. 
#        the last column is the allocation(set to be NA)  ==> column 1 is forced to be patient ID
### Value
# A list containing the following components:
# allocation: a matrix for allocation
# summary: summary of allocation
######################################################################

MinimizationRandomization<-function(K,nfactor,nlevel,Alloratio,seed=seed,olddf='',newdf,weight=''){
##
  olddf <- empty2null(olddf)
  olddf <- list2df(olddf)
  newdf <- list2df(newdf)
  if(!is.null(olddf)){
    if(!identical(colnames(olddf), colnames(newdf))){
      stop('olddf and newdf should have same colname!')
    }
  }
  if(length(weight)==1){
    if(weight=='') weight <- rep(1, nfactor)
  }
  if(length(weight)!=nfactor) stop("length of weight vector should be consistent with nfactor.")
  #browser()
  # no matterwhat, force colname as: xx, F1, F2, ..., xx
  originalcname = forcedcname = colnames(newdf)
  # python dict --> json input --> dict may lose ordering for the data frame. Need to ensure this since list ordering is important here!
  # following solution is error-prone: other index may disordered due to not-alpha ordering in reality
  # ensureOrdering <- function(df){
  #   if(is.null(df))
  #     return(df)
  #   ind_pid <- match('PatientID', colnames(newdf))
  #   ind_trt <- match('treatment', colnames(newdf))
  #   if(length(ind_pid)==0) stop(sprintf('Cannot find PatientID. Observed: %s', str_c(colnames(newdf))))
  #   ind_other <- sort(setdiff(colnames(newdf), c('PatientID', 'treatment')), decreasing=FALSE)
  #   df <- df[, c(ind_pid, ind_trt, ind_other)]
  #   df
  # }
  #olddf <- ensureOrdering(olddf)
  #newdf <- ensureOrdering(newdf)
  forcedcname <- c('patientID', paste0('F', 1:(length(originalcname)-2)), 'group')
  if(!is.null(olddf)){
    colnames(olddf) <- colnames(newdf) <- forcedcname
  } else {
    colnames(newdf) <- forcedcname
  }
  # python list to R vector
  nlevel=as.numeric(nlevel) 
  Alloratio=as.numeric(Alloratio)
  weight=as.numeric(weight) 
  idnew = as.character(newdf[, 1])
  newdf=newdf[,-1]
##  
  if(length(Alloratio)!=K) stop(sprintf("The length of Alloratio (%d)  must match K (%d)!",length(Alloratio),K))
  if(length(nlevel)!=nfactor) stop(sprintf("The length of nlevel (%d)  must match nfactor (%d)!",length(nlevel),nfactor))
  
  expt0 <- ClinicalExperiment(number.of.factors = nfactor,
                              number.of.factor.levels = nlevel,
                              number.of.treatments = K)
  g.func <- function(imbalances) {
    factor.weights <- weight
    imbalances %*% factor.weights
  }
  r.obj <- new("PocockSimonRandomizer", expt0, as.integer(seed),tr.ratios=Alloratio,g.func=g.func)
  if(!is.null(olddf)){
    idold = as.character(olddf[, 1])
    olddf=olddf[,-1]
    colnames(olddf)[ncol(olddf)]="Treatment"
    r.obj@tr.assignments=olddf
  }
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
  #auto generated ID. patientID=1:nrow(r.objnew@tr.assignments)
  # user supplied iD
  if(is.null(olddf)){
    patientID <- idnew 
  } else {
    patientID <- c(idold, idnew)
  }
  #browser()
  # impose colname is same as input; otherwise, if olddf and newdf has different colname, error emit; 
  assign0 <- data.frame(r.objnew@tr.assignments)
  #colnames(assign0) <- colnames(newdf) # the output always capitalize colname; now force it as newdf colname
  assign=cbind(patientID,assign0)
  assign[,ncol(assign)]=unlist(assign[,ncol(assign)])
  colnames(assign) <- originalcname
  colnames(assign)[ncol(assign)]="group"
  #summarytable=t(df_force_mode(r.objnew@stateTable, as.integer))
  #summarytable=t(df_force_mode(r.obj@stateTable, as.integer))
  summarytable=MinimizationSummary(assign,nlevel,K)
  list(assign=df_force_mode(assign, as.character, forcedf=TRUE),summary=df_force_mode(summarytable,as.integer))
}
