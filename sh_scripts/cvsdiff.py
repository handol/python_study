#!/usr/bin/env python
import os
import sys
import os.path
import time
#from shutil import copy, move

PKG_TRG_DIR = ''
PKG_ORG_DIR = ''

PKG_SUB_DIRS = [ 'slp', 'data', 'lib', 'bin' ]
flag_compress = 0

LOG = None

def	open_log(dir, name):
	log = name+'.'+ time.strftime("%Y%m%d-%H%M", time.localtime())
	fname = os.path.join(dir, log)
	try:
		fd = open(fname, "w")
		print "logfile = %s" % (fname)
		fd.write("\n===== starts at %s\n" % \
			time.strftime("%Y/%m/%d-%H:%M:%S", time.localtime()) )
	except:
		fd = None
		print "Cannot write logfile = %s" % (fname)
	return fd


def close_log(fd):
	if fd:
		fd.write("\n===== ends at %s\n" % \
			time.strftime("%Y/%m/%d-%H:%M:%S", time.localtime()) )
		fd.close()


def get_confirm(ment):
	try:
		ans = raw_input("\n%s [y/n] ? " % ment)
	except:
		print "\nYou stopped me..."
		sys.exit(-1)	
	else:
		if ans[0]=='y': return 1
		else: return 0


def exec_shell(cmnd, prn=1):
	#if prn: print os.getcwd(),'#',cmnd
	if prn: print cmnd
	if prn and LOG: LOG.write(os.getcwd()+' # '+cmnd+"\n")
	res = os.popen(cmnd, 'r').readlines()
	for r in res:
		if prn: print r[:-1]
		if prn and LOG: LOG.write(r)
	return res


def makedir_ifnot(dir):
	if not os.path.exists(dir):
		print "DIR created: ", dir
		os.makedirs(dir)


def get_version_num(cvss):
	ver = []
	for line in cvss:
		arr = line.split()
		if len(arr)>=3 and arr[1]=='revision:':
			ver.append(arr[2])
	return ver

def my_cvs_diff(filename, verdiff=1):
	res_cvs_status = exec_shell("cvs status %s" % (filename))
	ver = get_version_num(res_cvs_status)
	if len(ver)<2: return 0

	if ver[0]==ver[1]:
		s = ver[1].split('.')
		n = int(s[1]) - verdiff
		ver[1] = '%s.%d' % (s[0], n)

	resfile = "diff.%s.%s_%s" % (filename, ver[0], ver[1])

	#cmd = 'cvs diff -r %s -r %s %s > %s' \
	#	% (ver[0], ver[1], filename, resfile)
	cmd = 'cvs diff -r %s -r %s %s ' \
		% (ver[0], ver[1], filename)

	exec_shell(cmd)

	print "\nresult:: %s" % (resfile)


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "%s sourcefile [version] " % (sys.argv[0])
		sys.exit(0)

	if len(sys.argv)>2: vers = int(sys.argv[2])
	else: vers = 1

	my_cvs_diff(sys.argv[1], vers)
	#LOG = open_log(os.getcwd(), 'log.backup')



	#close_log(LOG)
