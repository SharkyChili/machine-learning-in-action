# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#PCA

from numpy import *

def loadDataSet(fileName, delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    datArr = [map(float,line)for line in stringArr]
    return mat(datArr)
    
def pca(dataMat, topNfeat = 9999999):
    meanVals = mean(dataMat, axis = 0)
    meanRemoved = dataMat - meanVals
    #covariance matrix, x.T * x
    #If rowvar is True (default), then each row represents a variable, with observations in the columns
    #covMat = cov(meanRemoved, rowvar = False)
    #Compute the eigenvalues and right eigenvectors of a square array.
    #eigVals,eigVects = linalg.eig(mat(covMat))
    #Returns the indices that would sort an array.
    s,eigVals,d = linalg.svd(meanRemoved)
    eigVects = d.T
    
    eigValInd = argsort(eigVals)
    eigValInd = eigValInd[:-(topNfeat + 1):-1]
    redEigVects = eigVects[:,eigValInd]
    lowDDataMat = meanRemoved * redEigVects
    reconMat = (lowDDataMat * redEigVects.T) + meanVals
    return lowDDataMat, reconMat
    
def replaceNanWithMean():
    dataMat = loadDataSet('secom.data',' ')
    numFeat = shape(dataMat)[1]
    for i in range(numFeat):
        #isnan fuction returns boolean for each element
        meanVal = mean(dataMat[nonzero(~isnan(dataMat[:,i].A))[0], i ] )
        
        dataMat[nonzero(isnan(dataMat[:,i].A))[0], i] = meanVal
    return dataMat
    
