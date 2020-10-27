#!/bin/bash

x=0
TIME_RUN=1800
while [ $x -lt $TIME_RUN ]
do
	temp=$(vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*')
	timestamp=($x +'%s')
	printf "%s,%s\n" "$timestamp" "$temp"
	x=$((x+1))
	sleep 1
done

