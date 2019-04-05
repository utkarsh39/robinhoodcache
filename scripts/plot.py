# myplot.py
from bokeh.plotting import figure, curdoc
from bokeh.driving import linear
from bokeh.io import show
from bokeh.layouts import row
import urllib, json, sys, time, datetime
from bokeh.palettes import Dark2_5 as palette
from bokeh.models.annotations import Title
import itertools
import sys
#colors has a list of colors which can be used in plots 
colors = itertools.cycle(palette)
ip = sys.argv[1]
url = "http://" + ip + ":9999/getstats"

p_p99 = figure(plot_width=600, plot_height=600, y_axis_type="log")
p_p99.xaxis.axis_label = 'Time'
p_p99.yaxis.axis_label = 'p99 Latency (in ms)'

p_hit = figure(plot_width=600, plot_height=600, y_axis_type="log")
p_hit.xaxis.axis_label = 'Time'
p_hit.yaxis.axis_label = 'Request Hit Rate (in %)'

t_p99 = Title()
t_p99.text = 'p99 Latency Time Series'
p_p99.title = t_p99

t_hit = Title()
t_hit.text = 'Request Hit Rate'
p_hit.title = t_hit

ds_p99 = {}
r_p99 = {}
y_p99 = {}
x_p99 = {}

ds_hit = {}
r_hit = {}
y_hit = {}
x_hit = {}

def setup(ds, r, y, x, p, param1, param2):
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
                data[dep][param1][param2]
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

def setup_p99():
    setup(ds_p99, r_p99, y_p99, x_p99, p_p99, "2", "p99")
    
def func_p99(data, dep):
    return data[dep]["2"]["p99"] / 1e6

@linear()
def update_p99(step):
    update(step, ds_p99, r_p99, y_p99, x_p99, p_p99, func_p99)

def setup_hit():
    setup(ds_hit, r_hit, y_hit, x_hit, p_hit, "2", "count")

def func_hit(data, dep):
    # print data[dep]["2"]["count"]
    if data[dep]["2"]["count"] == 0:
        return 0
    return 100 * (data[dep]["1"]["count"]*1.0 / data[dep]["2"]["count"])

@linear()
def update_hit(step):
    update(step, ds_hit, r_hit, y_hit, x_hit, p_hit, func_hit)


def update(step, ds, r, y, x, p, func):
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
            data[dep]["2"]["count"]
        except:
            continue
        # d = data[dep]["2"]["p99"]/1e6
        # d_hit = 100*(data[dep]["1"]["p99"]/data[dep]["2"]["p99"])
        d = func(data, dep)
        # print dep, d
        if dep in y:
            print dep, d
            y[dep].append(d)
            x[dep].append(step)
            ds[dep].data['y'] = y[dep]
            ds[dep].data['x'] = x[dep]
        else:
            # print dep, d
            y[dep] = []
            x[dep] = []
            y[dep].append(d)
            x[dep].append(step)
            ln = p.line([], [], line_width=2, legend=dep, color=next(colors))
            r[dep] = ln
            ds[dep] = ln.data_source

curdoc().add_root(row(p_p99, p_hit))
setup_p99()
setup_hit()
# Add a periodic callback to be run every 500 milliseconds
curdoc().add_periodic_callback(update_p99, 1000)
curdoc().add_periodic_callback(update_hit, 1000)