# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 03:41:19 2018

@author: User
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import metrics
import numpy as np
import itertools

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, with little normalization')

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()

pred = 'Bangla_dataset/our_predictions_test.csv'
real = 'Bangla_dataset/our_test_stances.csv'

pred = pd.read_csv(pred)['Stance']
real = pd.read_csv(real)['Stance']

print(pred.head())
print(" ... ")
print(real.head())

print(pred.shape , real.shape)

match = 0

for i in range(pred.shape[0]):
    if(pred[i] == real[i]):
        match += 1

print(match , 'out of' , real.shape[0])

#score = match*100/pred.shape[0]
#print('accuracy : ' , score , '%')
score = metrics.accuracy_score(real, pred)
print("accuracy:   %0.3f" % score)
cm = metrics.confusion_matrix(real, pred, labels=['agree', 'unrelated'])
plot_confusion_matrix(cm, classes=['agree', 'unrelated'])

#for i in range(100):
#    print(real[i] , " ----- " , pred[i])