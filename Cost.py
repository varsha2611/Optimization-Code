import numpy as np
def Cost(x,d):
    print("running Cost")
    data = [[1,3],[2,4],[3,6],[4,8],[5,10],[6,12],[7,14],[8,16],[10,20],[11,24],[12,30],[13,36],[14,42],[15,48],[16,54],[17,60],[18,64]]
    c = []
    sum = 0

    ConnIndex = [[1, 4],[2,6],[3,4],[4,3],[5,6],[6,9],[7,5],[8,6],[9,6],[10,7],[11,5],[12,6],[13,3],[14,7]]
    ret, nlinks = d.ENgetcount(d.EN_LINKCOUNT)
    for i in range(0,nlinks):
        idx = int(round(x[i]))
        ret, p = d.ENgetlinkvalue(i + 1, d.EN_LENGTH)
        c.append(p*3.280841 * data[idx][1]* 10)
        sum = sum + c[i]

    return sum