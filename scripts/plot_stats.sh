#/bin/sh
# Arguments
# 1 - Port for bokeh
# 2 - IP of the server where simulation is running
source deactivate
source activate py2
bokeh serve --show plot.py --port $1 --args $2 1>/dev/null 2>/dev/null&

# Curl stats periodically
now=$(date +"%T")
c="$2_$now"
echo $c
mkdir $c && cd $c 
declare -i out=0
while :
do
	curl $2:9999/getstats > $out
    out=$((out+5))
	sleep 300
done