Relaxed Minimum Spanning Tree 
=============================

Python implementation of the Relaxed Minimum Spanning Tree (RMST) algorithm, introduced in
```
Beguerisse-Díaz, Mariano, Borislav Vangelov, and Mauricio Barahona. "Finding role communities in directed networks using role-based similarity, markov stability and the relaxed minimum spanning tree." 2013 IEEE Global Conference on Signal and Information Processing. IEEE, 2013.
```

Installation
------------

To install, have a working python3 environment, and run
```
pip install .
```
This will also install all the necessary dependencies (see setup.py). 

Utilisation
-----------

To use, simply do
```
from RMST import RMST

G_RMST = RMST(G, gamma = 0.5, weighted = True, n_cpu = 1)
```
for a networks graph `G` and a given `gamma` parameter (set to `0.5` by default). A lower value of `gamma` will create a sparser graph (lower bound of zero will give a minimum spanning tree).


The other two parameters are for outputing the weighted or unweighted graph (with the original weights from Hadamard multiplication), and use more cpus to compute the `mlink` matrix. 

See the `test` folder for more details. 
