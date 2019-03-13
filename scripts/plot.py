# myplot.py
from bokeh.plotting import figure, curdoc
from bokeh.driving import linear
import urllib, json, sys, time, datetime
from bokeh.palettes import Dark2_5 as palette
from bokeh.models.annotations import Title
import itertools
import sys
#colors has a list of colors which can be used in plots 
colors = itertools.cycle(palette)
ip = sys.argv[1]
url = "http://" + ip + ":9999/getstats"

p = figure(plot_width=900, plot_height=600, y_axis_type="log")
p.xaxis.axis_label = 'Time'
p.yaxis.axis_label = 'p99 Latency (in ms)'
t = Title()
t.text = 'p99 Latency Time Series'
p.title = t
ds = {}
r = {}
y = {}
x = {}
def setup():
    while True:
        try:
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            print data
        except:
            print "No conn"
            time.sleep(30)
            continue
        for dep in data.keys():
            try:
                data[dep]["2"]["p99"]
            except:
                continue
            # print dep, data[dep]["2"]["p99"]
            if dep not in y:
                y[dep] = []
                x[dep] = []
                ln = p.line([], [], line_width=2, legend = dep, color = next(colors))
                r[dep] = ln
                ds[dep] = ln.data_source
        break

@linear()
def update(step):
    try:
        response = urllib.urlopen(url)
        data = json.loads(response.read())
    except:
        print "No conn"
        time.sleep(30)
        return
    for dep in data.keys():
        try:
            data[dep]["2"]["p99"]
        except:
            continue
        d = data[dep]["2"]["p99"]/1e6
        if dep in y:
            print dep, d
            y[dep].append(d)
            x[dep].append(step)
            ds[dep].data['y'] = y[dep]
            ds[dep].data['x'] = x[dep]
        else:
            print dep, d
            y[dep] = []
            x[dep] = []
            y[dep].append(d)
            x[dep].append(step)
            ln = p.line([], [], line_width=2, legend=dep, color=next(colors))
            r[dep] = ln
            ds[dep] = ln.data_source

curdoc().add_root(p)
setup()
# Add a periodic callback to be run every 500 milliseconds
curdoc().add_periodic_callback(update, 1000)