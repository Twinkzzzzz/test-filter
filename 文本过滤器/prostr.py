import numpy as np
import json

with open('_21_qst_xiaoxue_shuxue_new__202204081055.json','r',encoding='utf-8') as f:
    data = json.load(f,strict=False)
data=data['21_qst_xiaoxue_shuxue_new']

opec = "~!@#$&{}\|'_\n" "0
openc = "\"^[]:;.? " "2
oped = "+-*/×÷()%<>=" "3
dig = "0123456789" "4
cha = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM" "1

def jug(ch):
    if((ch>='a' and ch<='z') or (ch>='A' and ch<='Z')):
        return 1
    if(opec.find(ch)>=0):
        return 0
    if(dig.find(ch)>=0):
        return 4
    if(oped.find(ch)>=0):
        return 3
    if(openc.find(ch)>=0):
        return 2
    return 5

out = open('output.txt','w',encoding='utf-8')
mark = np.zeros(1024)
for item in data:
    s = item['stem']
    mark.fill(0)
    length=len(s)

    for i in range(length):
        ch = s[i];
        mark[i] = jug(ch)

    ss = ""
    for i in range(length):
        tot1 = 0
        tot2 = 0
        tot3 = 0
        for j in range(13):
            if((i + j - 6 >= 0) and (i + j - 6 < length)):
                tot1 += mark[i + j - 6]
            if ((i + j >= 0) and (i + j < length)):
                tot2 += mark[i + j]
            if ((i - j >= 0) and (i - j < length)):
                tot3 += mark[i - j]
        if((mark[i] == 3 and (tot1>18 or tot2>18 or tot3>18)) or (mark[i] > 0 and tot1>18 and tot2>18 and tot3>18)):
            ss+=s[i]
    print(ss)

