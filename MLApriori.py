#!/usr/bin/env python
# -*- coding: utf-8 -*-

#@Time: 2020/6/24 21:43
#@Project: ML
#@Author: 孤小绵羊
def loaddata():
    return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]
def createC1(dataset):
    c1 = []
    ##该代码时将数据集中每列不重复元素取出，形成新的数据集，以列形式，并且为冰冻集合
    for transaction in dataset:
        for item in transaction:
            if not [item] in c1:
                c1.append([item])
    c1.sort()

    return list(map(frozenset, c1))
'''
输入
d 集合数据集;c1 冰冻集合，所有出现的项集;minsupport 最小支持度
输出
retlist 满足要求的项集;supportdata 支持度矩阵
遍历d，c1 判断冰冻集合中的元素是否在数据集中，统计集合中单个数据出现的次数，填入字典中
遍历字典，根据元素出现的次数/数据集的大小的比值与支持度作比较，
满足的填入所要输出的列表中，并存入字典中，key 是元素，value为支持度
'''
def scan(d, c1, minsupport):
    sscnt = {}
    for i in d:
        for j in c1:
            if j.issubset(i):
                if j not in sscnt.keys():
                    sscnt[j] = 1
                else:
                    sscnt[j] += 1
    numitem = float(len(d))
    retlist = []
    supportdata = {}
    for key in sscnt:
        support = sscnt[key] / numitem
        if support >= minsupport:
            retlist.insert(0, key)
        supportdata[key] = support
    return retlist, supportdata
'''
将元素进行组合
输入lk=集合元素
k=2
输出组合集合
前 k-2项相同时，两两合并
'''
def aprioriGen(lk,k):
    retList=[]
    lenlk=len(lk)
    #lk的长度
    for i in range(lenlk):
        #循环遍历lk
        for j in range(i+1,lenlk):
            #在上层循环基础上，继续循环
            l1=list(lk[i])[:k-2];l2=list(lk[j])[:k-2]
            #取出lk在为i位置时的前k-2个，在循环位置为j的前k-2个
            l1.sort();l2.sort()
            #上述列表排序
            if l1 ==l2:
                #如果两者相等，就取并集，|这玩意就是集合取并
                retList.append(lk[i]|lk[j])
            # print(retList)
    return retList
'''
输入：数据，支持度
输出频繁项集，支持度矩阵
'''
def apriori(dataset,minsupport):
    c1=createC1(dataset)
    d=list(map(set,dataset))
    l1,supportdata=scan(d,c1,minsupport)
    l=[l1]
    k=2
    while (len(l[k-2])>0):
        ck=aprioriGen(l[k-2],k)
        lk,supk=scan(d,ck,minsupport)
        supportdata.update(supk)
        l.append(lk)
        k+=1
    return l,supportdata
# l,supportdara=apriori(loaddata(),0.7)


def generateRules(l,supportdata,minconf=0.7):
    #l的存储方式为0列为频繁项集为一个的元素，1列频繁项集为两个，其余的依次类推
    bigrulelist=[]
    for i in range(1,len(l)):
        print('第{0}次遍历频繁项集,频繁项集为{1}'.format(i,l[i]))
        #循环遍历频繁项集
        for freqset in l[i]:
            #遍历频繁项集中每个元素
            h1=[frozenset([item]) for item in freqset]
            #将频繁项集拆开，形成独立频繁项集集合
            if i>1:
                rulesFromConseq(freqset, h1, supportdata, bigrulelist, minconf)
                #生成关联股则，传入参数分别为频繁项集，频繁项集形成的集合、支持度字典，满足支持度和置信度的信息，列表形式，最小置信度
            else:
                calcconf(freqset, h1, supportdata, bigrulelist, minconf)
                #计算支持度，传入参数分别为频繁项集，频繁项集形成的集合、支持度字典，满足支持度和置信度的信息，列表形式，最小置信度。
    return bigrulelist

def calcconf(freqset,h,supportdata,brl,minconf=0.7):
    prunedh=[]
    print('freqset~~~~~~~~',freqset)
    for conseq in h:
        conf =supportdata[freqset]/supportdata[freqset-conseq]
        #freqset-conseq 返回的是冰冻集合内部相减，例如：frozenset({2, 5})-frozenset({2})，返回frozenset({5})
        #frozenset({2, 5})-frozenset({1})，返回frozenset({2,5})
        #计算单个元素在总体中的置信度

        if conf >= minconf:
            #判断条件，如果计算的置信度满足最小置信度条件
            print(freqset-conseq,'---->',conseq,'cof',conf)
            brl.append((freqset-conseq,freqset,conseq,conf))
            print(brl)
            #bigrulelist中存入以上信息（以元组形式存储），freqset-conseq,conseq,conf
            prunedh.append(conseq)
            #添加频繁项集
    return prunedh
def rulesFromConseq(freqset,h,supportdata,brl,minconf=0.7):
    m=len(h[0])
    if(len(freqset)>(m+1)):
        #如果频繁项集的个数大于频繁项集第一个项集的元素数加一，否则结束
        hmp1=aprioriGen(h,m+1)
        #频繁项集要进行m+1次的重新生成无重复
        hmp1=calcconf(freqset,hmp1,supportdata, brl,minconf)
        #重新计算支持度
        if(len(hmp1)>1):
            #若频繁项更多的集存在，则调用本函数继续组合，直到不满足条件为止退出
            rulesFromConseq(freqset,hmp1,supportdata, brl,minconf)


l,supportdata=apriori(loaddata(),0.7)
print(supportdata)
bigrulelist = generateRules(l,supportdata,minconf=0.7)