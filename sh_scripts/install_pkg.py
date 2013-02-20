#!/usr/bin/env python
import os
import sys
import os.path
import time
#from shutil import copy, move

PKG_TRG_DIR = ''
PKG_ORG_DIR = ''

PKG_SUB_DIRS = [ 'slp', 'data', 'lib', 'bin', 'mmdb', 'log' ]
flag_compress = 0

TAR = '/usr/local/bin/tar'
TAR = '/usr/sbin/tar'
LOG = None

def	open_log(dir, name):
	log = name+'.' + time.strftime("%Y%m%d-%H%M", time.localtime())
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
		ans = raw_input("%s [full 'yes'] ? " % ment)
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


def confirm_src_trg_dirs(srcdir, trgdir):
	print
	print "SOURCE of package: %s" % (srcdir)
	print "TARGET of install: %s" % (trgdir)
	if LOG: LOG.write("SOURCE: %s" % (srcdir)+"\n")
	if LOG: LOG.write("TARGET: %s" % (trgdir)+"\n")
	return get_yes_confirm("Are you sure ??")


def check_trg_dir(trgdir):
	if not os.path.exists(trgdir):
		return 0

	found = 0
	print
	for subw in PKG_SUB_DIRS:
		dir = os.path.join(trgdir, subw)
		if os.path.isdir(dir):
			found += 1
			print "found %s " % (dir)
			if LOG: LOG.write("found %s " % (dir) + '\n')
		else:
			pass

	print
	if found:
		print "%s : already contains a package !" % trgdir
		if not get_yes_confirm("Replace the package"):
			print "packaging is Canceled !!"
			sys.exit(0)


def get_src_trg_dirs(src=None, trg=None):
	if src: PKG_ORG_DIR = src	
	if trg: PKG_TRG_DIR = trg	

def makedir_ifnot(dir):
	if not os.path.exists(dir):
		print "DIR created: ", dir
		os.makedirs(dir)


def remove_if_exist(fname):
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
		and uncompress it.
	'''
	for subw in PKG_SUB_DIRS:
		fname = os.path.join(srcdir, subw+".tar")
		if os.path.exists(fname):
			print "found %s in package" % (fname)
			if LOG: LOG.write("found %s in package" % (fname) + '\n')
		elif os.path.exists(fname+".Z"):
			fname += ".Z"
			print "uncompressing %s in package" % (fname)
			if LOG: LOG.write("uncompressing %s in package" % (fname) + '\n')

			exec_shell ("/bin/compress -dv %s" % fname)
		else:
			pass
		#	print fname, " is Missing !"
		#	print srcdir, "is NOT a valid package directory."
		#	return -1


def uncompress_tars(trgdir):
	print "\n===== uncompressing package"
	print "\tuncompressing 33 Mb takes about 10 seconds"
	if not get_confirm("Uncompress tar files"): return

	os.chdir(trgdir)
	exec_shell ("/bin/compress -dv *.tar.Z")
	exec_shell( "/bin/ls -l ")


def install_subdir_tar(srcdir, trgdir, subdir):
	xyztar = os.path.join(srcdir, "%s.tar" % subdir)
	if not os.path.exists(xyztar):
		print "\n===== not found, so skipping: %s" % subdir
		return

	print "\n===== installing package: %s ..." % subdir
	installdir = os.path.join(trgdir, subdir)
	makedir_ifnot(installdir)
	
	os.chdir(installdir)
	exec_shell ("%s -xf %s" % (TAR, xyztar) )
	#exec_shell( "/bin/ls -l %s" % xyztar)

def install_all_tar(srcdir, trgdir):
	for subw in PKG_SUB_DIRS:
		if subw=='mmdb' or subw=='log':
			install_subdir_tar(srcdir, trgdir, subw)

			#if get_confirm("install %s" % subw):
			#	install_subdir_tar(srcdir, trgdir, subw)

		else:
			install_subdir_tar(srcdir, trgdir, subw)


ALONE_SLP = [ 'sri', 'locu', 'gprs_locu', 'sms_sri', 'sms_delstat',
		'sms_readysm', 'stand_alone_cncloc']
ALONE_SLP = [ 'sri', 'locu', 'gprs_locu', 'gprs', 'call_gmap', 'reg_gmap' ]

def link_empty_slp(trgdir):
	if not os.path.exists(trgdir):
		return
	for f in ALONE_SLP:
		ff = f+".slp"
		newf = f+".1.slp"
		if os.path.exists(newf):
			os.remove(newf)
		exec_shell ("/bin/cp pagereq.slp %s" % (ff), prn=0 )
		exec_shell ("/bin/ln -s %s %s" % (ff, newf), prn=0 )
	

def link_slp_one(trgdir):
	slpdir = os.path.join(trgdir, "slp")
	makedir_ifnot(slpdir)
	os.chdir(slpdir)
	n = 0
	for f in os.listdir(slpdir):
		if not f.endswith('.slp'): continue
		if f.find('.1.')>=0: continue
		w = f.split('.')
		newf = w[0] + '.1.' + w[1]
		newf = newf.lower()
		if os.path.exists(newf):
			os.remove(newf)
		exec_shell ("/bin/ln -s %s %s" % (f, newf), prn=0 )
		n += 1

	print "%d slp files were linked." % (n)
	#exec_shell( "/bin/ls -l %s" % slptar)


def chmod_bin(trgdir):
	bindir = os.path.join(trgdir, "bin")
	os.chdir(bindir)
	exec_shell("/bin/chmod a+x *")
	
def install_package(srcdir, trgdir):
	if not confirm_src_trg_dirs(srcdir, trgdir): return -1
	check_src_dir(srcdir)
	check_trg_dir(trgdir)
	install_all_tar(srcdir, trgdir)

	link_slp_one(trgdir)
	link_empty_slp(trgdir)
	chmod_bin(trgdir)
	



if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "%s source_dir targer_dir" % (sys.argv[0])
		sys.exit(0)
	LOG = open_log(os.getcwd(), 'log.install')
	install_package(sys.argv[1], sys.argv[2])
	close_log(LOG)
