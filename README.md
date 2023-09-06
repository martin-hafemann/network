# General
We consider a model of a two CHPs and network object for the electrical and gas grid using the block component in Pyomo. The CHP's are connected to the grids via Pyomo-Ports and -Arcs and optimized against the electricity market. The cost function, consisting of gas costs and electricity revenues, is minimized.

The construction rule for the CHP and grid blocks are located in the blocks directory.

The results are evaluated in the evaluation.ipynb.

# Pyomo Network
