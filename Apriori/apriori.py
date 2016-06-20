# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 12:28:42 2016

@author: Fengwei
"""

#Apriori

def loadDataSet():
    return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]
    
def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return map(frozenset, C1)
    
def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
#                if not ssCnt.has_key(can):
#                    ssCnt[can] = 1
#                else:
#                    ssCnt[can] += 1
                ssCnt[can] = ssCnt.get(can,0) + 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retList.insert(0,key)
        supportData[key] = support
    return retList, supportData
    

def aprioriGen(Lk,k):
    retList = []
    lenLk = len(Lk)
    #print "**********************************"
    for i in range(lenLk):
        for j in range(i+1,lenLk):
            L1 = list(Lk[i])[:k]
            L2 = list(Lk[j])[:k]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    #print "*************************************"
    return retList
    
def apriori(dataSet, minSupport = 0.5):
    C1 = createC1(dataSet)
    #print "Ck 1:",C1
    D = map(set, dataSet)
    L1, supportData = scanD(D, C1, minSupport)
    #print "Lk 1:",L1
    L = [L1]
    k = 0
    while (len(L[k]) > 0 ):
        Ck = aprioriGen(L[k] , k)
        #print "Ck:",Ck
        Lk, supK = scanD(D, Ck, minSupport)
        #print "Lk:", Lk
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData
    
def generateRules(L, supportData, minConf=0.7):
    bigRuleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            print 'freqSet:',freqSet
            print 'H1:',H1
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList
    
def calcConf(freqSet, H, supportData, brl, minConf = 0.7):
    print '****************************************'
    print 'Calc'
    print 'H:', H
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf:
            print freqSet-conseq, '-->', conseq,'conf:',conf
            brl.append((freqSet-conseq, conseq, conf))
            prunedH.append(conseq)
    print '--------------------------------------------'
    return prunedH
    
def rulesFromConseq(freqSet, H, supportData, br1, minConf = 0.7):
    print '*************************'
    print 'rules'
    print 'H:', H
    m = len(H[0])
    print "m=",m
    if (len(freqSet) > (m + 1) ):
        Hmp1 = aprioriGen(H,m - 1)
        print 'Generate super set ',Hmp1
        Hmp1 = calcConf(freqSet, Hmp1, supportData, br1, minConf)
        print 'cal Hmp1:',Hmp1
        if (len(Hmp1) > 1):
            rulesFromConseq(freqSet, Hmp1, supportData, br1, minConf)
    print '--------------------------------------------'
