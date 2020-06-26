#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 12:51:44 2020

@author: igm
"""
from googletrans import Translator
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords
  
lemmatizer = WordNetLemmatizer() 
stop_words = set(stopwords.words('english'))

translator = Translator()

def replace_punct(url):
    return url.replace('/',' ').replace('-',' ').replace('_',' ').replace('.',' ')



def lem_url(url):
    #url is str (but without ponctuation)
    #return lst of str but lemmatizé
    translated = translator.translate(url, dest='en')
    words = translated.text.lower().split()
    #print(words)

    clean=[] 
    for w in words:
        if w not in stop_words:
            clean.append(lemmatizer.lemmatize(w))
    return clean

#url1_clean = lem_url(url1)
#url2_clean = lem_url(url2)

def comparison(url_original,url):
    url_original_clean = lem_url(replace_punct(url_original))
    url_clean = lem_url(replace_punct(url))
    length = max(len(url_original_clean),len(url_clean))
    intersection = set(url_original_clean) & set(url_clean)
    intersection_length = len(intersection)
    if intersection_length / length >=0.7:
        return True
    return False



