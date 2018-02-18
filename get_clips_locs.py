#!/usr/bin/env pythonw

import subprocess
import sys
import json

primary="eDP1"

def run_command(cmd):
	# print("$ {}".format(cmd))
	proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	return proc.stdout

result = {}

xrandr = run_command("xrandr")
xrandr = xrandr.split('\n')
for line in xrandr:
	if line.find('VIRTUAL') == -1:
		continue
	if line.find('disconnected') != -1:
		# print("disconnected:", line)
		continue
	if line.find('mm') == -1:
		# print("not active:", line)
		continue
	line = line.split(' ')
	result[line[0]] = line[2]

# print(result)
output = json.dumps(result)
print(output)
