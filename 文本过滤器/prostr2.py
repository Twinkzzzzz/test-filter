from __future__ import unicode_literals
import numpy as np
import json

with open('_21_qst_xiaoxue_shuxue_new__202204081055.json','r',encoding='utf-8') as f:
    data = json.load(f,strict=False)
data=data['21_qst_xiaoxue_shuxue_new']
f.close()

with open('dicpre.json','r',encoding='utf-8') as f:
    repdic = json.load(f,strict=False)
f.close()

with open('dic.json','r',encoding='utf-8') as f:
    chndic = json.load(f,strict=False)
f.close()

oped = "+-*×÷%=/\"^:;,.? ~!|'_"
lope = "@$\#&\n\t"
dig = "0123456789０１２３４５６７８９º¹²³⁴⁵⁶⁷⁸⁹"
cha = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNMａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"
lstope = "，。？！：、；…-:;,.? ~!|'_/"

def clas(ch):
    if (ch == '('):
        return 1
    elif (ch == ')'):
        return 9
    elif (ch == '['):
        return 2
    elif (ch == ']'):
        return 8
    elif (ch == '{'):
        return 3
    elif (ch == '}'):
        return 7
    elif (ch == '<'):
        return 4
    elif (ch == '>'):
        return 6
    elif (cha.find(ch) >= 0 or dig.find(ch) >= 0 or oped.find(ch) >= 0):
        return 10
    elif (lope.find(ch) >= 0):
        return 11
    else:
        return 0

def process(str):
    length = len(str)
    tmp = ""
    list = [] #存储分割出的有用片段
    cat = 0 #当前片段的分类号
    precat = 0 #前一个片段的分类号
    stk = [] #括号匹配用的stack
    for i in range(length):
        ch = str[i]
        if (ch == ' '):
            continue
        cat = clas(ch)
        if (precat == (-1)):
            precat = cat
        if (cat >= 1 and cat <= 4):
            if (len(stk) == 0):
                if (tmp != ""):
                    list.append(tmp)
                tmp = ch
                stk.append(cat)
            else:
                stk.append(cat)
                tmp = tmp + ch
        elif (cat >= 6 and cat <= 9):
            if (len(stk) > 0 and stk[-1] + cat == 10):
                del stk[-1]
            tmp = tmp + ch
            if (len(stk) == 0):
                list.append(tmp)
                tmp = ""
                precat = -1
        elif (cat == 10):
            tmp = tmp + ch
        elif (cat == 11):
            if (precat == 11 or len(stk) > 0):
                tmp = tmp + ch
            else:
                if (tmp != ""):
                    list.append(tmp)
                    tmp = ch
                precat = 11
        else:
            if (precat != 0 and precat != 10 and len(stk) == 0):
                if (tmp != ""):
                    list.append(tmp)
                    tmp = ch
                precat = cat
            else:
                tmp = tmp + ch
    if (tmp != ""):
        list.append(tmp)
    return list

filelist = open('test(divided).json',"w",encoding='utf-8')
filefilt = open('test(filtered).json',"w",encoding='utf-8')

i = 0
ultilist = []
stlist = []
dict = {}

for item in data:
    id = item['id']
    #qid = item['questionId']
    s = item['stem'] #提取的题目内容字符串（有噪声）
    for ts in repdic.keys():
        s = s.replace(ts,repdic[ts])
    list = process(s) #list中储存所有有用的片段

    dict = {'id': id, 'content': str(list)}  # 'questionid': qid
    stlist.append(dict)

    filt = ""
    for tmp in list:
        cat = clas(tmp[0])
        if (cat == 0 or cat == 10):
            filt = filt + tmp
    # 把符号汉化
    i = 0
    while(i < len(filt)):
        ch = filt[i]
        if ((ch == '-') or (ch == '－') or (ch == '−') or (ch == '—') or (ch == '﹣')):
            if (i == 0):
                filt = '负' + filt[1:]
            elif (i == len(filt) - 1):
                filt = filt[:i-1] + '减'
            else:
                if (clas(filt[i-1]) == 10 and clas(filt[i+1]) == 10):
                    filt = filt[:i] + '减' + filt[i+1:]
                else:
                    filt = filt[:i] + '负' + filt[i+1:]
        elif (ch == ':' or ch == '：'):
            if (i > 0 and i < (len(filt) - 2) and dig.find(filt[i-1]) >= 0 and dig.find(filt[i+1]) >= 0 and dig.find(filt[i+2]) >= 0):
                filt = filt[:i] + '时' + filt[i+1:]
        elif (ch == '%' or ch == '％'):
            j = i - 1
            while ((dig.find(filt[j]) >= 0 or filt[j] == '.') and j >= 0):
                j = j - 1
            if (j < 0):
                filt = '百分之' + filt[:i] + filt[i+1:]
            else:
                filt = filt[:j+1] + '百分之' + filt[j+1:i] + filt[i+1:]
        elif (ch == 'm'):
            if (i > 0 and (dig.find(filt[i-1]) > 0 or filt[i-1] == ')' or filt[i-1] == '）')):
                filt = filt[:i] + '米' + filt[i+1:]
        elif (ch == 'g'):
            if (i > 0 and (dig.find(filt[i-1]) > 0 or filt[i-1] == ')' or filt[i-1] == '）')):
                filt = filt[:i] + '克' + filt[i+1:]
        elif (ch == '×' or ch == '*' or ch == '＊'):
            if (i > 0 and i < len(filt) - 1 and (dig.find(filt[i-1]) >= 0 or cha.find(filt[i-1]) >= 0) and (dig.find(filt[i+1]) >= 0 or cha.find(filt[i+1]) >= 0)):
                filt = filt[:i] + '乘' + filt[i + 1:]
            else:
                filt = filt[:i] + '叉' + filt[i + 1:]
        i = i + 1
    for ts in chndic.keys():
        filt = filt.replace(ts,chndic[ts])
    #把符号汉化结束,处理数据信息
    st = -1
    i = 0
    while (i < len(filt)):
        ch = filt[i]
        if (dig.find(ch) >= 0 or (ch == '.' and st != -1)):
            if (st == -1):
                st = i
        else:
            if (st != -1):
                filt = filt[:st] + '[数据]' + filt[i:]
                i = st + 3
                st = -1
        i = i + 1
    if (st != -1):
        filt = filt[:st] + '[数据]'
        st = -1
    #把数据用中文符号代替结束
    i = 0
    st = -1
    while (i < len(filt)):
        ch = filt[i]
        if (cha.find(ch) >= 0): #and (i == 0 or (i > 0 and cha.find(filt[i-1]) == -1)) and (i == len(filt) - 1 or (i < len(filt) - 1 and cha.find(filt[i+1]) == -1))):
            if (st == -1):
                st = i
        else:
            if (st != -1):
                if (st == i - 1):
                    filt = filt[:st] + '[变量]' + filt[i:]
                    i = st + 3
                    st = -1
                else:
                    filt = filt[:st] + '[条件量]' + filt[i:]
                    i = st + 4
                    st = -1
        i = i + 1
    if (st != -1):
        filt = filt[:st] + '[条件量]'
        st = -1
    #变量和条件用中文处理结束
    i = 0
    while (i < len(filt)):
        ch = filt[i]
        if (lstope.find(ch) >= 0):
            if ((i < len(filt) - 1 and lstope.find(filt[i + 1])) >= 0): #or ((i == 0 or lstope.find(filt[i-1]) >= 0) and (i == len(filt) - 1 or lstope.find(filt[i+1]) >= 0))):
                filt = filt[:i] + filt[i+1:]
                i = i - 1
        i = i + 1

    if (filt != ''):
        dict = {'id': id, 'content': filt}  # 'questionid':qid
        ultilist.append(dict)
    print(id)

data = json.dumps(ultilist,ensure_ascii=False,indent=4)
filefilt.write(data)

data = json.dumps(stlist,ensure_ascii=False,indent=4)
filelist.write(data)

filelist.close()
filefilt.close()