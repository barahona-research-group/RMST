#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 17:42:36 2017

@author: robert
"""
import numpy as np

# A vector (T) with the shortest distance to all nodes.
# After an addition of a node to the network, the vector is updated


def prim2(D):
    LLink = np.zeros(np.shape(D))
    #Number of nodes in the network
    N = np.shape(D)[0]
    #Allocate a matrix for the edge list
    E = np.zeros(np.shape(D))
    allidx = np.arange(0,N,1)
    #Start with a node
    mstidx = np.full(1, 0)
    otheridx = list(set(allidx) - set(mstidx))
    T = D[0,otheridx]
    P = np.zeros((len(T)))
    
    while T.size > 0:
        #print(T.size)
        i = np.argmin(T)
        idx = otheridx[i]
        
        #Start with a node
        E[idx,int(P[i])] = 1
        E[int(P[i]),idx] = 1
        
        	# 1) Update the longest links
        #indexes of the nodes without the parent
        idxremove = np.where(int(P[i])==mstidx)
        tempmstidx = mstidx
        tempmstidx = np.delete(tempmstidx,idxremove)
        
        # 2) update the link to the parent
        LLink[idx,int(P[i])] = D[idx,int(P[i])]
        LLink[int(P[i]),idx] = D[int(P[i]),idx]

        # 3) find the maximal
        tempLLink = np.maximum(LLink[int(P[i]),tempmstidx],D[idx,int(P[i])])
        LLink[idx, tempmstidx] = tempLLink
        LLink[tempmstidx, idx] = tempLLink
        
        # As a node is added clear his entries
        P = np.delete(P,i)
        T = np.delete(T,i)

        # Add the node to the list
        mstidx = np.append(mstidx,idx)
        
        # Remove the node from the list of the free nodes
        otheridx = np.delete(otheridx,i)
        
        #update the distance matrix
        Ttemp = D[idx,otheridx]
        
        if len(T) > 0:
            idxless = np.where(Ttemp < T)
            T[idxless] = Ttemp[idxless]
            P[idxless] = idx;
            
    return E, LLink

#Relaxed Minimum Spanning Tree
#Build a minimum spanning tree from the data
#It is optimal in the sense that the longest link in a path between
# two nodes is the shortest possible
#If a discounted version of the direct distance is shorter than
#longest link in the path - connect the two nodes
#The discounting is based on the local neighborhood around the two nodes
#We can use for example half the distance to the nearest neighbors is used.
    
# Reproduced in python by Robert Peach 05/12/17. Original code in matlab by Mariano Beguerisse 05/11/12
           
def constructNetworkStructure(D, *args):
    
    N = np.shape(D)[0]
    D = np.ones((N,N)) - D # This is because D is a similarity matrix (not a dissimilarity matrix)
    Emst, LLink = prim2(D) 
    
    p = 2.0 # smaller p would make it sparser
    if len(args) > 0:
        p = args[0]
    print(p)
    # Find distance to nearest neighbours
    Dtemp = D + np.eye(N)*np.amax(D)
    mD = np.amin(Dtemp,0)/p
    
    # Check condition
    mDnew = np.matlib.repmat(mD, N, 1)+np.transpose(np.matlib.repmat(mD, N, 1))
    E = np.less((D - mDnew), LLink).astype(int)
    E = E-np.diag(np.diag(E))

    E = np.sign(E)
    E = np.sign(Emst + E)
    
    return E
