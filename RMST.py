# -*- coding: utf-8 -*-
# This file is part of RMST.
#
# Copyright (C) 2019, 
# Alexis Arnaudon (alexis.arnaudon@epfl.ch), 
#https://github.com/FlorianSong/RelaxedMinimumSpanningTree
#
# RMST is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RMST is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RMST.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import networkx as nx
from multiprocessing import Pool
import scipy.sparse as sparse
from functools import partial

def RMST(G, gamma=0.5, weighted = True, n_cpu = 1):
    """
    Networkx wrapper for the RMST code
    Input:
    
    G : networkx graph of similarity
    gamma: RMST parameter
    weighted : return a graph with the original weights
    n_cpu : number of cpu to use in the construction of mlink matrix 
    
    Return: networkX RMST graph
    """

    #get adjacency matrix 
    A = nx.to_numpy_matrix(G)

    #adjacency matrix with large values instead of 0
    A_no_zero = A.copy()
    A_no_zero[A_no_zero == 0] = np.max(A) + 10
    
    #minimum weight vector d_i = min_k z_{i,k}
    d = np.asarray(A_no_zero.min(0))[0]

    #local distribution \gamma(d_i+d_j)
    D =  np.tile(d,(len(d),1))
    local_distribution = gamma*(D + D.T)
    
    #compute the mlink matrix 
    mlink = compute_mlink(G, n_cpu)

    #construct the adjacency matrix of RMST graph
    A_RMST = mlink + local_distribution - A
    A_RMST[A_RMST > 0] = 1. #set positive values to 1
    A_RMST[A_RMST < 0] = 0. #and remove negative values

    if weighted:
        A_RMST = np.multiply(A, A_RMST)    

    #return a networkx Graph
    return nx.Graph(A_RMST)

def compute_mlink(G, n_cpu):
    """construct the mlink matrix"""

    #minimum spannin tree from G
    G_MST = nx.minimum_spanning_tree(G)

    #all shortest paths
    all_shortest_paths = dict(nx.all_pairs_shortest_path(G_MST))

    G_mlink = nx.complete_graph(len(G))
    mlink = np.zeros([len(G), len(G)])


    mlink_f = partial(mlink_func, all_shortest_paths, A)

    with Pool(processes = n_cpu) as p_rmst:  #initialise the parallel computation
        mlink_edges = p_rmst.map(mlink_f, G_mlink.edges()) 

    #convert the output to a matrix
    mlink_edges_dict = dict(zip(G_mlink.edges(), mlink_edges)) 
    nx.set_edge_attributes(G_mlink, mlink_edges_dict, 'weight')
    mlink = nx.to_numpy_matrix(G_mlink)

    return mlink 

def mlink_func(all_shortest_paths, A, e):
    """ compute one entr yof mlink matrix, for parallel computation """

    mlink = 0 
    path = all_shortest_paths[e[0]][e[1]]
    for k in range(len(path)-1):
        mlink = np.max([mlink, A[path[k],path[k+1]]])
    return mlink


