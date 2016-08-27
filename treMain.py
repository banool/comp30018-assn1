#!/usr/bin/python

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
import preprocess

tweetFile = "porteousd_tweets_small.txt"
with open(tweetFile, "r") as f:
    tweets = f.read().splitlines()

locationsFile = "geonames/US-loc-names.txt"
with open(locationsFile, "r") as f:
    locations = f.read().splitlines()

print("Preprocessing tweets...")
tweets = preprocess.preprocessTweets(tweets)
print("Preprocessing locations...")
locations = preprocess.preprocessLocations(locations)

test = tre.compile(r"new york", tre.EXTENDED)
fz = tre.Fuzzyness(maxerr = 0)

for t in tweets:
    m = test.search(t, fz)
    if m:
        print(m.groups())
        print(m[0])

# Handy line that shows what methods an object has
# from here: https://stackoverflow.com/questions/34439/finding-what-methods-an-object-has
# print([method for method in dir(mine) if callable(getattr(mine, method))])