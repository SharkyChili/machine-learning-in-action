# -*- coding: utf-8 -*-
"""
Created on Mon Feb 01 09:43:24 2016

@author: Feng Wei
"""

from math import log
import operator

def calcShannonEnt(dataSet):
    """calculate Shannon Entropy"""
    
    #initial some value
    m = len(dataSet)
    dic = {}
    
    #establish the dictionary, include lebel: number
    for row in dataSet:
        key = row[-1]
        dic[key] =dic.get(key, 0) + 1
    
    #calculate Shannon Entropy, attention the "float"
    shannonEnt = 0.0
    for key in dic:
        p = float(dic[key]) / m
        shannonEnt -= p * log(p, 2)
    return shannonEnt 

def createDataSet():
    """create a dataset"""
    
    dataSet = [[1,1,'yes'],
               [1,1,'yes'],
                [1,0,'no'],
                [0,1,'no'],
                [0,1,'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels

def splitDataSet(dataSet, axis, value):
    """split the dataSet for the row[axis] == value"""
    
    retDataSet = []
    for row in dataSet:
        if row[axis] == value:
    #split the row with the row[axis]
            splitlist = row[:axis]
            splitlist.extend(row[axis+1:])
            
    #appdend the splited row as a element ( row with out row[axis])
            retDataSet.append(splitlist)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    """find which column is the best split feature"""
    
    #initial some value
    colind = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    inforgain = 0.0
    bestFeature = -1
    
    #get the feature
    for i in range(colind):
        collist = [row[i] for row in dataSet]
        collist = set(collist)

    #calculate the entropy
        Entropy = 0.0        
        for value in collist:
            subDataSet = splitDataSet(dataSet, i, value)
            p = float(len(subDataSet)) / len(dataSet)
            Entropy += p * calcShannonEnt(subDataSet)

    #calculate the inforgain (ie. the loss of entropy)
        subinforgain = baseEntropy - Entropy

    #for each feature(ie. column), find the biggest inforgain
        if subinforgain > inforgain:
            inforgain = subinforgain
            bestFeature = i
    return bestFeature
    
def majorityCnt(classList):
    """get the most frequent value """
    
    #use dictionary to solve problem
    classCount = {}
    for vote in classList:
        classCount[vote] = classCount.get(vote,0) + 1
        
    #sort dictionary
    sortedClassCount = sorted(classCount.iteritems(),\
                        key = operator.itemgetter(1),reverse = True)

    #return the most frequent value
    return sortedClassCount[0][0]
    
def createTree(dataSet, labels):
    """create tree"""
    
    #get the last column, ie. y
    classList = [example[-1] for example in dataSet]
    
    #if lebels is equal, stop 
    if classList.count(classList[0]) == len(classList):
        return classList[0]
        
    #if all feature used, return the maximun
    if len(dataSet) == 1:
        return majorityCnt(classList)
    
    #choose feature to split and delete the label
    #create the tree list
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    
    #get the column unique values
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    
    #fill teh dic inside the dic { { }}
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet\
                            (dataSet, bestFeat, value), subLabels)
    return myTree
    
def classify(inputTree,featLabels,testVec):
    """ classifier"""
    
    #set the beginning of the cycle, it can be used in recursion with out modify
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    
    #find the test[featIndex] == key; the featIndex is the beginning of this cycle
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key],featLabels,testVec)
            else:
                classLabel = secondDict[key]
    return classLabel

def storeTree(inputTree, filename):
    import pickle
    fw = open(filename,'w')
    pickle.dump(inputTree,fw)
    fw.close()

def grabTree(filename):
    import pickle
    fr= open(filename)
    return pickle.load(fr)