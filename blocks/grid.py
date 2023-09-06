import pandas as pd
from pyomo.environ import *
from pyomo.network import *

# Get input parameters for the electrical net
data = pd.read_csv(
    'data/assets/electrical_grid.csv',
    index_col=0
)


def electrcial_grid_block_rule(block):
    """Rule for creating a electrical power grid block with default components and 
    constraints."""
    # Get index from model
    t = block.model().t

    # Define components
    block.power = Var(t, domain=NonNegativeReals)

    block.port_in = Port(initialize={'power': (block.power, Port.Extensive)})


    # Define construction rules for constraints
    def power_max_rule(_block, i):
        power_max = data.loc['Max', 'Power']

        return _block.power[i] <= power_max
    

    # Define constraints
    block.power_max_constraint = Constraint(
        t,
        rule=power_max_rule
        )
    


def gas_grid_block_rule(block):
    t = block.model().t

    block.gas = Var(t, domain=NonNegativeReals)

    block.port_out = Port(initialize={'gas': (block.gas, Port.Extensive)})