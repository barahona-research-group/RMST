import numpy as np
import networkx as nx
from multiprocessing import Pool
import scipy.sparse as sparse
from functools import partial

def RMST(G, gamma=0.5, n_cpu = 1):
    """
    Networkx wrapper for the RMST code
    Input:
    
    G : networkx graph of similarity
    gamma: RMST parameter
    
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
    
    #minimum spannin tree from G
    G_MST = nx.minimum_spanning_tree(G)
    
    #all shortest paths
    all_shortest_paths = dict(nx.all_pairs_shortest_path(G_MST))

    #construct the mlink matrix 
    G_mlink = nx.complete_graph(len(G))
    mlink = np.zeros([len(G), len(G)])

    if n_cpu == 1:  #if only one cpu, just do a loop
        for i,j in G_mlink.edges():
            path = all_shortest_paths[i][j]
            for k in range(len(path)-1):
                 mlink[i,j] = np.max([mlink[i,j], A[path[k],path[k+1]]])

    else: #else use multiprocessing 

        mlink_f = partial(mlink_func, all_shortest_paths, A)

        with Pool(processes = n_cpu) as p_rmst:  #initialise the parallel computation
            mlink_edges = p_rmst.map(mlink_f, G_mlink.edges()) 
        
        #convert the output to a matrix
        mlink_edges_dict = dict(zip(G_mlink.edges(), mlink_edges)) 
        nx.set_edge_attributes(G_mlink, mlink_edges_dict, 'weight')
        mlink = nx.to_numpy_matrix(G_mlink)

    #construct the adjacency matrix of RMST graph
    A_RMST = mlink + local_distribution - A
    A_RMST[A_RMST > 0] = 1. #set positive values to 1
    A_RMST[A_RMST < 0] = 0. #and remove negative values
    
    #return a networkx Graph
    return nx.Graph(A_RMST)

def mlink_func(all_shortest_paths, A, e):
    mlink = 0 
    path = all_shortest_paths[e[0]][e[1]]
    for k in range(len(path)-1):
        mlink = np.max([mlink, A[path[k],path[k+1]]])
    return mlink


