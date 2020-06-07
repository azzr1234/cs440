# neuralnet.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/29/2019

"""
You should only modify code within this file for part 1 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable

class NeuralNet(torch.nn.Module):
    def __init__(self, lrate,loss_fn,in_size,out_size):
        """
        Initialize the layers of your neural network
        @param lrate: The learning rate for the model.
        @param loss_fn: The loss function
        @param in_size: Dimension of input
        @param out_size: Dimension of output
        The network should have the following architecture (in terms of hidden units):
        in_size -> 128 ->  out_size
        """
        super(NeuralNet, self).__init__()
        self.loss_fn = loss_fn
        self.lrate=lrate
        self.in_size=in_size
        self.out_size=out_size
        self.relu1=nn.ReLU(inplace=False)
        self.fc1=nn.Linear(in_size,128)
        #self.fc2=nn.Linear(128,128)
        self.fc3=nn.Linear(128,out_size)
        self.loss_fn=loss_fn
        self.optimizer=optim.SGD(self.get_parameters(), lr=0.01)#weight_decay reflects l2-norm

    def get_parameters(self):
        """ Get the parameters of your network
        @return params: a list of tensors containing all parameters of the network
        """
        return self.parameters()


    def forward(self, x):
        """ A forward pass of your autoencoder
        @param x: an (N, in_size) torch tensor
        @return y: an (N, out_size) torch tensor of output from the network
        """
        x=self.fc1(x)
        x=self.relu1(x)
        x=self.fc3(x)
        x=torch.sigmoid(x)
        #print('x=',x,'shape=',x.shape)
        return x

    def step(self, x,y):
        """
        Performs one gradient step through a batch of data x with labels y
        @param x: an (N, in_size) torch tensor
        @param y: an (N,) torch tensor
        @return L: total empirical risk (mean of losses) at this time step as a float
        """
        L=0.0
        self.optimizer.zero_grad() 
        predict=self.forward(x)
        L=self.loss_fn(predict,y)
        L.backward()
        self.optimizer.step()
        #print('L data',L.data,'with item',L.data.item)
        return L.data.item()

def fit(train_set,train_labels,dev_set,n_iter,batch_size=100):
    """ Fit a neural net.  Use the full batch size.
    @param train_set: an (N, out_size) torch tensor
    @param train_labels: an (N,) torch tensor
    @param dev_set: an (M,) torch tensor
    @param n_iter: int, the number of batches to go through during training (not epoches)
                   when n_iter is small, only part of train_set will be used, which is OK,
                   meant to reduce runtime on autograder.
    @param batch_size: The size of each batch to train on.
    # return all of these:
    @return losses: list of total loss (as type float) at the beginning and after each iteration. Ensure len(losses) == n_iter
    @return yhats: an (M,) NumPy array of approximations to labels for dev_set
    @return net: A NeuralNet object
    # NOTE: This must work for arbitrary M and N
    """
    lrate=1
    in_size=train_set.shape[1]
    out_size=3
    loss_fn=nn.CrossEntropyLoss()
    net=NeuralNet(lrate,loss_fn,in_size,out_size)
    losses=[]
    train_set=(train_set-torch.mean(train_set))/torch.std(train_set)
    for n in range(n_iter):
        for i in range(0,len(train_set),batch_size):
            train_batch=train_set[i:i+batch_size]
            label_batch=train_labels[i:i+batch_size]
            train_input=Variable(train_batch,requires_grad=True)
            label_input=Variable(label_batch)
            L=net.step(train_input,label_input)
        losses.append(L)
    dev_set=(dev_set-torch.mean(dev_set))/torch.std(dev_set)
    dev_set=Variable(dev_set)
    predict=net(dev_set)
    yhats=torch.max(predict,1)[1].numpy()
    print(losses)
    return losses,yhats, net
