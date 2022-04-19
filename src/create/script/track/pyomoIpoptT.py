#!/usr/bin/python
# coding=gbk

from pyomo.environ import * 
path = '~/vscode_ros/3rd_party/ipopt-linux64/ipopt' 


model = ConcreteModel()

# define model variables
# domain = Reals(Default) / NonNegativeReals Binary
model.x1 = Var(domain=Reals)
model.x2 = Var(domain=Reals)
# define objective function
# sense = minimize(Default) / maximize 
model.f = Objective(expr = model.x1**2 + model.x2**2, sense=minimize)
# define constraints, equations or inequations 
model.c1 = Constraint(expr = -model.x1**2 + model.x2 <= 0)
model.ceq1 = Constraint(expr = model.x1 + model.x2**2 == 2)
# use 'pprint' to print the model information 
model.pprint()
SolverFactory('ipopt', executable=path).solve(model).write()
print('optimal f: {:.4f}'.format(model.f()))
print('optimal x: [{:.4f}, {:.4f}]'.format(model.x1(), model.x2()))