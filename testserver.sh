#!/bin/bash

echo "recived" | nc -l -p $2 | tee  output.log; 
echo "got tcp connection"
tcp="$(echo "connect" | netcat -vz $1 $2 2>&1)" 


nc -u -w 1 -l -p $2 | tee  output.log; 
echo "got udp connection"
