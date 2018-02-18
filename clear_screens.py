#!/usr/bin/env pythonw

import subprocess
import sys

primary="eDP1"

def run_command(cmd):
	print("$ {}".format(cmd))
	proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	return proc.stdout

reset_primary = "xrandr --output {} --mode 1920x1080".format(primary)
print(run_command(reset_primary))

for output in ['VIRTUAL1', 'VIRTUAL2']:
	disable = "xrandr --output {output} --off --output {primary} --mode 1920x1080".format(output=output, primary=primary)
	print(run_command(disable))

print(reset_primary)
print(run_command(reset_primary))
