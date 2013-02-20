#!/usr/bin/env python
import os, sys, os.path, stat, fnmatch, shutil, filecmp
import time
from stat import *

# find . -name "*.[ch]" -print

### Create File List
def extList(eList):
	List = eList.split(",")
	#print List
	for e in range(len(List)):
		List[e] = List[e].replace(" ", "")
	#print List
	return List

def matchAny(fname, patterns):
	for p in patterns: 
		if fnmatch.fnmatchcase(fname, p):
			return 1
	return 0


def	goodTime(t):
	tuple = time.localtime(t)
	return "%d/%d %d:%d" %(tuple[1], tuple[2], tuple[3], tuple[4]) 

def walktree(top, patterns, toplen, callback, prn=0):
	for f in os.listdir(top):
		pathname = os.path.join(top, f)
		print pathname
		try:
			stinfo = os.stat(pathname)
		except OSError:
			continue

		mode = stinfo[ST_MODE]
		if S_ISDIR(mode):
			os.chdir(pathname)

			# It's a directory, recurse into it
			walktree(pathname, patterns, toplen, callback, prn)
		elif S_ISBLK(mode):
			print "block :", pathname

		elif S_ISREG(mode):
			# It's a file, call the callback function
			if matchAny(f, patterns):
				pname = pathname[toplen:]
				if pname[0]=='/': pname = pname[1:]
				if prn: print pname,"\t\t", stinfo[ST_SIZE], stinfo[ST_MTIME]	
				if callable(callback): callback(pname)
		else:
			# Unknown file type, print a message
			pass

def	prn_finfo(path):
	s = os.stat(path)
	print path, s[ST_SIZE], s[ST_MTIME], time.strftime('%Y/%M/%D %h:%m%s', s[ST_MTIME])


####

def prnBeauty(str, ment):
	m = 72 - len(str)
	print str, "-"*m, ment

class walkdir:
	def __init__(self, dir, fileext='', callback=None ):
		if fileext=='':
			pList = extList("*.c, *.h, *.py, *.script, *Jamfile, *cshrc*")
		else:
			pList = []
		walktree(dir, pList, len(dir), callback, 1)

### main()
def my_callback(fpath):
	print "\t", fpath
	#os.system("cvs status %s" %fpath)
	pass

if __name__=="__main__":
	os.chdir(sys.argv[1])
	w = walkdir(sys.argv[1], '', my_callback)

