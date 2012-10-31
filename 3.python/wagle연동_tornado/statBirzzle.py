#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs


def get_score(line):
	ptn = "클래식 모드에서"
	p = line.find(ptn)
	if p==-1: return None
	print p

				
	# load the first line
def load(fname):
	print "Loading:", fname
	f = codecs.open(fname, "r", "utf-8")
	for line in f.xreadlines():
		get_score(line)


if __name__=="__main__":
	import sys
	if len(sys.argv) > 1:
		load(sys.argv[1])
