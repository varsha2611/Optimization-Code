from platypus import NSGAII, Problem, Integer
import Functions
import Settings
from epanettools.epanettools import EPANetSimulation,Node, Link
class my_mo_problem(Problem):
    d = EPANetSimulation('/home/varsha/Documents/water networks/d-town.inp')
    ret, nlinks = d.ENgetcount(d.EN_LINKCOUNT)
    hStar = Settings.SetValues(d)
    Functions.SetVariables(d)
    def __init__(self):
        super(my_mo_problem, self).__init__(self.nlinks, 2, 2)
        self.types[:] = [Integer(0, 16)]*self.nlinks
        self.constraints[:] = "<=0"
        self.directions[:] = Problem.MINIMIZE
    def evaluate(self, solution):
        y = solution.variables
        solution.objectives[:] = [-Functions.Res(y,self.d,self.hStar),Functions.Cost(y,self.d)]
        solution.constraints[:] = Functions.Constraint(self.hStar)

