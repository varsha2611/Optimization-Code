from epanettools import epanet2 as et
from epanettools.epanettools import Node, Link
import numpy as np
import random
nnodes = 0
llinks = 0
h = []
D = []
H = []
Diam = []
F = []
R = []
E = []
L = []
Conn = []
NoConn = []
data = [[1 ,76.2 ,0.74],[2, 101.6,0.58],[ 3,152.4,0.41],[4,203.2,0.25],[5, 254,0.15],[6,304.8,0.1],[7,355.6,0.08],[8,406.4,0.06],[9,457.2,0.05],\
        [10,508,0.04],[11,609.6,0.03],[12,762,0.025],[13, 914.4, 0.02],[14,1066.8, 0.015],[15,1219.2,0.01],[16,1371.6,0.009],[17,1524,0.008],[18,1625.6,0.007]]

def SetVariables(d):
    global nnodes
    global llinks
    ret,  nnodes = d.ENgetcount(d.EN_NODECOUNT)
    ret, llinks = d.ENgetcount(d.EN_LINKCOUNT)

def Simulation(x,d):
    import time
    start = time.time()

    global nnodes
    global llinks
    global h
    global D
    global H
    global Diam
    global F
    global R
    global E
    global L
    global Conn
    global NoConn
    h_degree = 0
    tstep = 1
    h = [0] * nnodes
    D = [0] * nnodes
    R = [0] * nnodes
    H = [0] * nnodes
    E = [0] * nnodes
    F = [0] * llinks
    L = [0] * llinks
    F = [0] * llinks
    Diam = [0] * llinks

    if(len(Conn) == 0):
        for n in range(0, nnodes + 1):
            c = []
            Conn.append(c)

    for i in range(0, (llinks + 1)):
        if (i < llinks - 1):
            idx = int(round(x[i]))
            Diam[i+1] = data[idx][1]
            para = Link.value_type['EN_DIAMETER']
            d.ENsetlinkvalue(i + 1, para, Diam[i])
        if(len(Conn)== (nnodes+1)):
            nodes = d.ENgetlinknodes(i + 1)
            if (nodes[0] == 0):
                Conn[nodes[1]].append(i + 1)
                Conn[nodes[2]].append(i + 1)
                h_degree = max(len(Conn[nodes[0]]), len(Conn[nodes[1]]), h_degree)


    if(len(Conn) == nnodes+1):
        for idx in range(0, nnodes + 1):
            NoConn.append(len(Conn[idx]))
            while (len(Conn[idx]) < h_degree):
                Conn[idx].append(0)
        del Conn[0]
        del NoConn[0]


    d.ENopenH()
    d.ENinitH(0)
    while tstep > 0:
        ret, t = d.ENrunH()
        for i in range(0, nnodes):
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
        for i in range(0, llinks):
            ret, p = d.ENgetlinkvalue(i + 1, d.EN_FLOW)
            F[i] = p
            ret, p = d.ENgetlinkvalue(i + 1, d.EN_DIAMETER)
            Diam[i] = p
            ret, p = d.ENgetlinkvalue(i + 1, d.EN_LENGTH)
            L[i] = p
        ret, tstep = d.ENnextH()
    ret = d.ENcloseH()
    end = time.time()
    print("time for simulation : " , end-start)

def Res(x,d,hStar):
    Simulation(x,d)
    import time
    start = time.time()
    Numerator = 0
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

    Denomin = np.subtract(sum, np.sum(np.multiply(D, hStar)))

    for i in range(0, nbofJunctions):  # only junctions
            Numerator += D[i] * (H[i] - hStar[i])

    y = Numerator / Denomin
    end = time.time()
    print("Time to calculate Resilience", end-start)
    return y

def Constraint(hStar):
    import time
    start = time.time()
    Delta = []
    for i in range(0, 10):
        Delta.append(H[i] - hStar[i])

    Penalty = []
    for i in range(0, 10):
        if Delta[i] <= 0:
            Penalty.append(Delta[i])
        else:
            Penalty.append(0)

    C = abs(100 * np.sum(Penalty))
    end = time.time()
    print("Time to calculate constraint", end - start)
    return C

def Cost(x,d):
    import time
    start = time.time()
    data = [[1,3],[2,4],[3,6],[4,8],[5,10],[6,12],[7,14],[8,16],[10,20],[11,24],[12,30],[13,36],[14,42],[15,48],[16,54],[17,60],[18,64]]
    c = []
    sum = 0

    #ConnIndex = [[1, 4],[2,6],[3,4],[4,3],[5,6],[6,9],[7,5],[8,6],[9,6],[10,7],[11,5],[12,6],[13,3],[14,7]]
    ret, nlinks = d.ENgetcount(d.EN_LINKCOUNT)
    for i in range(0,nlinks):
        idx = int(round(x[i]))
        ret, p = d.ENgetlinkvalue(i + 1, d.EN_LENGTH)
        c.append(p*3.280841 * data[idx][1]* 10)
        sum = sum + c[i]
    end = time.time()
    print("Time to calculate Cost", end - start)
    return sum