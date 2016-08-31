#!/usr/local/bin/python

"""
Uses the TRE library. Fetch it by following the instructions here:
http://laurikari.net/tre/download/
(so just do this): sudo apt-get install tre-agrep libtre4 libtre-dev
and then install this package (https://pypi.python.org/pypi/tre/0.8.0) via pip:
sudo -H pip install tre

Troubles with pip? See this:
https://stackoverflow.com/questions/17886647/cant-install-via-pip-because-of-egg-info-error
"""

import tre
import itertools
import time
from multiprocessing import Pool

import preprocess


"""
Opening tweets and locations files.
"""
tweetFile = "porteousd_tweets_small.txt"
with open(tweetFile, "r") as f:
    tweets = f.read().splitlines()

locationsFile = "geonames/US-loc-names.txt"
with open(locationsFile, "r") as f:
    locations = f.read().splitlines()



"""
Preprocessing the tweets and locations data. See preprocessing.py for more info.
"""
print
print("Preprocessing locations...")
locations = preprocess.preprocessLocations(locations)

print
print("Getting dictionary of common words without locations...")
wordsNoLocations = preprocess.getWordsNoLocationsDict(locations)

print
print("Preprocessing tweets...")
tweets = list(preprocess.preprocessTweets(tweets, wordsNoLocations))

# Creating the fuzziness object. This maxerr represents the max local edit distance.
fz = tre.Fuzzyness(maxerr=3)

# Takes a chunk of locations and checks the tweets for these locations.
def checkLocations(locations):
    output = []
    for l, origL in locations:
        cmpl = tre.compile(l, tre.EXTENDED)
        for t, origT in tweets:
            m = cmpl.search(t, fz)
            if m:
                out = {"tweet": origT, "location": origL, "match": m[0], "cost": m.cost, "numDel": m.numdel, "numIns": m.numins, "numSub": m.numsub}
                output.append(out)
    return output

locations = list(locations)

# Generator that produces chunks of the larger list of locations.
def chunkGen(locations, chunkSize=10000):
    for i in range(0, len(locations), chunkSize):
        yield locations[i:i + chunkSize]

print
print("Starting search...")

startTime = time.time()

#locations = [("san francisco", "San Francisco")]

pool = Pool(16)
res = pool.map(checkLocations, chunkGen(locations))

res = [item for sublist in res for item in sublist]
print(res)
print(len(res))

print("--- %s seconds ---" % (time.time() - startTime))

# Dumping results to pickle.
import pickle
pickle.dump(res, open("results.p", "wb"))


# Handy line that shows what methods an object has
# from here: https://stackoverflow.com/questions/34439/finding-what-methods-an-object-has
# print([method for method in dir(mine) if callable(getattr(mine, method))])

"""
for t in tweets:
    cmpl = tre.compile(t, tre.EXTENDED)
    for l in locations:
        print(l)
        m = cmpl.search(l, fz)
        if m:
            print(m.groups())
            print(m[0])
"""

"""
Converting to C code, compiling that C code and running using Cython:
cython --embed -o ctreMain.c treMain.py && gcc -Os -I /usr/include/python2.7 -o ctreMain ctreMain.c -lpython2.7 -lpthread -lm -lutil -ldl && ./ctreMain
"""

"""
startTime = time.time()
for l in locations:
    cmpl = tre.compile(r"{}".format(l), tre.EXTENDED)
    for t in tweets:
        m = cmpl.search(t, fz)
        if m:
            print(t, l)
            #print(m.cost)
            #print(m[0])
print("--- %s seconds ---" % (time.time() - startTime))
"""