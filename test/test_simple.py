import networkx as nx
import numpy as np
import pylab as plt
import scipy as sc

from RMST import RMST

#create a graph from a random matrix
A = np.random.uniform(.1,5,[20,20])
A += A.T

G = nx.Graph(A)

plt.figure()
pos = nx.spring_layout(G,weight=None,scale=1)

nx.draw(G, pos=pos, node_size=50, width = 0.5*np.array([G[i][j]['weight'] for i,j in G.edges]))
plt.title('original graph')
plt.savefig('original_graph.png')

# comput MST graph 
G_MST = nx.minimum_spanning_tree(G)

plt.figure()
nx.draw(G_MST, pos=pos,width = 2, node_size=50)
plt.title('MST')
plt.savefig('MST_graph.png')

#compute RMST graph
G_RMST = RMST(G, gamma = 0.5)

plt.figure()
nx.draw(G_RMST, pos=pos,width = 2, node_size=50)
plt.title('RMST')
plt.savefig('RMST_graph.png')

plt.show()

