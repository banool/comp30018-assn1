How to use

Your system will need the TRE library. Easiest way to get it on unix is:
sudo apt-get install tre-agrep libtre5 libtre-dev
Following this, you'll need the python hooks, most easily installed by:
(sudo) pip install tre

Following this, all you have to do is run it from the command line (assuming 
that the location and twitter data are in the expected locations).
preprocess.py can also be run on its own using a sample set of data.

Be careful using this script as it utilises multiprocessing and will quickly
take control over pretty much 100% CPU usage. The parameters are easy enough
to change within the script though (map.Pool), so it shouldn't be a worry.