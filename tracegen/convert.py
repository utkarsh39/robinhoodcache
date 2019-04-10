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
        binsize = 20000
        threshold = 50
        if num_keys > threshold:
            tmp = t/binsize
            if tmp in req_dist:
                req_dist[tmp] += 1
            else:
                req_dist[tmp] = 1
        t += 1
        if t > numlines:
            break

plot_dict = {}
for key in req_dist:
    plot_dict[key*20] = req_dist[key]
    
lists = sorted(plot_dict.items()) # sorted by key, return a list of tuples

x, y = zip(*lists) # unpack a list of pairs into two tuples

plt.plot(x, y)
plt.title('Request Size Distribution for requests containing more than ' + str(threshold) + ' keys\n' +
          'for first ' + str(numlines) + ' requests')
plt.show()


# maxkey = max(keyspace.iteritems(), key=operator.itemgetter(1))[0]
# print key /space[maxkey]
