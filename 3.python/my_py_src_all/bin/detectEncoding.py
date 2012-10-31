#!/usr/bin/env python
import chardet

def detect(fname):
	f = open(fname)
	buf = f.read()
	f.close()

	d = chardet.detect(buf)
	return d["encoding"]

if __name__=="__main__":
	import sys
	print detect(sys.argv[1])

