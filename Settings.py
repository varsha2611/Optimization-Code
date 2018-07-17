from epanettools.epanettools import EPANetSimulation,Node, Link
import random
def SetValues(d):
    MinHead = [30.18, 25.61, 27.61, 32.22, 32.22, 32.22, 32.22, 32.22, 32.22, 32.22]
    ret, nnodes = d.ENgetcount(d.EN_NODECOUNT)
    hStar = [0]*nnodes
    nodes = d.network.nodes
    nbofJunctions = 0
    for x, y in nodes.items():
        if y.node_type == Node.node_types['JUNCTION']:
            hStar[nbofJunctions] = random.choice(MinHead)
            nbofJunctions += 1

    return hStar
