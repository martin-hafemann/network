## General
We consider a model of a two CHPs and network objects for the electrical and gas grid using the block component in Pyomo. The CHP's are connected to the grids via Pyomo-Ports and -Arcs and optimized against the electricity market. The cost function, consisting of gas costs and electricity revenues, is minimized.

The construction rule for the CHP and grid blocks are located in the blocks directory.

The results are evaluated in the evaluation.ipynb.

## Ports
Pyomo port components have been introduced to link the objects.
The block construction rules for the CHP's have been extended with port components as in- and outlets for the gas required for combustion and the generated electrical power.
The grid objects contain the respective counterpart of the ports of the CHP's.

## Arcs
To connect the defined ports, you have to create pyomo arcs. Each port can have multiple arcs. Because the arcs are connected to the ports of the blocks, the ports have to be initialized in the model for the arc to be created. Therefore the arc initialisation need to take place in a concrete or instanciated abstract model.

After declaration, the arcs have to be expaneded in order to generate the appropriate constraints. Therefore the TransormationFactory is called. For further information, see https://pyomo.readthedocs.io/en/stable/modeling_extensions/network.html#arc-expansion-transformation