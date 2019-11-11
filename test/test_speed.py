import networkx as nx
import numpy as np
import pylab as plt
import scipy as sc

from RMST import RMST
import time as time
from tqdm import tqdm 

#create a graph from a random matrix
n = 20
def test_RMST(n):
    t0 = time.time()
    A = np.random.uniform(.1,5,[n, n])
    A += A.T

    G = nx.Graph(A)

    #compute RMST graph
    G_RMST = RMST(G, gamma = 0.5, n_cpu = 1)

    return time.time()-t0

K = 2
times = []
Ns = np.arange(20, 220, 20)
print(Ns)
for n in tqdm(Ns):
    times_tmp = []
    for k in range(K):
        times_tmp.append(test_RMST(n))

    times.append(np.mean(times_tmp))

plt.figure(figsize=(6,5))
plt.loglog(Ns, times, '+')
plt.xlabel('number of nodes')
plt.ylabel('computational time')
plt.savefig('speed_test.png')
plt.show()
