# COMP30018 - Assignment 1
Assignment 1 for COMP30018 - Knowledge Technologies, an approximate string search tool.

## Overview
The aim of this project is to find locations within twitter data (tweets). For this, we were given roughly 1.3 million locations to find within roughly 300 thousand tweets.

The library used in this project is the excellent TRE library (https://github.com/laurikari/tre), an efficient local edit distance implementation written in C. A python interface was used to function this library, as well as multi-processing to significantly improve run time.

For a sample tweet collection of 4k tweets, this script can search for all 1.3 million locations in 30 mins - 2 hours with an edit distance of 3, depending on the speed of your system. This is reasonable performance considering the scope of the problem.

## How to use
(The below is copied from the README.txt file, which was required for the submission of the project).

Your system will need the TRE library. Easiest way to get it on unix is:
sudo apt-get install tre-agrep libtre5 libtre-dev
Following this, you'll need the python hooks, most easily installed by:
(sudo) pip install tre

The source for TRE can be found here:
https://github.com/laurikari/tre
All credit of course to Ville Laurikari for a great library, even if the pydocs are a bit limited.

Following this, all you have to do is run it from the command line (assuming 
that the location and twitter data are in the expected locations). I haven't included them here for data duplication purposes (they're already on the server).
preprocess.py can also be run on its own using a sample set of data.

For example, do the following:
./treMain.py

## Basic functionality

The basic functioning of the system is the following:

1. The location, tweet and other useful data are read in.
2. This data is pre-processed by the functions in preprocess.py
3. The locations are broken into chunks by a generator and passed to a multiprocessing based map function.
4. Each spawned process will iterate through each location, checking all the tweets for any instance of it. To do this it compiles a regex for a location, which is then searched for in each tweet given a set "fuzziness" (edit distance).
5. Once all the locations in the chunk (around 10k per chunk), it will report back a list of dictionaries with the tweet, location and match in question, as well as cost information. 
6. The main process keeps dishing out chunks until it is all entirely done.
7. The final results are by default dumped to a pickle file, but can just as easily be put in a csv file.

## Notes

Be careful using this script as it utilises multiprocessing and will quickly
take control over pretty much 100% CPU usage. The parameters are easy enough
to change within the script though (map.Pool), so it shouldn't be a worry.

The .csv files here are just there because I vaguely referenced them in my report, they're the manually checked tweets. The original data is not included in the repo because it is far too large.

## Results

Final result: 14.5/15

Critical analysis: 6/6 || Creativity: 2/2 || Soundness: 4/4 || Report quality: 2.5/3

The 0.5 was lost for report being slightly too long.