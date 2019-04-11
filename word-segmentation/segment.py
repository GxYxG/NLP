#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:19:16 2019

@author: GxY
"""

import re,math
from nltk.probability import FreqDist

#Divide words into ngram parts
def ngram(text,max_gram):
    t1 = [i for i in text]
    loop = len(t1) + 1 - max_gram
    t = []
    for i in range(loop):
        t.append(text[i:i+max_gram])
    if max_gram == 1:
        return t1
    else:
        return t

#Calculate probability of word
def pro(word):
    len_word = len(word)
    total_count = len(word_all[len_word])
    pro = freq_all[len_word][word]/total_count
    return pro

#Calculate left and right entropy
def entropy(alist):
    f = FreqDist(alist)
    ent = (-1) * sum([i/len(alist) * math.log(i/len(alist),2) for i in f.values()])
    return ent

word_all = [0]
freq_all = [0]
word_score = {}
final_word2 = {}
min_entropy = 0.8
min_pro = 2
max_gram = 4
PMI = 10 

with open("/home/gxy/pku_training.utf8","r",encoding = 'utf-8') as f:
    #处理文件
    text = f.read()
    text = text.replace(" ","")
    text = text.replace("\n","")
    
    for i in range(1,max_gram + 1):
        t = ngram(text,i)
        #得到词频字典
        freq = FreqDist(t)
        word_all.append(t)
        freq_all.append(freq)
# =============================================================================
#     for i in range(2,max_gram + 1):
#         for j in word_all[i]:
#             #计算p(x)*p(y)
#             p = min([pro(j[:i]) * pro(j[i:])for i in range(i,len(j))])
#             #if math.log(pro(j)/p) > min_p:
#                 word_score[j] = math.log(pro(j))
# =============================================================================
    #计算互信息MI
    mi = 0
    h = 0
    for e in range(1,len(text) - 1):
        mi_old = mi
        if(len(text[h:e+1]) > 4):
            word_score[text[h:e]] = mi_old
            h = e
            continue
        mi = math.log(pro(text[h:e+1]) / (pro(text[h:e]) * pro(text[e])),2)
        if(mi < PMI):
            word_score[text[h:e]] = mi_old
            h = e
    word_sorted = sorted(zip(word_score.values(),word_score.keys()),reversed = True)
    print(word_sorted[:50])
    
    #计算左右熵
    Candi_words = list(word_score.keys())
    print("len of Candidates is %d"%len(Candi_words))
    for i in Candi_words:
        #提取左右邻接词
        lr = re.findall('(.)%s(.)'%i,text)
        left_entropy = entropy(w[0] for w in lr)
        right_entropy = entropy(w[1] for w in lr)
        word_score += min(left_entropy,right_entropy)
        
    word_sorted = sorted(zip(word_score.values(),word_score.keys()),reversed =  True)
    print(word_sorted[:50])
    
