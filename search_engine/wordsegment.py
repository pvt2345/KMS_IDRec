# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 11:49:12 2018

@author: User
"""
import json
import string
from underthesea import word_tokenize
data=json.load(open('db.json',encoding='UTF-8'))
documents=data['data']['content']
ref=[]
corpus=[]
for document in documents:
    doc_obj=word_tokenize(document['content'],format='text')
    corpus.append(doc_obj)
    ref.append(document['reference'])
with open('vietnamese-stopwords.txt', encoding = 'utf8') as f:
    vietnamese_stopwords = f.read()
vietnamese_stopwords = vietnamese_stopwords.split('\n')
punc_remove = set(string.punctuation)

def clean(doc):
    stop_free = " ".join([i for i in doc.split() if i not in vietnamese_stopwords])
    punc_free = ''.join(ch for ch in stop_free if ch not in punc_remove)
    return punc_free
doc_clean = [clean(d) for d in corpus]

f = open('input.txt', 'w', encoding = 'utf8')
for item in doc_clean:
    f.write(item + '\n')
f.close()
print('success')    