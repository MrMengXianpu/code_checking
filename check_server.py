# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, request, flash, render_template, jsonify  
# from flask_login import LoginManager, login_user, login_required, logout_user
from flask_cors import *
import time            
import re            
import os  
import string  
import sys  
import math

app = Flask(__name__)
CORS(app, supports_credentials=True)

code_id = ''

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():

    global code_id

    if request.method == 'POST':
        code_id = request.form['code_id']
        print code_id
        file_path = '/Users/MrM/Desktop/' + code_id + '/'
        
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        print request.files

        for file in request.files:
            file_name = request.files[file].filename
            request.files[file].save(file_path + file_name)
            # print file
        return 'succ'


@app.route('/check', methods=['GET', 'POST'])
def start_check():
    file_list = []
    for root, dirs, files in os.walk('/Users/MrM/Desktop/' + code_id):
        for file in files:
            file_list.append(root + '/' + file)

    return_info_list = []

    for i in range(len(file_list)):
        score_list = []
        for j in range(len(file_list)):
            if file_list[i] != file_list[j]:
                check_re = check_two_file(file_list[i], file_list[j])
                score_list.append(check_re)
                print 'the result of ' + file_list[i].split('/')[-1] + 'and' + file_list[j].split('/')[-1] + ' is ----- ' + str(check_re)
            
        re_score_list = sort(score_list)
        print re_score_list

        result_info = file_list[i].split('/')[-1] + ' : ' + str(re_score_list[-1])
        print result_info
        return_info_list.append(result_info)

    return_info_str = ''
    for item in return_info_list:
        return_info_str += (item + ',')

    return jsonify(return_info_str)
    # return 'done'


def sort(list):
    if len(list) <= 1:
        return list

    middle_index = len(list) / 2
    left = sort(list[:middle_index])
    right = sort(list[middle_index:])

    return merge(left, right)


def merge(left, right):
    merge_list = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):

        if left[i] < right[j]:
            merge_list.append(left[i])
            i += 1

        else:
            merge_list.append(right[j])
            j += 1

    if i == len(left):
        for x in right[j:]:
            merge_list.append(x)

    else:
        for x in left[i:]:
            merge_list.append(x)

    return merge_list


def check_two_file(file_1, file_2):
    # res_1 = file_1.split('.')[0] + '_res.txt'

    if not os.path.exists('/Users/MrM/Desktop/' + code_id + '_res/'):
        os.makedirs('/Users/MrM/Desktop/' + code_id + '_res/')

    res_1 = '/Users/MrM/Desktop/' + code_id + '_res/' + file_1.split('/')[-1].split('.')[0] + '_res.txt'
    dic1 = CountKey(file_1, res_1)

    # res_2 = file_2.split('.')[0] + '_res.txt'
    res_2 = '/Users/MrM/Desktop/' + code_id + '_res/' + file_2.split('/')[-1].split('.')[0] + '_res.txt'
    dic2 = CountKey(file_2, res_2)

    check_result = MergeKeys(dic1, dic2)
    print check_result
    return check_result




''''' ------------------------------------------------------- '''  
#统计关键词及个数  
def count_key(file_path, result_path):  
    try:  
        #计算文件行数  
        lineNums = len(open(file_path,'rU').readlines())  
        print u'文件行数: ' + str(lineNums)  
  
        #统计格式 格式<Key:Value> <属性:出现个数>  
        # i = 0  
        table = {}  
        source = open(file_path,"r")  
        count_result = open(result_path,"w")  
        lines = source.readlines()
        for line in lines:  
        # while i < lineNums:  
            # line = source.readline()  
            line = line.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('{', ' { ').replace('}', ' } ').replace(';', ' ; ').replace('=', ' = ').replace('.', ' . ').replace(',', ' , ').replace(':', ' : ').replace('(', ' ( ').replace(')', ' ) ').replace('+', ' + ').replace('-', ' - ').replace('*', ' * ').replace('/', ' / ').replace('<', ' < ').replace('>', ' > ')
            print line  
              
            words = line.split(" ")  #空格分隔  
            # print str(words).decode('string_escape') #list显示中文  
              
            #字典插入与赋值  
            for word_info in words:  
                # word = word_info.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ').strip()
                if word_info != "" and table.has_key(word_info):      #如果存在次数加1  
                    num = table[word_info]  
                    table[word_info] = num + 1  
                elif word_info != "":                            #否则初值为1  
                    table[word_info] = 1  
            # i = i + 1  
  
        #键值从大到小排序 函数原型：sorted(dic,value,reverse)  
        dic = sorted(table.iteritems(), key = lambda asd:asd[1], reverse = True)  
        for i in range(len(dic)):  
            #print 'key=%s, value=%s' % (dic[i][0],dic[i][1])  
            count_result.write("<" + dic[i][0] + ":" + str(dic[i][1]) + ">\n")  
        return dic  
          
    except Exception, e:      
        print 'Error:', e  
    finally:  
        source.close()  
        count_result.close()  
        print 'END\n\n'  
  
  
''''' ------------------------------------------------------- '''  
#统计关键词及个数 并计算相似度  
def merge_keys(dic1, dic2):  
    #合并关键词 采用三个数组实现  
    array_key = []  
    # for i in range(len(dic1)):  
    #     array_key.append(dic1[i][0])       #向数组中添加元素  
    # for i in range(len(dic2)):         
    #     if dic2[i][0] in array_key:  
    #         print 'has_key',dic2[i][0]  
    #     else:                             #合并  
    #         array_key.append(dic2[i][0])  
    # else:  
    #     print '\n\n'  

    for item_1 in dic1:
        array_key.append(item_1[0])
        
    for item_2 in dic2:
        if item_2[0] in array_key:
            pass
        else:
            array_key.append(item_2[0])
      
    test = str(array_key).decode('string_escape')  #字符转换  
    print test  
  
    #计算词频  
    array_num1 = [0]*len(array_key)  
    array_num2 = [0]*len(array_key)  
      
    #赋值array_num1  
    # for i in range(len(dic1)):       
    #     key = dic1[i][0]  
    #     value = dic1[i][1]  
    #     j = 0  
    #     while j < len(array_key):  
    #         if key == array_key[j]:  
    #             array_num1[j] = value  
    #             break  
    #         else:  
    #             j = j + 1  


    for item in dic1:
        key = item[0]
        value = item[1]
        j = 0
        while j < len(array_key):
            if key == array_key[j]:
                array_num1[j] = value
                break
            else:
                j += 1 

  
    #赋值array_num2  
    # for i in range(len(dic2)):       
    #     key = dic2[i][0]  
    #     value = dic2[i][1]  
    #     j = 0  
    #     while j < len(array_key):  
    #         if key == array_key[j]:  
    #             array_num2[j] = value  
    #             break  
    #         else:  
    #             j = j + 1  


    for item in dic2:
        key = item[0]
        value = item[1]
        j = 0
        while j < len(array_key):
            if key == array_key[j]:
                array_num2[j] = value
                break
            else:
                j += 1 


    print array_num1  
    print array_num2  
    print len(array_num1),len(array_num2),len(array_key)  
  
    #计算两个向量的数量积  
    x = 0  
    i = 0  
    while i < len(array_key):  
        x = x + array_num1[i] * array_num2[i]  
        i = i + 1  
    print x  # x^2 + y^2 + z^2 + ...
  
    #计算两个向量的模  
    i = 0  
    sq1 = 0  
    while i < len(array_key):  
        sq1 = sq1 + array_num1[i] * array_num1[i]   # sq1 = sq1 + x^2
        i = i + 1  
    print sq1  # x^2 + y^2 + z^2 + ...
      
    i = 0  
    sq2 = 0  
    while i < len(array_key):  
        sq2 = sq2 + array_num2[i] * array_num2[i]  
        i = i + 1  
    print sq2  
      
    result = float(x) / ( math.sqrt(sq1) * math.sqrt(sq2) )  # cos
    return result  
      


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






if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        port = 8085,
        debug = True
    )
