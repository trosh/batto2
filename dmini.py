#!/usr/bin/env python3

import json

with open("distances.json", "r") as distfile:
    inputdict = json.load(distfile)

D = inputdict["D"]
names = inputdict["names"]
del inputdict

n = len(D)

startkeys = [k for k in D]

for k1 in startkeys:
    assert n-1 == len(D[k1]), "D must be square matrix"
    startkeysinner = [k for k in D[k1]]
    for k2 in startkeysinner:
        D[k1][int(k2)] = D[k1][k2]
        del D[k1][k2]
    D[int(k1)] = D[k1]
    del D[k1]

active = [k for k in D]

while n > 2:
    mind = float("inf")
    a = 0
    b = 0
    for k1 in active:
        for k2 in active:
            if k2 in D[k1] and D[k1][k2] < mind:
                mind = D[k1][k2]
                a = k1
                b = k2
    x = -n # composite object id
    D[x] = {"children": (a, b)}
    active.remove(a)
    active.remove(b)
    for k in active:
        if a in D[k] and b in D[k]:
            D[k][x] = min(D[k][a], D[k][b])
        if k in D[a] and k in D[b]:
            D[x][k] = min(D[a][k], D[b][k])
    active.append(x)
    n -= 1

def getstring(k, otherk):
    if "children" in D[k]: # is composite
        child0 = D[k]["children"][0]
        child1 = D[k]["children"][1]
        return "(%s,%s):%f" % \
            (getstring(child0, child1),
             getstring(child1, child0),
             D[k][otherk] - D[child0][child1])
    else: # is real object
        name = names[str(k)]
        name = name[:name.find(",")]
        return "%s:%f" % (name, D[k][otherk])

print("(%s,%s);" % \
      (getstring(active[0], active[1]),
       getstring(active[1], active[0])))
