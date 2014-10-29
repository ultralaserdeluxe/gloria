#!/bin/bash

if [ "$#" -ne 1 ]
then
    echo "usage: connect.sh <ip-address>"
    exit 1
fi

# Kill connection if it exists
pand -k 00:19:0E:0F:F0:6F

# Create new connection
pand -n -c 00:19:0E:0F:F0:6F
ifconfig bnep0 $1 up

exit 0
