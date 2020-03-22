# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 23:35:32 2018

@author: User
"""

import json

f = open('fake_moti.json')
dct = json.load(f)
print(dct)

print(dct[0])

print(len(dct))
for i in range(len(dct)):
    print(dct[i]['headline'])