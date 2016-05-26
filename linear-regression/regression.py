# -*- coding: utf-8 -*-
"""
Created on Thu May 26 12:24:18 2016

@author: Fengwei
"""

from numpy import *

def loadDataSet(filename):
    width = len(open(filename).readline().split('\t')) - 1 
    
    dataMat = []
    labelVec = []

    filehandle = open(filename)
    for line in filehandle.readlines():
        
        linelist = []
        curline = line.strip().split('\t')
                
        for i in range(width):
            linelist.append(float(curline[i]))
            
        dataMat.append(linelist)
        labelVec.append(float(curline[-1]))
        
    return dataMat, labelVec
    
def normalequation(x,y):
    x = mat(x)
    y = mat(y).T
    if linalg.det(x.T * x) == 0.0:
        print "sigular, can not inverse"
        return
    theta = (x.T * x).I *(x.T * y)
    return theta

def lwlr(testPoint, xArr,yArr,k=1.0):
    xMat = mat(xArr);  yMat = mat(yArr).T
    m = shape(xMat)[0]
    weights = mat(eye((m)))
    for j in range(m):
        diffMat = testPoint - xMat[j,:]
        weights[j,j] = exp(diffMat * diffMat.T / (-2.0 * k **2))
    xTx = xMat.T * (weights *xMat)
    if linalg.det(xTx) == 0.0:
        print "singular, can not do inverse"
        return
    theta = xTx.I * (xMat.T * (weights * yMat))
    return testPoint * theta

def lwlrTest(testArr,xArr,yArr,k=1.0):
    m = shape(testArr)[0]
    yHat = zeros(m)
    for i in range(m):
        yHat[i] = lwlr(testArr[i],xArr,yArr,k)
    return yHat


def rssError(yArr,yHatArr):
    return ((yArr - yHatArr)**2).sum()
    
    
def ridgeRegres(xMat,yMat,lam=0.2):
    xTx = xMat.T*xMat
    denom = xTx + eye(shape(xMat)[1])*lam
    if linalg.det(denom) == 0.0:
        print 'sigular, can not inverse'
        return
    ws = denom.I * (xMat.T * yMat)
    return ws

def ridgeTest(xArr,yArr):
    xMat=mat(xArr);yMat=mat(yArr).T
    yMean = mean(yMat,0)
    yMat = yMat - yMean
    xMeans = mean(xMat,0)
    xVar = var(xMat,0)
    xMat = (xMat - xMeans) / xVar
    numTestPts = 30
    wMat = zeros((numTestPts,shape(xMat)[1]))
    for i in range(numTestPts):
        ws = ridgeRegres(xMat,yMat,exp(i-10))
        wMat[i,:] =ws.T
    return wMat

def stageWise(xArr,yArr,eps=0.01,numIt = 100):
    xMat = mat(xArr);yMat = mat(yArr).T
    yMean = mean(yMat,0)
    yMat = yMat - yMean
    xMat = regularize(xMat)
    m,n = shape(xMat)
    returnMat = zeros((numIt,n))
    ws = zeros((n,1));wsTest = ws.copy();wsMax = ws.copy()
    for i in range(numIt):
        print ws.T
        lowestError = inf
        for j in range(n):
            for sign in [-1,1]:
                wsTest = ws.copy()
                wsTest[j] += eps*sign
                yTest = xMat * wsTest
                rssE = rssError(yMat.A, yTest.A)
                if rssE < lowestError:
                    lowestError = rssE
                    wsMax = wsTest
        ws = wsMax.copy()
        returnMat[i,:] = ws.T
    return returnMat

def regularize(x):
    return (x-mean(x,axis=0))/var(x,axis=0)
    
#google Api
    
from time import sleep
import json
import urllib2
def searchForSet(retX,retY,setNum,yr,numPce,origprc):
    sleep(10)
    myAIPstr = 'get from code.google.com'
    searchURL = 'https://www.googleapis.com/shopping/search/v1/public/products?\
        key=%s&country=US&q=lego+%d&alt=json' % (myAIPstr, setNum)
    pg = urllib2.urlopen(searchURL)
    retDict = json.loads(pg.read())
    for i in range(len(retDict['items'])):
        try:
            currItem = retDict['items']['i']
            if currItem['product']['condition'] == 'new':
                newFlag = 1
            else:
                newFlag = 0
            listofInv = currItem['product']['inventories']
            for item in listOfInv:
                sellingPrice = item['price']
                if sellingPrice > origPrc * 0.5:
                    print "%d\t%d\t%d\t%f\t%f"%\
                        (yr,numPce,newFlag,origPrc,sellingPrice)
                    retX.append([yr,numPce,newFlag,origPrc])
                    retY.append(sellingPrice)
        except:
            print 'problem with item %d' % i
            
def setDataCollect(retX,retY):
    searchForSet(retX, retY, 8288, 2006, 800, 49.99)
    searchForSet(retX, retY, 10030, 2002, 3096, 269.99)
    searchForSet(retX, retY, 10179, 2007, 5195, 499.99)
    searchForSet(retX, retY, 10181, 2007, 3428, 199.99)
    searchForSet(retX, retY, 10189, 2008, 5922, 299.99)
    searchForSet(retX, retY, 10196, 2009, 3263, 249.99)
                        