import json
import csv
import random
import sys
import operator

if len(sys.argv) < 2:
    print "need trace path name as argument"


idSizes = {}
minSize = 1000
maxSize = 1000

backtoid = {}
t = 0
keyspace = {}
req_dist = {}

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
        req_dist[t] = num_keys
        t += 1

# maxkey = max(keyspace.iteritems(), key=operator.itemgetter(1))[0]
# print key /space[maxkey]
