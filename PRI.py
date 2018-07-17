from epanettools import epanet2 as et
from epanettools.epanettools import EPANetSimulation, Node, Link, Network, Nodes, \
    Links, Patterns, Pattern, Controls, Control  # import all elements needed
import numpy as np
import random

def PRI(x,d,hStar):
    tstep = 1
    h = []
    D = []
    H = []
    Diam = []
    F = []
    R = []
    E = []
    L = []
    b = []
    Prob = []
    bt = []
    data = [[1 ,76.2 ,0.74],[2, 101.6,0.58],[ 3,152.4,0.41],[4,203.2,0.25],[5, 254,0.15],[6,304.8,0.1],[7,355.6,0.08],[8,406.4,0.06],[9,457.2,0.05],\
            [10,508,0.04],[11,609.6,0.03],[12,762,0.025],[13, 914.4, 0.02],[14,1066.8, 0.015],[15,1219.2,0.01],[16,1371.6,0.009],[17,1524,0.008],[18,1625.6,0.007]]

    ret, nnodes = d.ENgetcount(d.EN_NODECOUNT)
    ret, llinks = d.ENgetcount(d.EN_LINKCOUNT)

    Conn = []
    NoConn = []
    h_degree = 0
    for n in range(0, nnodes + 1):
        c = []
        Conn.append(c)

    for i in range(0,(llinks+1)):
        if(i<llinks-1):
            idx = int(round(x[i]))
            Diam.append(data[idx][1])
            para = Link.value_type['EN_DIAMETER']
            d.ENsetlinkvalue(i+1, para, Diam[i])

        nodes = d.ENgetlinknodes(i+1)
        if (nodes[0] == 0):
            Conn[nodes[1]].append(i+1)
            Conn[nodes[2]].append(i+1)
            h_degree = max(len(Conn[nodes[0]]), len(Conn[nodes[1]]), h_degree)

    for idx in range(0,nnodes+1):
        NoConn.append(len(Conn[idx]))
        while(len(Conn[idx])<h_degree):
            Conn[idx].append(0)

    del Conn[0]
    del NoConn[0]

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
        F.append(0)
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
            F[i] = p
            ret, p = d.ENgetlinkvalue(i + 1, d.EN_DIAMETER)
            Diam[i] = p
            ret, p = d.ENgetlinkvalue(i + 1, d.EN_LENGTH)
            L[i] = p
        ret, tstep = d.ENnextH()
    ret = d.ENcloseH()


    Length = np.divide(L, 1000)

    for i in range(0,llinks):
        idx = int(round(x[i]))
        b.append(data[idx][2])
        bt.append(b[i] * np.exp(50 *0.03))
        Prob.append(1 - (np.exp(np.multiply(np.multiply(bt[i],-1),Length[i]))))


    Pl = np.zeros((nnodes,h_degree))
    for i in range(0,nnodes): #12 = no of junctions + reservoir
        for j in range(0,h_degree):
            if Conn[i][j] == 0:
                Pl[i][j] = 0
            else:
                Pl[i][j] = 1 - Prob[(Conn[i][j]-1)]


    Pl = np.transpose(Pl)
    ProbNumer = np.sum(Pl , axis=0)

    ProbNumer = np.transpose(ProbNumer)

    Numer1 = ProbNumer/NoConn
    Numerator = 0
    hStar = [0]*nnodes
    nbofJunctions = 0
    sum = 0
    nodes = d.network.nodes
    for x, y in nodes.items():
        if y.node_type == Node.node_types['RESERVOIR']:
            ret, reser = d.ENgetnodeindex(y.id)
            flow = Conn[reser-1][0]
            sum = sum+ F[flow-1]*H[reser-1]
        elif y.node_type == Node.node_types['JUNCTION']:
            nbofJunctions+=1




    #Flow calculated for all the pipes next to reservoir
    Denomin = np.subtract(sum, np.sum(np.multiply(D, hStar)))

    for i in range(0, nbofJunctions):  # only junctions
            Numerator += Numer1[i] * D[i] * (H[i] - hStar[i])

    y = Numerator / Denomin

    return y
