# -*- coding: utf-8 -*-  
import time            
import re            
import os  
import string  
import sys  
import math  
  
  
''''' ------------------------------------------------------- '''  
#统计关键词及个数  
def CountKey(fileName, resultName):  
    try:  
        #计算文件行数  
        lineNums = len(open(fileName,'rU').readlines())  
        print u'文件行数: ' + str(lineNums)  
  
        #统计格式 格式<Key:Value> <属性:出现个数>  
        i = 0  
        table = {}  
        source = open(fileName,"r")  
        result = open(resultName,"w")  
          
        while i < lineNums:  
            line = source.readline()  
            line = line.rstrip('\n')  
            print line  
              
            words = line.split("=")  #空格分隔  
            # print str(words).decode('string_escape') #list显示中文  
              
            #字典插入与赋值  
            for word_info in words:  
                word = word_info.replace('\r', '').replace('\n', '').replace('\t', '').strip()
                if word != "" and table.has_key(word):      #如果存在次数加1  
                    num = table[word]  
                    table[word] = num + 1  
                elif word != "":                            #否则初值为1  
                    table[word] = 1  
            i = i + 1  
  
        #键值从大到小排序 函数原型：sorted(dic,value,reverse)  
        dic = sorted(table.iteritems(), key = lambda asd:asd[1], reverse = True)  
        for i in range(len(dic)):  
            #print 'key=%s, value=%s' % (dic[i][0],dic[i][1])  
            result.write("<"+dic[i][0]+":"+str(dic[i][1])+">\n")  
        return dic  
          
    except Exception,e:      
        print 'Error:',e  
    finally:  
        source.close()  
        result.close()  
        print 'END\n\n'  
  
  
''''' ------------------------------------------------------- '''  
#统计关键词及个数 并计算相似度  
def MergeKeys(dic1,dic2):  
    #合并关键词 采用三个数组实现  
    arrayKey = []  
    for i in range(len(dic1)):  
        arrayKey.append(dic1[i][0])       #向数组中添加元素  
    for i in range(len(dic2)):         
        if dic2[i][0] in arrayKey:  
            print 'has_key',dic2[i][0]  
        else:                             #合并  
            arrayKey.append(dic2[i][0])  
    else:  
        print '\n\n'  
      
    test = str(arrayKey).decode('string_escape')  #字符转换  
    print test  
  
    #计算词频 infobox可忽略TF-IDF  
    arrayNum1 = [0]*len(arrayKey)  
    arrayNum2 = [0]*len(arrayKey)  
      
    #赋值arrayNum1  
    for i in range(len(dic1)):       
        key = dic1[i][0]  
        value = dic1[i][1]  
        j = 0  
        while j < len(arrayKey):  
            if key == arrayKey[j]:  
                arrayNum1[j] = value  
                break  
            else:  
                j = j + 1  
  
    #赋值arrayNum2  
    for i in range(len(dic2)):       
        key = dic2[i][0]  
        value = dic2[i][1]  
        j = 0  
        while j < len(arrayKey):  
            if key == arrayKey[j]:  
                arrayNum2[j] = value  
                break  
            else:  
                j = j + 1  
      
    print arrayNum1  
    print arrayNum2  
    print len(arrayNum1),len(arrayNum2),len(arrayKey)  
  
    #计算两个向量的点积  
    x = 0  
    i = 0  
    while i < len(arrayKey):  
        x = x + arrayNum1[i] * arrayNum2[i]  
        i = i + 1  
    print x  
  
    #计算两个向量的模  
    i = 0  
    sq1 = 0  
    while i < len(arrayKey):  
        sq1 = sq1 + arrayNum1[i] * arrayNum1[i]   #pow(a,2)  
        i = i + 1  
    print sq1  
      
    i = 0  
    sq2 = 0  
    while i < len(arrayKey):  
        sq2 = sq2 + arrayNum2[i] * arrayNum2[i]  
        i = i + 1  
    print sq2  
      
    result = float(x) / ( math.sqrt(sq1) * math.sqrt(sq2) )  
    return result  
      
  
''''' -------------------------------------------------------  
    基本步骤： 
        1.分别统计两个文档的关键词 
        2.两篇文章的关键词合并成一个集合,相同的合并,不同的添加 
        3.计算每篇文章对于这个集合的词的词频 TF-IDF算法计算权重 
        4.生成两篇文章各自的词频向量 
        5.计算两个向量的余弦相似度,值越大表示越相似                              
    ------------------------------------------------------- ''' 
#主函数
def main():
    #计算文档1-百度的关键词及个数
    # fileName1 = BaiduSpider.txt
    # resultName1 = Result_Key_BD.txt
    fileName1 = './4.py'
    resultName1 = './1.txt'
    dic1 = CountKey(fileName1, resultName1)
     
    #计算文档2-互动的关键词及个数
    # fileName2 = HudongSpider\001.txt
    # resultName2 = HudongSpider\Result_Key_001.txt
    fileName2 = './5.py'
    resultName2 = './2.txt'
    dic2 = CountKey(fileName2, resultName2)
 
    #合并两篇文章的关键词及相似度计算
    result = MergeKeys(dic1, dic2)
    print result
 
 
if __name__ == '__main__':
    main()