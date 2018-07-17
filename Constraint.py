from epanettools import epanet2 as et
from epanettools.epanettools import EPANetSimulation, Node, Link, Network, Nodes, \
    Links, Patterns, Pattern, Controls, Control  # import all elements needed
import numpy as np

def Constraint(x, d,hStar):
    print("running Constraint")
    tstep = 1
    h = []
    D = []
    H = []
    Diam = []
    q = []
    R = []
    E = []
    L = []

    data = [[1 ,76.2 ],[2, 101.6],[ 3,152.4],[4,203.2],[5, 254],[6,304.8],[7,355.6],[8,406.4],[9,457.2],\
                [10,508],[11,609.6],[12,762],[13, 914.4],[14,1066.8],[15,1219.2],[16,1371.6],[17,1524],[18,1625.6]]

    ret, nnodes = d.ENgetcount(d.EN_NODECOUNT)
    ret, llinks = d.ENgetcount(d.EN_LINKCOUNT)
    for i in range(0, llinks): # change
        idx = (x[i])
        Diam.append(data[idx][1])
        # d.ENsetlinkvalue(i, 0, Diam[i])
        para = Link.value_type['EN_DIAMETER']
        d.ENsetlinkvalue(i + 1, para, Diam[i])

    nodes = []
    links = []

    for index in range(0, nnodes):
        ret, t = d.ENgetnodeid(index)
        nodes.append(t)
        h.append(t)
        D.append(t)
        R.append(t)
        H.append(t)
        E.append(t)

    for index in range(0, llinks):
        q.append(0)
        Diam.append(0)
        L.append(0)
        links.append(index)

    d.ENopenH()
    d.ENinitH(0)
    while tstep > 0:
        ret, t = d.ENrunH()
        for i in range(0, len(nodes)):
            ret, p = d.ENgetnodevalue(i + 1, d.EN_PRESSURE)
            h[i] = p
            ret, p = d.ENgetnodevalue(i + 1, d.EN_DEMAND)
            D[i] = p
            ret, p = d.ENgetnodevalue(i + 1, d.EN_BASEDEMAND)
            R[i] = p
            ret, p = d.ENgetnodevalue(i + 1, d.EN_HEAD)
            H[i] = p
            ret, p = d.ENgetnodevalue(i + 1, d.EN_ELEVATION)
            E[i] = p
        for i in range(0, len(links)):
            ret, p = d.ENgetlinkvalue(i + 1, d.EN_FLOW)
            q[i] = p
            ret, p = d.ENgetlinkvalue(i + 1, d.EN_DIAMETER)
            Diam[i] = p
            ret, p = d.ENgetlinkvalue(i + 1, d.EN_LENGTH)
            L[i] = p
        ret, tstep = d.ENnextH()
    ret = d.ENcloseH()

    Delta = []
    for i in range(0,10):
        Delta.append(H[i] - hStar[i])

    Penalty = []
    for i in range(0,10):
        if Delta[i] <= 0:
            Penalty.append(Delta[i])
        else:
            Penalty.append(0)


    C = abs(100 * np.sum(Penalty))
    return C





