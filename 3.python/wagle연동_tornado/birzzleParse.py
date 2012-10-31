#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import sys


DICT = {}

def parseline(line):
	if line.find('Birzzle')==-1: 
		return None

	if line[0]=='[':
		flds = line.split()
		if len(flds) < 4: 
			return None
		timestr = flds[1]+" "+flds[2]
		idstr = flds[3]			
		print timestr, idstr
		pass
	else:
		#pos = line.find(u"레벨")
		flds = line.split()
		if len(flds) < 7: 
			return None
		levelstr = flds[4]
		scorestr = flds[6]
		print levelstr, scorestr
		pass

# load the first line
def load(fname):
	f = codecs.open(fname, "r", "utf-8")
	for line in f.xreadlines():
		parseline(line)
	f.close()

if __name__=="__main__":
	load(sys.argv[1])
