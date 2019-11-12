Relaxed Minimum Spanning Tree 
=============================

Python implementation of the Relaxed Minimum Spanning Tree  (RMST) algorithm. 

To install 
```
pip install .
```

To use, 
```
from RMST import RMST

G_RMST = RMST(G, gamma = 0.5, weighted = True, n_cpu = 1)

```
for a networks graph `G` and a given `gamma` parameter (set to `0.5` by default). 
The other two parameters are for outputing the weighted or unweighted graph (with the original weights from Hadamard multiplication), and use more cpus to compute the `mlink` matrix. 

See the `test` folder for more details. 
