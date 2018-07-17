from epanettools import epanet2 as et
from epanettools.epanettools import EPANetSimulation, Node, Link, Network, Nodes, \
    Links, Patterns, Pattern, Controls, Control  # import all elements needed

def get_Data(d):
    ret, nnodes = d.ENgetcount(d.EN_NODECOUNT)
    Conn = []
    length = []
    for n in range(0,nnodes+1):
        x = []
        Conn.append(x)
    ret,nlinks = d.ENgetcount(d.EN_LINKCOUNT)
    h_degree = 0
    for index in range(0, nlinks+1):
        nodes = d.ENgetlinknodes(index)
        if(nodes[0] == 0):
            Conn[nodes[1]].append(index)
            Conn[nodes[2]].append(index)
            h_degree = max(len(Conn[nodes[0]]),len(Conn[nodes[1]]),h_degree)
            length.append(d.ENgetlinkvalue(index, d.EN_LENGTH))

    NoConn = []
    for idx in range(0,nnodes+1):
        NoConn.append(len(Conn[idx]))
        while(len(Conn[idx])<h_degree):
            Conn[idx].append(0)

    ResFlowPair = []
    nodes = d.network.nodes
    for x, y in nodes.items() :
        if y.node_type == Node.node_types['RESERVOIR']:
            ret, r = d.ENgetnodeindex(y.id)
            f = Conn[r][0]
            ResFlowPair.append([f,r])


    return length, Conn, NoConn, ResFlowPair