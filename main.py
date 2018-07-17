from platypus import NSGAII, Problem, Integer
import CustomProblem

algorithm = NSGAII(CustomProblem.my_mo_problem())
algorithm.run(2000)

feasible_solutions = [s for s in algorithm.result if s.feasible]

# plot the results using matplotlib
import matplotlib.pyplot as plt

plt.scatter([s.objectives[0] for s in feasible_solutions],
            [s.objectives[1] for s in feasible_solutions])
plt.xlabel("$PRI(x)$")
plt.ylabel("$Cost(x)$")
plt.show()
