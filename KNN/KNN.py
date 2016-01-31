# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import operator
from os import listdir
#KNN

def Classify(inx, dataset, labels, k):
    """inx(1*n) dataset(m*n) labels(m*1) k = number in front"""
    
    #get the traingset size
    m = dataset.shape[0]
    
    #caculate distance
    #note: np do caculate by element 
    distances = np.sqrt(np.square(np.ones((m,1)) * inx - dataset).sum(axis=1))
    
    #put distance in a dictionary
    dic = {}
    for i in range(k):
        lab = labels[distances.argsort()[i]]
        dic[lab] = dic.get(lab,0) + 1
        
    #sort dictionary
    sortdic = sorted(dic.iteritems(),key = operator.itemgetter(1), reverse = True)
    return sortdic[0][0]


def file2matrix(filename):
    """deal with text"""
    
    #read text to list
    lst = open(filename).readlines()
    m = len(lst)
    
    #initial trainingset X,Y
    Xmatrix = np.zeros((m,3))
    Ylst = []
    dic = {'largeDoses':3,'smallDoses':2,'didntLike':1}
    
    row = 0
    for line in lst:
        linelst = line.strip().split('\t')
        
        Xmatrix[row,:] = linelst[0:3]
        Ylst.append(int(dic[linelst[-1]]))
        row = row + 1
    return Xmatrix, Ylst


def autoNorm(dataSet):
    """regularization the training set"""
    
    #get min max range
    minbycol = dataSet.min(0)
    maxbycol = dataSet.max(0)
    ranges = (maxbycol - minbycol).astype(float)
    
    #regularization
    normdataSet = np.zeros(dataSet.shape)
    m = dataSet.shape[0]
    normdataSet = (dataSet - np.ones((m,1))* minbycol)/ranges
    
    return normdataSet, ranges, minbycol
    
def datingClassTest(test=0.1,k=3):
    """auto test classifier"""
    
    #prepare data
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    
    #set some value
    testpercent = test
    m = normMat.shape[0]
    numtest = int(m * testpercent)    
    
    #test  first numtest row to be test, other rows be training set
    error = 0
    for i in range(numtest):
        result = Classify(normMat[i,:],normMat[numtest:m,:],datingLabels[numtest:m],k)
        print "the classifier came back with: %d ,the real answer is: %d"%(result,datingLabels[i])
        if result != datingLabels[i]:
            error += 1
    print "the total error rate: %f" %(error/float(numtest))
    
    
def classifyPerson():
    """classify by input"""
    
    #set some value
    resultlist = ['not at all','in small doses','in large doses']
    numvideo = float(raw_input('percentage of time spent playing video games?'))
    numflymile = float(raw_input('frequent flier miles earned per year:'))
    numicecream = float(raw_input('liters of ice cream consumed per year?'))
    
    #prepare data
    datingDataMat,datingLabels = file2matrix('datingTestSet.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = np.array([numflymile,numvideo,numicecream])
    
    #attention: inArr has only one row, so the ranges will error,don't use autoNorm
    #norminArr = autoNorm(inArr)
    #numresult = Classify(norminArr, normMat, datingLabels,3)
    numresult = Classify((inArr - minVals)/ranges,normMat,datingLabels,3)
    result = resultlist[numresult - 1]
    print "You will probably like this person: ", result
    
def img2vector(filename):
    """transform image to vector"""
    
    #initial value, set a hand on txt
    vec = np.zeros((1,1024))
    fhand = open(filename)

    #'readline() read the text line by line,btw,readlines() read the text as a list
    for i in range(32):
        line = fhand.readline()
        
    #seperate the line string and set the vector
        for j in range(32):
            vec[0, 32*i + j]=int(line[j])
    return vec
    
def handwritingClassTest():
    labels = []
    filelist = listdir('trainingDigits')
    m = len(filelist)
    trainingMat = np.zeros((m,1024))
    for i in range(m):
        trainingMat[i:] = img2vector('trainingDigits/%s' % filelist[i])
        labels.append(int(filelist[i].split('.')[0].split('_')[0]))
    
    testfile = listdir('testDigits')
    error = 0.0
    mtest = len(testfile)
    for i in range(mtest):
        testvec = img2vector('testDigits/%s' % testfile[i])
        testlab = int(testfile[i].split('.')[0].split('_')[0])
        result = Classify(testvec, trainingMat, labels, 3)
    
        print "the classifier came back with: %d, the real answer is %d " %(result, testlab)
        if result != testlab:
            error += 1
    print "\nthe total number of errors is: %d" % error
    print "\nthe total error rate is: %f" %(error/mtest)