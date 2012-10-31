#!/usr/bin/env python
import sys
				
	

def doit(logfile, starttime="00:00:00", endtime="23:59:59"):
	print starttime, endtime
	try:
		fd = open(logfile, 'r')
	except:
		print "file NOT found:", logfile
		return

	prefixlen = len(starttime)
	for line in fd:
		prefix = line[:prefixlen]
		if prefix.count(':') != 2: continue
		if prefix>= starttime: break


	for line in fd:
		prefix = line[:prefixlen]
		if prefix.count(':') != 2: continue
		if prefix > endtime: break
		print line[:-1]

if __name__=="__main__":
	print "usage: input_file start_time end_time"
	if len(sys.argv) > 2:
		doit(sys.argv[1], sys.argv[2], sys.argv[3])
		


