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

# These are only used for getting small samples in getNTweetsWithFuzz.
import random
import csv




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




def checkLocations(locations):
    """
    Takes a chunk of locations and checks the tweets for these locations.
    Will be run in parallel.
    """
    output = []
    for l, origL in locations:
        # Check only for locations with spaces/tabs/etc. on the start and end.
        # Eliminates potential matches, but most of them would be garbage.
        # Trades precision for accuracy
        cmpl = tre.compile(r"\b{}\b".format(l), tre.EXTENDED)
        for t, origT in tweets:
            m = cmpl.search(t, fz)
            if m:
                out = {"tweet": origT, "location": origL, "match": m[0], "cost": m.cost, "numDel": m.numdel, "numIns": m.numins, "numSub": m.numsub}
                output.append(out)
    return output

locations = list(locations)




def chunkGen(locations, chunkSize=1000):
    """
    Generator that produces chunks of the larger list of locations.
    """
    for i in range(0, len(locations), chunkSize):
        yield locations[i:i + chunkSize]


def mainSearch(locations, fuzz):
    """
    Main functionality. Tests all 1.3 million locations against the small tweet file.
    Majority of study was conducted on this function.
    """
    # Creating the fuzziness object. This maxerr represents the max local edit distance.
    global fz # The global fz prevents having to pass fz to checkLocations each call in pool.map
    fz = tre.Fuzzyness(maxerr=fuzz)

    print
    print("Starting search...")

    startTime = time.time()

    pool = Pool(16)
    res = pool.map(checkLocations, chunkGen(locations))

    res = [item for sublist in res for item in sublist] # Flattening the list of dicts.

    print("--- %s seconds ---" % (time.time() - startTime))
    
    return res


def getNTweetsWithFuzz(locations, numTweets, fuzz):
    """ 
    Give this function like 500 results if numTweets is 200 so it has enough to pull entries
    with the requested fuzz/cost. We use this function to check the precision of the algorithm
    at various edit distances. These will be unique matches,
    """

    global fz
    fz = tre.Fuzzyness(maxerr=fuzz)

    res = []

    print
    print("Starting search...")

    startTime = time.time()

    pool = Pool(16)

    seen = []

    while len(res) < numTweets:
        # Pass the function chunks until it finds enough hits with the requested cost.
        randomLocations = [locations.pop(random.randrange(len(locations))) for _ in xrange(numTweets*100)]
        print("Testing {} random locations.".format(len(randomLocations)))
        res = res + mainSearch(randomLocations, fuzz)

        # Filter matches we've already had and items of the wrong cost.
        new = []
        for r in res:
            if r["match"] not in seen and r["cost"] == fuzz:
                new.append(r)
                seen.append(r["match"])

        res = new
        print("Number of tweets at cost {} found so far: {}".format(fuzz, len(res)))

    print("--- %s seconds ---" % (time.time() - startTime))

    return res[:numTweets]




# Uncomment this to get a sample set of data with a given cost.
# res = getNTweetsWithFuzz(locations, 200, 1)

# This is the main functionality
res = mainSearch(locations, 3)

# Uncomment this if using getNTweetsWithFuzz for a csv printout.
"""
with open("resultsDist1_200.csv", "w") as f:
    w = csv.DictWriter(f, res[0].keys())
    w.writeheader()
    w.writerows(res)
"""

# Dumping results to pickle.
import pickle
pickle.dump(res, open("resultsTestSmall.p", "wb"))


"""
Converting to C code, compiling that C code and running using Cython:
cython --embed -o ctreMain.c treMain.py && gcc -Os -I /usr/include/python2.7 -o ctreMain ctreMain.c -lpython2.7 -lpthread -lm -lutil -ldl && ./ctreMain
"""