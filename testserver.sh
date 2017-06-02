#!/bin/bash

echo "recived" | nc -l -p 5555 | tee  output.log; 
echo "got tcp connection"
tcp="$(echo "connect" | netcat -vz 127.0.0.1 5555 2>&1)" 


nc -u -w 1 -l -p 5555 | tee  output.log; 
echo "got udp connection"