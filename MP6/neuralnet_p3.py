# neuralnet.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/29/2019

"""
This is the main entry point for MP6. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import time
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable

class NeuralNet(torch.nn.Module):
    def __init__(self, lrate, loss_fn, in_size,out_size):
        """
        Initialize the layers of your neural network
        @param lrate: The learning rate for the model.
        @param loss_fn: The loss function
        @param in_size: Dimension of input
        @param out_size: Dimension of output
        """
        super(NeuralNet, self).__init__()
        """
        1) DO NOT change the name of self.encoder & self.decoder
        2) Both of them need to be subclass of torch.nn.Module and callable, like
           output = self.encoder(input)
        """
        self.encoder = nn.Sequential(
            nn.Conv2d(1,16,kernel_size=5,padding=2),
            nn.ReLU(inplace=True),
            nn.Conv2d(16,32,kernel_size=5,padding=2),
            nn.ReLU(inplace=True))
        self.decoder = nn.Sequential(
            nn.Conv2d(32,16,kernel_size=5,padding=2),
            nn.ReLU(inplace=True),
            nn.Conv2d(16,1,kernel_size=5,padding=2),
            nn.ReLU(inplace=True))
        self.loss_fn = loss_fn
        self.optimizer=optim.Adam(self.get_parameters(),lr=lrate, weight_decay=0.01)

    def get_parameters(self):
        """ Get the parameters of your network
        @return params: a list of tensors containing all parameters of the network
        """
        # return self.net.parameters()
        return self.parameters()

    def forward(self, x):
        """ A forward pass of your autoencoder
        @param x: an (N, in_size) torch tensor
        @return xhat: an (N, out_size) torch tensor of output from the network
        """
        x=x.view(len(x),1,28,28)
        out=self.encoder(x)
        out=self.decoder(out)
        #print('out after decoder',out.shape)
        out=out.view(len(out),784)
        return out

    def step(self, x):
        # x [100, 784]
        """
        Performs one gradient step through a batch of data x with labels y
        @param x: an (N, in_size) torch tensor
        @return L: total empirical risk (mean of losses) at this time step as a float
        """
        L=0.0
        self.optimizer.zero_grad()
        predict=self.forward(x)
        L=self.loss_fn(predict,x)
        L.backward()
        self.optimizer.step()
        return L.data.item()

def fit(train_set,dev_set,n_iter,batch_size=100):
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
    #train_set=train_set.view(len(train_set),1,28,28)
    #train_set=(train_set-torch.mean(train_set))/torch.std(train_set)
    out_size=5
    losses=[]
    loss_fn=nn.MSELoss()
    lrate=1E-3
    #lrate=3E-4 #ITER 15 TAKES 590S
    #lrate=4E-4 #17:20 TRIAL
    #lrate=5E-4
    in_size=28*28
    start=time.time()
    net=NeuralNet(lrate,loss_fn,in_size,out_size)
    for n in range(n_iter):
        for i in range(0,len(train_set),batch_size):
            train_batch=train_set[i:i+batch_size]
            train_input=Variable(train_batch,requires_grad=True)
            L=net.step(train_input)
        losses.append(L)
        #print('in iteration number',n,'the loss is',L,losses[-1])
        if n>=1 and (L-losses[-2]>=-1E-3 or L<=0.10 or L-losses[-2]>=0.0005):
            while len(losses)<n_iter:
                losses.append(losses[-1])
            break
    #print('losses list=',losses)
    dev_set=dev_set.view(len(dev_set),1,28,28)
   #dev_set=(dev_set-torch.mean(dev_set))/torch.std(dev_set)
    dev_set=Variable(dev_set)
    predict=net(dev_set)
    #print('predict shape',predict.shape)
    #print('predict result',predict,'max shape',torch.max(predict,1)[1].shape)
    xhats=predict.data.numpy()
    end=time.time()
    return losses,xhats, net
