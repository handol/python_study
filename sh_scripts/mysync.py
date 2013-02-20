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


def setKoreaTime():
## not good
	import locale
	locale.setlocale(locale.LC_ALL, '')

def	goodTime(t):
	#return strftime("%Y/%m/%d %H:%M", gmtime(t))
	#return strftime("%m/%d %H:%M", gmtime(t))
	tuple = time.localtime(t)
	return "%d/%d-%d:%d" %(tuple[1], tuple[2], tuple[3], tuple[4]) 

def walktree(top, patterns, resList, topdirlen, prn=0, rootonly=0):

	for f in os.listdir(top):
		pathname = os.path.join(top, f)
		try:
			stinfo = os.stat(pathname)
		except OSError:
			return resList

		mode = stinfo[ST_MODE]
		if S_ISDIR(mode):
			# It's a directory, recurse into it
			if rootonly==0:
				resList += walktree(pathname, patterns, [], topdirlen, prn)
		elif S_ISREG(mode):
			# It's a file, call the callback function
			if matchAny(f, patterns):
				pname = pathname[topdirlen:]
				if pname[0]=='/': pname = pname[1:]
				if prn: print pname,"\t\t", stinfo[ST_SIZE], stinfo[ST_MTIME]	
				resList.append( [pname, stinfo[ST_SIZE], stinfo[ST_MTIME] ] )	
		else:
			# Unknown file type, print a message
			pass
	return resList

def	prn_finfo(path):
	s = os.stat(path)
	print path, s[ST_SIZE], s[ST_MTIME], time.strftime('%Y/%M/%D %h:%m%s', s[ST_MTIME])


####
def mkdir_ifnot_and_copy(srcdir, dstdir, newpath, docopy):
	#print "SD= ",srcdir,"DD= ", dstdir, "N= ", newpath
	pathname = os.path.join(dstdir, newpath)
	dir = os.path.dirname(pathname)
	#print "P= ",pathname,"D= ", dir
	if not os.path.exists(dir):
		print dir, "\t\t New DIR created ", dir
		os.makedirs(dir)
	if docopy: 
		try:
			shutil.copyfile(os.path.join(srcdir, newpath), pathname)
		except:
			print "copy FAILED :", os.path.join(srcdir, newpath), pathname
	#print os.path.join(srcdir, newpath),"-->", pathname

### Read and Compare File List
def readList(fname):
	f = file(fname)
	List = []
	for line in f.readlines():
		s= line.split()
		if s[0][0]=='#':
			srcdir = s[1]
			continue
		List.append(s)
	return srcdir, List


def prnBeauty(str, ment):
	#m = 9 - int (len(str)/4)
	m = 40 - len(str)
	#if len(str)%8 == 0: m-=1
	#if m < 1: m = 1
	print str, "-"*m, ment
	#print len(str), m

# compare A and B. if A is updated, copy A to B.
# 'A is updated' if A is newer than B, and the sizes are different.
# A is SOURCE, B is TARGET
# Element in the list is [filename, filesize, file_modified_time]
def cmpList(srcdir, dstdir, lista, listb, debug=0, docopy=0):
	sizea, sizeb = len(lista), len(listb)
	print sizea, sizeb
	a,b = 0,0
	for i in range( max(sizea, sizeb) ):
		if debug: 
			if a < sizea: namea=os.path.basename(lista[a][0])
			else: namea="---"
			if b < sizeb: nameb=os.path.basename(listb[b][0])
			else: nameb="---"
			print '\n',i, a, b, lista[a][0], listb[b][0], lista[a][1], listb[b][1], lista[a][2], listb[b][2]
		if b >= sizeb:
			prnBeauty( lista[a][0], "New")
			mkdir_ifnot_and_copy(srcdir, dstdir, lista[a][0], docopy)
			a = a+1
		elif a >= sizea:
			break
		elif lista[a]==listb[b]:
			a, b = a+1, b+1
		elif lista[a][0]<listb[b][0]:
			prnBeauty( lista[a][0], "New")
			mkdir_ifnot_and_copy(srcdir, dstdir, lista[a][0], docopy)
			a = a+1
		elif lista[a][0]>listb[b][0]:
			#prnBeauty( listb[b][0], "??")
			b = b+1
		elif lista[a][1]!=listb[b][1]:  # different size
			# if source is newer & bigger
			#if lista[a][2] > listb[b][2] and lista[a][1] > listb[b][1]:
			if lista[a][2] > listb[b][2]:
				prnBeauty( lista[a][0], "Upd")
				mkdir_ifnot_and_copy(srcdir, dstdir, lista[a][0], docopy)

				#print lista[a][0],'\t',\
				print '\t\t\t\t\t\t',\
						goodTime(listb[b][2]), listb[b][1], "-->",\
						goodTime(lista[a][2]), lista[a][1]
			# if source is older
			elif lista[a][2] < listb[b][2]:
				prnBeauty( listb[b][0], "Mod")
				print "\t\t\t\t\t\t",goodTime(listb[b][2]), listb[b][1], "<-->",\
						goodTime(lista[a][2]), lista[a][1]
			else:
				pass
			a, b = a+1, b+1
		# same size & source is newer
		elif lista[a][2] > listb[b][2]:
			if not filecmp.cmp(os.path.join(srcdir, lista[a][0]), os.path.join(dstdir, listb[b][0])):
				prnBeauty( lista[a][0], "same size, but Upd")
				mkdir_ifnot_and_copy(srcdir, dstdir, lista[a][0], docopy)
				print "\t\t\t\t\t\t",goodTime(listb[b][2]), listb[b][1], "<-->",\
						goodTime(lista[a][2]), lista[a][1]
			a, b = a+1, b+1
		else:
			a, b = a+1, b+1

####
def prnList(List, fname="", firstline=""):
	if fname=="":
		fd = sys.stdout
	else:
		try: 
			fd = open(fname, "w")
		except:
			print "file writing FAILED: %s" % fname
			fd = sys.stdout

	if firstline!="":
		print >>fd, firstline

	for e in List: print >>fd, e[0], e[1], e[2]
	


### main()
if __name__=="__main__":
#prn_f_size_n_mtime(sys.argv[0])
	#walktree("/home/dahee/HLRSVC")
	os.chdir("/home/dahee/HLRSVC")
	#print os.getcwd()
	pList = extList(".c, *.h,  *.script, *Jamfile, *cshrc*")
	listA = walktree("~/dahee_UAHLR_REL_0_6/hlrsvc/HLRSVC", pList, [] )
	listB = walktree("/home/dahee/HLRSVC", pList, [] )

	#listA =  readList("a")
	#listB =  readList("b")
	listA.sort()
	listB.sort()

	for e in listA: print e
	for e in listB: print e
	cmpList(listA, listB, debug=1)
