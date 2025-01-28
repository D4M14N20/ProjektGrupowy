#!/bin/ash

cp -r /data/in /tmp

g++ -Wall -o /tmp/out/program /tmp/in/*.cpp 2> /tmp/out/comp.stderr.txt
exit_code=$?

cp /tmp/out/* /data/out

exit $exit_code