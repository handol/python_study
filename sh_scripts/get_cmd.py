#!/usr/bin/env python
import os
import sys


def read_cmd_file(fname, rmi=0):
	try:
		f = open(fname, "r")
	except:
		print "read error : ", fname
		return

	for l in f.readlines():
		pos = l.find("DATA[")
		if pos<0: continue
		nl = l[pos+5:-2]
		if nl.startswith("user"): continue
		if rmi:
			print 'rmi -u admin -p hlr -c "%s"' % nl
		else:
			print nl


if len(sys.argv) < 2:
	#print "Give me package number"
	#print "ex) %s 7 " % (sys.argv[0])
	print "%s filename [rmi] " % (sys.argv[0])
	print "ex) %s ~/hlrhome/log/.cmdhistory/12/cmd.20031215 " % (sys.argv[0])

if len(sys.argv) > 2:
	read_cmd_file(sys.argv[1], 1)
else:
	read_cmd_file(sys.argv[1], 0)
