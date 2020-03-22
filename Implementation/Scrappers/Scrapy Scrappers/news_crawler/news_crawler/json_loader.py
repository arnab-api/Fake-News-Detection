
# -*- coding: utf-8 -*-
import json

file_name = 'ittefaq.json' 
with open(file_name) as f:
    news = json.load(f)
    print("{} loaded successfully".format(file_name) , ":: {} articles".format(len(news)))
    type(news)
    type(news[0])
    
    for i in range(5):
        print(" -----> " , news[i]['headline'])
        print(news[i]['body'])
    