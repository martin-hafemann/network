import pandas as pd

from pyomo.environ import *
from pyomo.network import *
from pyomo.opt import SolverFactory

import blocks.chp as chp
import blocks.grid as grid


PATH_PRICES = 'data/prices/'
PATH_OUT = 'data/output/'

opt = SolverFactory('gurobi')
# opt.options['nonconvex'] = 2


data = DataPortal()

data.load(
        filename=PATH_PRICES + '/gas_price.csv',
        index='t',
        param='gas_price'
)
data.load(
        filename=PATH_PRICES + '/power_price.csv',
        index='t',
        param='power_price'
)

m = AbstractModel()

# Define sets
m.t = Set(ordered=True)

# Define parameters
m.gas_price = Param(m.t)
m.power_price = Param(m.t)

# Define assets from blocks
m.chp1 = Block(rule=chp.cgu_block_rule)
m.chp2 = Block(rule=chp.cgu_block_rule)
m.power_grid = Block(rule=grid.electrcial_grid_block_rule)
m.gas_grid = Block(rule=grid.gas_grid_block_rule)


def obj_expression(m):
    """ Objective Function """
    return (quicksum(m.gas_grid.gas[t] * m.gas_price[t] for t in m.t) -
            quicksum(m.power_grid.power[t] * m.power_price[t] for t in m.t))


m.obj = Objective(
    rule=obj_expression,
    sense=minimize
    )

# Create instance
instance = m.create_instance(data)

# Define arcs
instance.arc1 = Arc(source=instance.chp1.port_out, destination=instance.power_grid.port_in)
instance.arc2 = Arc(source=instance.chp2.port_out, destination=instance.power_grid.port_in)
instance.arc3 = Arc(source=instance.chp1.port_in, destination=instance.gas_grid.port_out)
instance.arc4 = Arc(source=instance.chp2.port_in, destination=instance.gas_grid.port_out)

TransformationFactory('network.expand_arcs').apply_to(instance)

# Solve the optimization problem
results = opt.solve(
    instance,
    symbolic_solver_labels=True,
    tee=True,
    logfile='data/output/solver.log',
    load_solutions=True)

# Write Results
results.write()

df_variables = pd.DataFrame()
df_parameters = pd.DataFrame()
df_output = pd.DataFrame()

for parameter in instance.component_objects(Param, active=True):
    name = parameter.name
    df_parameters[name] = [value(parameter[t]) for t in instance.t]

for variable in instance.component_objects(Var, active=True):
    name = variable.name
    df_variables[name] = [value(variable[t]) for t in instance.t]

df_output = pd.concat([df_parameters, df_variables], axis=1)

df_output.to_csv('data/output/output_time_series.csv')
