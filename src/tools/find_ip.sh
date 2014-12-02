#!/bin/bash

for i in {1..254}
do
    ping -c 1 -W 1 10.42.0.$i
done
