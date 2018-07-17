import PyGMO as pg
from PyGMO.problem import base
from PyGMO import *
import numpy as np
import pandas as pd
import Cost
import Constraint
import PRI
import sys
import matplotlib.pyplot as plt
from epanettools import epanet2 as et
from epanettools.epanettools import EPANetSimulation, Node, Link, Network, Nodes, \
    Links, Patterns, Pattern, Controls, Control  # import all elements needed


class my_udp:
    def fitness(self, x):
        from epanettools import epanet2 as et
        from epanettools.epanettools import EPANetSimulation, Node, Link, Network, Nodes, \
            Links, Patterns, Pattern, Controls, Control  # import all elements needed
        d = EPANetSimulation('/home/varsha/Documents/Project.inp')
        f1 = Cost.Cost(x)
        f2 = PRI.PRI(x,d)
        return [f1, f2]

    def get_nobj(self):
        return 2

    def get_bounds(self):
        return ([-4]*2, [4]*2)

    def get_nic(self):
        return 6

    def get_nix(self):

        return 2



from PyGMO import population

d = EPANetSimulation('/home/varsha/Documents/Project.inp')
prob = problem(my_udp())
print (prob)
algo = pg.algorithm.sms_emoa(gen=2000)  # 2000 generations of SMS-EMOA should solve it
pop = population(prob,500)
pop = algo.evolve(pop)

print(prob.objfun(pop.champion.x))
import matplotlib.pyplot as plt
import numpy as np

F = np.array([ind.cur_f for ind in pop]).T
plt.scatter(F[0], F[1])
plt.xlabel("Objective 1")
plt.ylabel("Objective 2")
plt.show()

