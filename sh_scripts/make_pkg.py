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



def get_yes_confirm(ment):
	try:
		ans = raw_input("\n%s [full 'yes'] ? " % ment)
	except:
		print "\nYou stopped me..."
		sys.exit(-1)	
	else:
		if ans=='yes': return 1
		else: return 0

   
def exec_shell(cmnd, prn=1):
	if prn: print os.getcwd(),'#',cmnd
	if prn and LOG: LOG.write(os.getcwd()+' # '+cmnd+"\n")
	res = os.popen(cmnd, 'r').readlines()
	for r in res:
		if prn: print r[:-1]
		if prn and LOG: LOG.write(r)

def exec_shell2(cmnd):
	print cmnd
	res = os.system(cmnd)
	#os.wait()
	return res

def confirm_src_trg_dirs(srcdir, trgdir):
	print
	print "ORG: %s" % (srcdir)
	print "TRG: %s" % (trgdir)
	if LOG: LOG.write("ORG: %s" % (srcdir)+"\n")
	if LOG: LOG.write("TRG: %s" % (trgdir)+"\n")
	return get_yes_confirm("Are you sure ??")

def get_src_trg_dirs(src=None, trg=None):
	if src: PKG_ORG_DIR = src	
	if trg: PKG_TRG_DIR = trg	

def makedir_ifnot(dir):
	if not os.path.exists(dir):
		print "DIR created: ", dir
		os.makedirs(dir)


def remove_if_exist(fname):
	# we got confirm for the whole directory at start of the script.
	# so, we don't need a confirmation for each file.
	return 0

	if not os.path.exists(fname): return 0

	print "'%s' already exists." % (fname)
	if get_confirm("replace this file"):
		os.remove(fname)
		return 0
	else: 
		return -1


def count_files_with_ext(dir, ext):
	''' count files with 'ext' in 'dir'
	ex) /hlrhome/lib, .so
	'''
	n = 0
	for f in os.listdir(dir):
		if f.endswith(ext): n += 1
	return n
	

def check_src_dir(srcdir):
	''' check if the given source directory is valid one.
	'''
	for subw in PKG_SUB_DIRS:
		dir = os.path.join(srcdir, subw)
		if not os.path.isdir( dir ): 
			print dir, "NOT exists !"
			print srcdir, " is NOT valid package directory"
			return -1
	return 0



def check_trg_dir(trgdir):
	if not os.path.exists(trgdir):
		return 0

	found = 0
	print
	for subw in PKG_SUB_DIRS:
		fname = os.path.join(trgdir, subw+".tar")
		if os.path.exists(fname):
			found += 1
			print "found %s " % (fname)
			if LOG: LOG.write("found %s " % (fname) + '\n')
		elif os.path.exists(fname+".Z"):
			found += 1
			fname += ".Z"
			print "found %s " % (fname)
			if LOG: LOG.write("found %s " % (fname) + '\n')

		else:
			pass

	print
	if found:
		
		print "%s : already contains a package !" % trgdir
		if not get_yes_confirm("Replace the package"):
			print "packaging is Canceled !!"
			sys.exit(0)
			


def move_core_in_bin_dir(srcdir):
	print "trying to move 'core' files ..."
	bindir = os.path.join(srcdir, "bin/")
	coredir = os.path.join(srcdir, "cores/")
	makedir_ifnot(coredir)
	exec_shell("/bin/mv %score* %s" % (bindir, coredir) )


def compress_tars(trgdir):
	print "\n===== compressing package"
	print "\tcompressing 80 Mb takes about 20 seconds"
	#if not get_confirm("Compress tar files"): return

	os.chdir(trgdir)
	for f in os.listdir(trgdir):
		if not f.endswith('.tar'): continue
		print "-- compressing %s" % f
		exec_shell ("/bin/compress -fv %s" % f)

	exec_shell("/bin/chmod a+w *.tar.Z")
	exec_shell( "/bin/ls -l ")


def make_subdir_tar(srcdir, trgdir, subdir):
	print "\n===== packaging %s ..." % subdir
	xyzdir = os.path.join(srcdir, "%s/" % subdir)
	xyztar = os.path.join(trgdir, "%s.tar" % subdir)
	if remove_if_exist(xyztar) < 0: return -1
	
	os.chdir(xyzdir)
	exec_shell ("/usr/local/bin/tar -cf %s *" % (xyztar) )
	exec_shell( "/bin/ls -l %s" % xyztar)

def make_bin_tar(srcdir, trgdir):
	print "\n===== packaging bin ..."
	bindir = os.path.join(srcdir, "bin/")
	bintar = os.path.join(trgdir, "bin.tar")
	if remove_if_exist(bintar) < 0: return -1
	
	os.chdir(bindir)
	exec_shell ("/usr/local/bin/tar -cf %s *" % (bintar) )
	exec_shell( "/bin/ls -l %s" % bintar)


def make_data_tar(srcdir, trgdir):
	print "\n===== packaging data ..."
	datadir = os.path.join(srcdir, "data/")
	datatar = os.path.join(trgdir, "data.tar")
	if remove_if_exist(datatar) < 0: return -1
	
	os.chdir(datadir)
	exec_shell ("/usr/local/bin/tar -cf %s *" % (datatar) )
	exec_shell( "/bin/ls -l %s" % datatar)


def make_lib_tar(srcdir, trgdir):
	print "\n===== packaging lib ..."
	libdir = os.path.join(srcdir, "lib/")
	libtar = os.path.join(trgdir, "lib.tar")
	if remove_if_exist(libtar) < 0: return -1
	
	cnt = count_files_with_ext(libdir, ".so")
	print "%d '.so' file in '%s'" % (cnt, libdir)
	if LOG: LOG.write("%d '.so' file in '%s'" % (cnt, libdir)+"\n")

	os.chdir(libdir)
	exec_shell ("/usr/local/bin/tar -cf %s *.so" % (libtar) )
	exec_shell( "/bin/ls -l %s" % libtar)


def make_slp_tar(srcdir, trgdir):
	print "\n===== packaging slp ..."
	slpdir = os.path.join(srcdir, "slp/")
	slptar = os.path.join(trgdir, "slp.tar")
	if remove_if_exist(slptar) < 0: return -1
	
	os.chdir(slpdir)
	n = 0
	for f in os.listdir(slpdir):
		if not f.endswith('.slp'): continue
		if f.find('.1.')>=0: continue
		exec_shell ("/usr/local/bin/tar -rf %s %s" % (slptar, f), prn=0 )
		n += 1

	print "%d slp files were packaged." % (n)
	exec_shell( "/bin/ls -l %s" % slptar)


def make_package(srcdir, trgdir, comp_flag=1):
	if not confirm_src_trg_dirs(srcdir, trgdir): return -1
	if check_src_dir(srcdir) < 0: return -1
	check_trg_dir(trgdir)
	makedir_ifnot(trgdir)
	exec_shell("/bin/chmod a+wx %s" % trgdir)
	make_slp_tar(srcdir, trgdir)
	make_data_tar(srcdir, trgdir)
	make_lib_tar(srcdir, trgdir)
	move_core_in_bin_dir(srcdir)
	make_bin_tar(srcdir, trgdir)
	if comp_flag:
		compress_tars(trgdir)


def backup_package(srcdir, trgdir, comp_flag):
	if not confirm_src_trg_dirs(srcdir, trgdir): return -1
	if check_src_dir(srcdir) < 0: return -1
	check_trg_dir(trgdir)
	makedir_ifnot(trgdir)
	exec_shell("/bin/chmod a+wx %s" % trgdir)
	make_slp_tar(srcdir, trgdir)
	make_subdir_tar(srcdir, trgdir, "data")
	make_lib_tar(srcdir, trgdir)
	move_core_in_bin_dir(srcdir)
	make_subdir_tar(srcdir, trgdir, "bin")
	make_subdir_tar(srcdir, trgdir, "mmdb")
	make_subdir_tar(srcdir, trgdir, "log")
	if comp_flag:
		compress_tars(trgdir)



if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "%s source_dir targer_dir [-backup] [-nocomp]" % (sys.argv[0])
		print "\t-nocomp: no compressing of tar files"
		print "\t-backup: backup a package including 'mmdb' and 'log' directory"
		print "ex) %s ~/hlrhome/ /tmp/pkg9"
		sys.exit(0)

	backup = 0
	compflag = 1
	for a in sys.argv:
		if a=='-backup': backup = 1
		if a=='-nocomp': compflag = 0

	if backup:
		LOG = open_log(os.getcwd(), 'log.backup')
		backup_package(sys.argv[1], sys.argv[2], compflag)
	else:
		LOG = open_log(os.getcwd(), 'log.packaging')
		make_package(sys.argv[1], sys.argv[2], compflag)
	close_log(LOG)
