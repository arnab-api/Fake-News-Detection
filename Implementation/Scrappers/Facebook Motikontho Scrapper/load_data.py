# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 18:10:27 2018

@author: User
"""

import json

with open('news_recent.json') as f:
    news = json.load(f)
#    print(news , type(news))
    
    for id in news:
        print(id , news[id]['title'])
    print(len(news.keys()))
    
with open('comments.json') as f:
    comments = json.load(f)
    print(comments , type(comments))
    
with open('likers.json') as f:
    likers = json.load(f)
    print(likers , type(likers))