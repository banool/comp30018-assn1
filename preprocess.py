#!/usr/bin/python3

import re

def toLower(inp):
    print("    Converting to lower case.")
    output = []

    for i in inp:
        new = i.lower()
        output.append(new)

    return output

def removePunctuation(inp):
    print("    Removing punctuation.")
    output = []

    for i in inp:
        new = re.sub(r'[^\w\s]','', i)
        output.append(new)

    return output

def removeNumbers(inp):
    """
    Finds any word with a number in it and removes it.
    Might be erroneous behaviour because an intended location might have a typo number in it.
    """
    print("    Removing words with numbers in them.")

    output = []

    for i in inp:
        new = " ".join([w for w in i.split() if not any(c.isdigit() for c in w)])
        output.append(new)

    return output

def getWordsNoLocationsDict(locations):
    """
    Returns a list of common words with no locations in them.
    This can be used to clean a tweet of words that we KNOW aren't a location.
    Main negative is it would delete words that were meant to be locations but
    wer mispelled from the intended location word into a different valid word.
    Make sure to call this after having preprocessed the locations (so that 
    they're lower case, cleaned of puncation, etc).
    """

    wordsFile = "/usr/share/dict/words"
    with open(wordsFile, "r") as f:
        wordsDict = f.read().splitlines()

    wordsDict = toLower(removePunctuation(wordsDict))
    wordsDict = set(wordsDict)
    locations = set(locations)

    return wordsDict - locations


def preprocessTweets(tweets, wordsNoLocations):
    """
    Preprocesses the tweets, removing tokens that we know won't have locations in them.
    """
    
    def cleanNumbersAndDateTime(tweets):
        """
        Takes the input tweets and cleans them of the two starting numbers
        and the date at the end of each tweet, assuming they're present.
        """
        print("    Removing numbers from the start and dates from the end.")

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

    def removeCommonWords(tweets, wordsNoLocations):
        """
        Uses the dictionary of words that aren't locations to remove common words.
        This won't pick up all non-location words, but should cut down the length of the tweet quite substantially.
        """
        print("    Removing common words from tweets.")

        numWordsRemoved = 0
        output = []

        for tweet in tweets:
            sp = tweet.split()
            noCommon = [w for w in sp if w not in wordsNoLocations]
            numWordsRemoved += len(sp) - len(noCommon)
            new = " ".join(noCommon)
            output.append(new)

        print("        Removed {} common words from tweets.".format(numWordsRemoved))        
        return output            

    cleaned = cleanNumbersAndDateTime(tweets)
    cleaned = removeNumbers(cleaned)
    cleaned = toLower(cleaned)
    cleaned = removePunctuation(cleaned)
    cleaned = removeCommonWords(cleaned, wordsNoLocations)

    print("    Removing duplicates.")
    oldLen = len(cleaned)
    cleaned = set(cleaned) # Remove duplicates by converting to a set.
    print("        Removed {} items.".format(oldLen-len(cleaned)))

    return cleaned

def preprocessLocations(locations):
    """
    Preprocesses the locations, removing tokens that we know won't have locations in them.
    """

    def removeShortLong(locations):
        print("    Removing locations that are too short or long.")

        oldLen = len(locations)
        output = []

        for loc in locations:
            length = len(loc)
            if length > 4 and length < 70:
                output.append(loc)

        newLen = len(output)
        print("        Removed {} items.".format(oldLen-newLen))
        return output  
        

    cleaned = toLower(locations)
    cleaned = removePunctuation(cleaned)
    cleaned = removeNumbers(cleaned)
    cleaned = removeShortLong(cleaned)

    print("    Removing duplicates.")
    oldLen = len(cleaned)
    cleaned = set(cleaned) # Remove duplicates by converting to a set.
    print("        Removed {} items.".format(oldLen-len(cleaned)))

    return cleaned


if __name__ == "__main__":
    tweets = ["hey brude what's up?", "123 5125 123123123", "Hey man number 123 whatsup"]
    tweets = preprocessTweets(tweets)
    print(tweets)