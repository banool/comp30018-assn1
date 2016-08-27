#!/usr/bin/python3

import re

target = "porteousd_tweets_small.txt"

with open(target, "r") as f:
	tweets = f.read().splitlines()


"""
Takes the input tweets and cleans them of the two starting numbers
and the date at the end of each tweet, assuming they're present.
"""
def cleanNumbersAndDateTime(tweets):
	datePattern = r"([0-9]{4}-[0-9]{2}-[0-9]{2}\s[0-9]{2}:[0-9]{2}:[0-9]{2})"
	twoNumPattern = r"^[0-9]+\s[0-9]+"

	output = []	

	for i in tweets:
		trimTwoNumStart = False
		trimDateEnd = False
		sp = i.split()

		if re.match(twoNumPattern, " ".join(sp[:2])):
			trimTwoNumStart = True

		if re.match(datePattern, " ".join(sp[-2:])):
			trimDateEnd = True

		if trimTwoNumStart:
			startSplit = 2
		else:
			startSplit = None

		if trimDateEnd:
			endSplit = -2
		else:
			endSplit = None

		tweet = " ".join(sp[startSplit:endSplit])
		output.append(tweet)

	return output

def removeWordsWithNumbers(tweets):
    output = []

    for tweet in tweets:
        new = " ".join([w for w in tweet.split() if not any(c.isdigit() for c in w)])
        output.append(new)

    return output