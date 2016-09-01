How to use

Your system will need the TRE library. Easiest way to get it on unix is:
sudo apt-get install tre-agrep libtre5 libtre-dev
Following this, you'll need the python hooks, most easily installed by:
(sudo) pip install tre

The source for TRE can be found here:
https://github.com/laurikari/tre
All credit of course to Ville Laurikari for a great library, even if the pydocs are a bit limited.

Following this, all you have to do is run it from the command line (assuming 
that the location and twitter data are in the expected locations).
preprocess.py can also be run on its own using a sample set of data.

For example, do the following:
./treMain.py

The basic functioning of the system is the following:
1. The location, tweet and other useful data are read in.
2. This data is pre-processed by the functions in preprocess.py
3. The locations are broken into chunks by a generator and passed to a multiprocessing based map function.
4. Each spawned process will iterate through each location, checking all the tweets for any instance of it. To do this it compiles a regex for a location, which is then searched for in each tweet given a set "fuzzyness" (edit distance).
5. Once all the locations in the chunk (around 10k per chunk), it will report back a list of dictionaries with the tweet, location and match in question, as well as cost information. 
6. The main process keeps dishing out chunks until it is all entirely done.
7. The final results are by default dumped to a pickle file, but can just as easily be put in a csv file.

Be careful using this script as it utilises multiprocessing and will quickly
take control over pretty much 100% CPU usage. The parameters are easy enough
to change within the script though (map.Pool), so it shouldn't be a worry.
