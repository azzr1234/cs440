# tf_idf_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018
# Modified by Jaewook Yeom 02/02/2020

"""
This is the main entry point for the Extra Credit Part of this MP. You should only modify code
within this file for the Extra Credit Part -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np
import math
from collections import Counter
import time



def compute_tf_idf(train_set, train_labels, dev_set):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    Return: A list containing words with the highest tf-idf value from the dev_set documents
            Returned list should have same size as dev_set (one word from each dev_set document)
    """
    # TODO: Write your code here
    number_of_docs=len(train_labels)
    word_result=[]
    Counter_List=[]
    Dev_Counter_List=[]
    
    #turn every review in training set to list of unique words
    for i in range(0,len(train_labels)):
        train_dict={}
        each_review_train=train_set[i]
        for j in set(each_review_train):
            train_dict[j]=1
        Counter_List.append(train_dict)#Counter list a list of dicts in each review, every dict contains unique words
    #get the dev set data
    Dev_Counter=Counter()
    for i in range(0,len(dev_set)):
        each_review_dev=dev_set[i]
        Dev_Counter+=Counter(each_review_dev)    
    total_num_word=sum(Dev_Counter.values())
    for k in range(0,len(dev_set)):#in each dev document
        each_review_dev=Counter(dev_set[k])
        Dev_Counter_List.append(Counter(each_review_dev))#each element in the list is the counter for 1 article in dev
    for m in Dev_Counter_List:
        result={}
        for j in m.items():
            doc_containing_word=0
            string=j[0]
            frequency=j[1]
            for k in Counter_List:
                doc_containing_word+=k.get(string,0)
            tf_idf_each=(frequency/total_num_word)*math.log(number_of_docs/(1+doc_containing_word))
            result[string]=tf_idf_each
        word_result.append(max(result,key=result.get))
    # return list of words (should return a list, not numpy array or similar)
    return word_result
'''
python mp3_tf_idf.py --training Mp3_data_zip/train --development Mp3_data_zip/dev
'''