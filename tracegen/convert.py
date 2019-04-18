#This code works in Python2
import json
import csv
import random
import sys
import operator
import matplotlib.pylab as plt

if len(sys.argv) < 2:
    print "need trace path name as argument"


idSizes = {}
minSize = 1000
maxSize = 1000

backtoid = {}
t = 0
keyspace = {}
req_dist = {}
max_keys = {}
keys_in_bins = {}
numlines = int(sys.argv[2])
with open(sys.argv[1]) as df:
    for line in df:
        bla = json.loads(line.strip())
        base = {"t": t, "d": [{}]}
        num_keys = 0
        for query in bla:
            num_keys += 1
            if query["backend"] not in backtoid:
#                print idx, line
                backtoid["backend"]="b4fbebd8"
#                idx+=1
            if backtoid["backend"] not in base["d"][0]:
                base["d"][0][backtoid["backend"]] = {"S": [], "U": [], "C": []}
            base["d"][0][backtoid["backend"]]["S"].append(query["size"])
            base["d"][0][backtoid["backend"]]["U"].append(str(query["uri"]))
            base["d"][0][backtoid["backend"]]["C"].append(1)
            if query["uri"] not in keyspace:
                keyspace[query["uri"]] = 1
            else:
                keyspace[query["uri"]] += 1
        # print json.dumps(base)
        # Find number of requests having requests more than a threshold contained within them
        binsize = 5000
        threshold = 50
        if num_keys > threshold:
            tmp = t/binsize
            if tmp in req_dist:
                req_dist[tmp] += 1
            else:
                req_dist[tmp] = 1
        tmp = t/binsize

        if tmp in max_keys:
            max_keys[tmp] = max(max_keys[tmp], num_keys)
        else:
            max_keys[tmp] = num_keys

        if tmp in keys_in_bins:
            keys_in_bins[tmp] += num_keys
        else:
            keys_in_bins[tmp] = 0

        t += 1
        if t > numlines:
            break

def plot_dict(d, title):

    pdict = {}
    for key in d:
        pdict[key*binsize/1000] = d[key]
        
    lists = sorted(pdict.items()) # sorted by key, return a list of tuples

    x, y = zip(*lists) # unpack a list of pairs into two tuples

    plt.plot(x, y)
    plt.title(title)
    plt.figure()

plot_dict(req_dist, 'Request Size Distribution for requests containing more than '
          + str(threshold) + ' keys\n' + 'for first ' + str(numlines)
          + ' requests')
            
plot_dict(max_keys, 'Max Keys Distribution\n' +
          'for first ' + str(numlines) + ' requests')

plot_dict(keys_in_bins, 'Total keys requested\n' +
          'for first ' + str(numlines) + ' requests')

plt.show()
