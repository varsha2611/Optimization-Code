from platypus import NSGAII, Problem, Integer
import Cost
import PRI
import Constraint
from epanettools.epanettools import EPANetSimulation

class my_mo_problem(Problem):
    d = EPANetSimulation('/home/varsha/Documents/Project.inp')
    ret, nlinks = d.ENgetcount(d.EN_LINKCOUNT)
    def __init__(self):
        super(my_mo_problem, self).__init__(self.nlinks, 2, 2)
        self.types[:] = [Integer(0, 16)]*self.nlinks
        self.constraints[:] = "<=0"
        self.directions[:] = Problem.MINIMIZE

    def evaluate(self, solution):
        y = solution.variables
        solution.objectives[:] = [PRI.PRI(y,self.d),Cost.Cost(y,self.d)]
        solution.constraints[:] = Constraint.Constraint(y,self.d)

