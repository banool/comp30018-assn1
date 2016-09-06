#!/usr/local/bin/python

import pickle

#res = [{'numDel': 0, 'tweet': 'listening to Empire State of Mind by Jay-Z & Alicia Keys. Her voice is amazingg!!', 'numSub': 3, 'cost': 1, 'location': 'Zzyzx', 'numIns': 0, 'match': 'jayz '}]

res = pickle.load(open("results.p", "rb"))
#nonExactMatches = pickle.load(open("resultsCostGreaterZero.p", "rb"))


def getAndDumpNonExactMatches():
    def checkCost(item):
        print(item)
        print(type(item))
        return item["cost"] > 0

    nonExactMatches = filter(checkCost, res)

    pickle.dump(nonExactMatches, open("resultsCostGreaterZero.p", "wb"))


print("res:       ", len(res))
#print("non-exact: ", len(nonExactMatches))
#print(nonExactMatches)


from collections import OrderedDict
import csv

with open("results2.csv", "w") as f:
    w = csv.DictWriter(f, res[0].keys())
    w.writeheader()
    w.writerows(res)
