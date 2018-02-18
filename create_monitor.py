#!/usr/bin/env pythonw

import subprocess
import sys

# progname.py VIRTUAL1 1920 1080 left 
primary="eDP1"
output=sys.argv[1]
xpx=int(sys.argv[2])
ypx=int(sys.argv[3])
refresh=60
position=sys.argv[4]+"-of"
# position=["left-of", "right-of"][1]

def run_command(cmd):
	print("$ {}".format(cmd))
	proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	return proc.stdout

gtf_cmd = "gtf {xpx} {ypx} {refresh}".format(xpx=xpx, ypx=ypx, refresh=refresh)
gtf_out = run_command(gtf_cmd)

gtf_out = gtf_out.strip().split('\n')[-1].strip()
modeline = gtf_out[len("Modeline "):].strip()
name = modeline.split()[0].strip()[1:-1]

print("Modeline:", modeline)
print("Name:", name)

if len(modeline) == 0 or len(name) == 0:
	sys.exit("Modeline/name is empty")

disable = "xrandr --output {output} --off --output {primary} --mode 1920x1080".format(output=output, primary=primary)
print(run_command(disable))

reset_primary = "xrandr --output {} --mode 1920x1080".format(primary)
print(run_command(reset_primary))

delmode = "xrandr --delmode {output} {name}".format(output=output, name=name)
print(run_command(delmode))
rmmode = "xrandr --rmmode {name}".format(name=name)
print(run_command(rmmode))
newmode = "xrandr --newmode {modeline}".format(modeline=modeline)
print(run_command(newmode))
addmode = "xrandr --addmode {output} {name}".format(output=output, name=name)
print(run_command(addmode))

print(reset_primary)
print(run_command(reset_primary))

print("--output {output} --mode {name} --{position} {primary}".format(output=output, name=name, position=position, primary=primary))

# NOTE: put all screens into this command
# example: xrandr --output VIRTUAL1 --mode 1920x1080_60.00 --left-of eDP1 --output VIRTUAL2 --mode 1280x720_60.00 --right-of eDP1
# enable_output = "xrandr --output {output} --mode {name} --{position} {primary}".format(output=output, name=name, position=position, primary=primary)
# print (enable_output)
# print(run_command(enable_output))
