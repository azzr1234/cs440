# classify.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/27/2018
# Extended by Daniel Gonzales (dsgonza2@illinois.edu) on 3/11/2018

"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.

train_set - A Numpy array of 32x32x3 images of shape [7500, 3072].
            This can be thought of as a list of 7500 vectors that are each
            3072 dimensional.  We have 3072 dimensions because there are
            each image is 32x32 and we have 3 color channels.
            So 32*32*3 = 3072. RGB values have been scaled to range 0-1.
[[] []...7500 of length 3072 array] np array
[True False...]

train_labels - List of labels corresponding with images in train_set
example: Suppose I had two images [X1,X2] where X1 and X2 are 3072 dimensional vectors
         and X1 is a picture of a dog and X2 is a picture of an airplane.
         Then train_labels := [1,0] because X1 contains a picture of an animal
         and X2 contains no animals in the picture.

dev_set - A Numpy array of 32x32x3 images of shape [2500, 3072].
          It is the same format as train_set
"""
import numpy as np
import math
from collections import Counter
def trainPerceptron(train_set, train_labels, learning_rate, max_iter):
    # TODO: Write your code here
    # return the trained weight and bias parameters 
    #initialization of W,b
    length=len(train_set[0])#training data length
    W=np.full((length+1,),0.0)#should give (3072+1,) shape of elements 1array combining b into the w weight
    #adding 1 to each feature 
    #iterations=0
    i=1
    for k in range(0,max_iter):
        for index in range(0,len(train_labels)):
            element=np.append(train_set[index],1)
            y_predict=np.sign(np.dot(W,element))# each element append 1 at the end
            target=True if (y_predict>0) else False#>0 show better result on cmd
            if target==train_labels[index]:
                continue
            else:
                y=1 if (train_labels[index]==True) else -1
                W+=learning_rate*y*element
                #adding result is correct at 19:33 4/1
    b=W[-1]
    W=W[0:-1]
    return W, b

def classifyPerceptron(train_set, train_labels, dev_set, learning_rate, max_iter):
    # TODO: Write your code here
    # Train perceptron model and return predicted labels of development set
    W,b=trainPerceptron(train_set,train_labels,learning_rate,max_iter)
    result=[]
    for each_data_element in dev_set:
        yhat=np.sign(np.dot(W,each_data_element)+b)
        if yhat>=0:
            result.append(True)
        else:
            result.append(False)        
    return result

def sigmoid(x):
    # TODO: Write your code here
    # return output of sigmoid function given input x
    s=1/(1+math.exp(-1*x))
    return s

def trainLR(train_set, train_labels, learning_rate, max_iter):
    # TODO: Write your code here
    # return the trained weight and bias parameters 
    length=len(train_set[0])#training data length
    W=np.full((length+1,),1)
    iterations=0
    while iterations<max_iter:
        for index in range(0,len(train_labels)):
            element=np.append(train_set[index],1)
            #print('input to sigmoid=',np.dot(element,W))
            cal=round(sigmoid(np.dot(element,W)))#input W*X 
            y_predict=True if (cal==1) else False
            if y_predict==train_labels[index]:
                continue
            else:
                #gradient descent following the formula of https://math.stackexchange.com/questions/2503428/derivative-of-binary-cross-entropy-why-are-my-signs-not-right/2503773
                y=1 if (train_labels[index]==True) else 0
                #print('y=',y,'cal=',cal)
                W=np.subtract(W,element*(cal-y)*learning_rate)    
        iterations+=1
    b=W[-1]
    W=W[0:-1]
    return W, b

def classifyLR(train_set, train_labels, dev_set, learning_rate, max_iter):
    # TODO: Write your code here
    # Train LR model and return predicted labels of development set
    W,b=trainLR(train_set,train_labels,learning_rate,max_iter)
    result=[]
    for each_data_element in dev_set:
        yhat=round(sigmoid(np.dot(W,each_data_element)+b))
        if yhat>=0.5:
            result.append(True)
        else:
            result.append(False)
    return result
def distance(a1,a2):
    return np.linalg.norm(a1-a2)
def Voter(X):
    C=Counter(X)
    if len(C)>1:
        Voter=C.most_common(2)
        frequency1=Voter[0][1]
        frequency2=Voter[1][1]
        if frequency1==frequency2:#there is a tie
            return  False
        else:
            return True if (Voter[0][0]==1) else False
    else:
        return True if (C.most_common(1)[0][0]==1) else False


def classifyEC(train_set, train_labels, dev_set, k):
    # Write your code here if you would like to attempt the extra credit
    iterations=0
    result=[]
    for each_element in dev_set:        
        distance_array=np.empty([len(train_set),])
        label_array=np.empty([len(train_set),])
        length_k_array=[0]
        for index in range(0,len(train_set)):
            train_element=train_set[index]
            distance_array[index]=distance(each_element,train_element)
            label_array[index]=train_labels[index]
        min_index=np.where(distance_array==np.min(distance_array))   
        if len(min_index)>=k:
            length_k_array=label_array[min_index[0:k]]
            #print('length_k_array in >=k case',length_k_array)
            result.append(Voter(length_k_array))
        else:
            length_k_array=label_array[min_index]
            while len(length_k_array)<k:
                distance_array=np.delete(distance_array,min_index)
                label_array=np.delete(label_array,min_index)
                min_index=np.where(distance_array==np.min(distance_array))  
                #print(min_index)
                if len(min_index)>=k-len(length_k_array):
                    #print('second case-1 before',length_k_array,'added contents=',label_array[min_index])
                    length_k_array=np.append(length_k_array,label_array[min_index])[0:k]
                    #print('second case-1 after',length_k_array[0:k],len(length_k_array))
                else:
                    #print('second case-2 before',length_k_array,'added contents=',label_array[min_index])
                    length_k_array=np.append(length_k_array,label_array[min_index])
                    #print('second case-2 after',length_k_array)
            result.append(Voter(length_k_array))
    #print(result)
    return  result
#python mp5.py --dataset mp5_data