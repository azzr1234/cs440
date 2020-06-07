# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018
# Modified by Jaewook Yeom 02/02/2020
    
"""
This is the main entry point for Part 1 of MP3. You should only modify code
within this file for Part 1 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as numpy
import math
from collections import Counter




def naiveBayes(train_set, train_labels, dev_set, smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter you provided with --laplace (1.0 by default)

    pos_prior - positive prior probability (between 0 and 1)
    """
    # TODO: Write your code here
    Postive_Counter=Counter()
    Negative_Counter=Counter()
    Dev_Counter=Counter()
    len_positive=0
    len_negative=0
    result=[]
    for i in range(0,len(train_labels)):
        if train_labels[i]==1:#positive label
            each_review_positive=train_set[i]
            Postive_Counter+=Counter(each_review_positive)
            len_positive+=1
        if train_labels[i]==0:#negative label
            each_review_negative=train_set[i]
            Negative_Counter+=Counter(each_review_negative)
            len_negative+=1
    #get each 
    N_positive=sum(Postive_Counter.values())#follow the notation in MP3 document
    N_negative=sum(Negative_Counter.values())
    ###get the words in the dev_set
    for i in range(0,len(dev_set)):
        Positive_Likelihood=0
        Negative_Likelihood=0
        Dev_Counter=Counter()
        each_review_dev=dev_set[i]
        Dev_Counter+=Counter(each_review_dev)
        for i in Dev_Counter.items():
            string=i[0]
            frequency=i[1]
            Positive_Likelihood+=math.log10((Postive_Counter.get(string,0)+smoothing_parameter)/(N_positive+smoothing_parameter*frequency))
            Negative_Likelihood+=math.log10((Negative_Counter.get(string,0)+smoothing_parameter)/(N_negative+smoothing_parameter*frequency))
        if Positive_Likelihood+math.log10(pos_prior)>Negative_Likelihood+math.log10(1-pos_prior):
            result.append(1)
        if Positive_Likelihood+math.log10(pos_prior)<Negative_Likelihood+math.log10(1-pos_prior):
            result.append(0)
        if Positive_Likelihood+math.log10(pos_prior)==Negative_Likelihood+math.log10(1-pos_prior):
            #use random number to judge if it falls to Positive / Negative
            A=numpy.random.random([1])
            if A[0]>=0.5:
                result.append(1)
            else:
                result.append(0)
    # return predicted labels of development set (make sure it's a list, not a numpy array or similar)
    return result

'''
python mp3.py --training MP3_data_zip/train --development MP3_data_zip/dev --stemming False --lower_case True --laplace 0.1 --pos_prior 0.8
'''