#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
def loadUserInfo(fname):
	fp = open(fname)
	userdict = {}
	for line in fp:
		flds = line.split(",")
		if len(flds) < 2: continue
		user = int(flds[0])
		numcoms = int(flds[1])
		userdict[user] = numcoms
	fp.close()
	return userdict


## GMM result 파일에서 cluster 개수 구함.
def getnumcluster(resfile):
	try:
		fp = open(resfile)
	except:
		print "read failed", resfile
		return 0

	line = fp.readline()
	flds =  line.split()
	if len(flds) < 3:
		return 0

	num = int(flds[1])
	fp.close()
	return num
	

def wc(fname):
	try:
		fp = open(fname)
		return len(fp.readlines())
	except:
		return 0

def doit(userfile, dirname, extname):
	userdict = loadUserInfo(userfile)

	files = os.listdir(dirname)
	#print "all files: %d" % (len(files))

	filterfunc = lambda x: x.endswith(extname)
	files = filter(filterfunc, files)
	#print "filtered files: %d" % (len(files))

	for file in files:
		basename = file.split(".")[0]
		numcoms = userdict.get(int(basename), 0)
		numclusters = getnumcluster(file+".res")
		numlines = wc(file)
		print "%s, %d, %d, %d" % (basename, numcoms, numclusters, numlines)
	
	

if __name__=="__main__":
	import sys
	if len(sys.argv) > 3:
		doit(sys.argv[1], sys.argv[2], sys.argv[3])
	else:
		print "usage: userfile dirname fileextension"	
