#!/usr/bin/python3

import re

def toLower(inp):
    output = []

    for i in inp:
        new = i.lower()
        output.append(new)

    return output

def preprocessTweets(tweets):
    """
    Preprocesses the tweets, removing tokens that we know won't have locations in them.
    """
    
    def cleanNumbersAndDateTime(tweets):
        """
        Takes the input tweets and cleans them of the two starting numbers
        and the date at the end of each tweet, assuming they're present.
        """
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

    def removeNumbers(tweets):
        """
        Finds any word with a number in it and removes it.
        Might be erroneous behaviour because an intended location might have a typo number in it.
        """
        output = []

        for tweet in tweets:
            new = " ".join([w for w in tweet.split() if not all(c.isdigit() for c in w)])
            output.append(new)

        return output

    cleaned = cleanNumbersAndDateTime(tweets)
    cleaned = removeNumbers(cleaned)
    cleaned = toLower(cleaned)

    return cleaned

def preprocessLocations(locations):
    """
    Preprocesses the locations, removing tokens that we know won't have locations in them.
    """

    cleaned = toLower(locations)

    return cleaned


if __name__ == "__main__":
    tweets = ["hey brude what's up?", "123 5125 123123123", "Hey man number 123 whatsup"]
    tweets = preprocess(tweets)
    print(tweets)