#!/bin/bash


ping -q -c 1 $1 > /dev/null 2> /dev/null && echo "sucsesfuly pinged $1" || echo "could not ping $1"


tcp="$(echo "connect" | netcat -vz $1 $2 2>&1)" 
echo "$tcp"
if [[ $tcp =~ "failed:" ]] 
	then
	echo "failed to connect tcp"
	exit 1
fi

echo "recived" | nc -l -p $2 | tee  output.log; 


udp="$( netcat -u -vz $1 $2 2>&1)" 
echo "$udp"


