# myplot.py
from bokeh.plotting import figure, curdoc
from bokeh.driving import linear
from bokeh.io import show, export_png, export_svgs
from bokeh.layouts import row, widgetbox
import urllib, json, sys, time, datetime
from bokeh.palettes import Dark2_5 as palette
from bokeh.models.annotations import Title
from bokeh.models.widgets import Dropdown
import time;
import csv

import itertools
import sys
#colors has a list of colors which can be used in plots 
colors = itertools.cycle(palette)
urllist = []
for ip in sys.argv[1:]:
    urllist.append("http://" + ip + ":9999/getstats")

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

csvdata = {}
csvfile = {}

def getipfromurl(url):
    return url[7:-14]

# Data sources in a json file to plot
dep_show = {"req"}
localtime = time.asctime(time.localtime(time.time()))
it = 0

def setup(dsm, rm, ym, xm, p, param1, param2):
    if param2 not in csvdata:
        writer = csv.writer(open(param2 + "_" + localtime + ".csv", 'w'))
        head = []
        for url in urllist:
            head.append(getipfromurl(url))
        csvdata[param2] = []
        csvdata[param2].append(head)
        csvfile[param2] = param2 + "_" + localtime + ".csv"

    for url in urllist:
        if url not in dsm:
            dsm[url] = {}
            rm[url] = {}
            ym[url] = {}
            xm[url] = {}

    for url in urllist:
        ds = dsm[url]
        r = rm[url]
        y = ym[url]
        x = xm[url]
        while True:
            try:
                response = urllib.urlopen(url)
                data = json.loads(response.read())
            except:
                print "No conn"
                time.sleep(30)
                continue
            for dep in data.keys():
                if dep not in dep_show:
                    continue
                try:
                    data[dep][param1][param2]
                except:
                    continue
                if dep not in y:
                    y[dep] = []
                    x[dep] = []
                    ln = p.line([], [], line_width=2, legend = dep+"_"+getipfromurl(url), color = next(colors))
                    r[dep] = ln
                    ds[dep] = ln.data_source
            break

def setup_p99():
    setup(ds_p99, r_p99, y_p99, x_p99, p_p99, "2", "p99")
    
def func_p99(data, dep):
    return data[dep]["0"]["p99"] / 1e6

@linear()
def update_p99(step):
    update(step, ds_p99, r_p99, y_p99, x_p99, p_p99, func_p99, "p99")

def setup_hit():
    setup(ds_hit, r_hit, y_hit, x_hit, p_hit, "2", "count")

def func_hit(data, dep):
    if data[dep]["2"]["count"] == 0:
        return 0
    return 100 * (data[dep]["1"]["count"]*1.0 / data[dep]["2"]["count"])

@linear()
def update_hit(step):
    update(step, ds_hit, r_hit, y_hit, x_hit, p_hit, func_hit, "count")


def update(step, dsm, rm, ym, xm, p, func, param):
    row = []
    for url in urllist:
        ds = dsm[url]
        r = rm[url]
        y = ym[url]
        x = xm[url]
        try:
            response = urllib.urlopen(url)
            data = json.loads(response.read())
        except:
            print "No conn"
            time.sleep(30)
            return
        for dep in data.keys():
            if dep not in dep_show:
                continue
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
                # print dep, d
                y[dep].append(d)
                x[dep].append(step)
                ds[dep].data['y'] = y[dep]
                ds[dep].data['x'] = x[dep]
                row.append(d)
            else:
                # print dep, d
                y[dep] = []
                x[dep] = []
                y[dep].append(d)
                x[dep].append(step)
                ln = p.line([], [], line_width=2, legend=dep+"_"+getipfromurl(url), color=next(colors))
                r[dep] = ln
                ds[dep] = ln.data_source
    
    csvdata[param].append(row)
    # Flush data to csv every minute
    if len(csvdata[param]) % 60 == 0:
        f = open(csvfile[param], "w")
        writer = csv.writer(f)
        for row in csvdata[param]:
            writer.writerow(row)
        csvdata[param] = []
        f.close()

menu = [("PNG", "png"), ("SVG", "svg")]
save_drop = Dropdown(label="Save as:", button_type="warning", menu=menu)

def save_handler(attr, old, new):
    lt = time.asctime( time.localtime(time.time()))
    if new == 'png':
        export_png(p_p99, filename="p99_%s.png" % str(lt))
        export_png(p_hit, filename="req_%s.png" % str(lt))
    elif  new == 'svg':
        p_p99.output_backend = "svg"
        p_hit.output_backend = "svg"
        export_svgs(p_p99, filename="p99_%s.svg"  % str(lt))
        export_svgs(p_hit, filename="req_%s.svg" % str(lt))

save_drop.on_change('value', save_handler)

curdoc().add_root(row(p_p99, p_hit, widgetbox(save_drop)))
setup_p99()
setup_hit()
# Add a periodic callback to be run every 500 milliseconds
curdoc().add_periodic_callback(update_p99, 1000)
curdoc().add_periodic_callback(update_hit, 1000)