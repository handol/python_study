#!/usr/bin/env python

import os
import stat
import dircache
import fnmatch
import os.path
import shutil
import time


I_RPT_PASSED				= 0
I_RPT_COPIED				= 1
I_RPT_REPLACED				= 2

		
def syncDir( dfrom, dto, files, recursive = 0 ):
	dfrom = os.path.abspath( dfrom )
	dto = os.path.abspath( dto )

	report = [ 0, 0, 0 ]
	doSyncDir( report, dfrom, dto, files, recursive )
	return report

def doSyncDir( report, dfrom, dto, files, recursive = 0 ):

	# files == file extenstions : ex) .c,.h,.script
	#
	# copy files
	#

	fileList = files.split(",")	
	
	filesInSrc = dircache.listdir(dfrom);
	for f in filesInSrc:
		spath = dfrom + "/" + f
		dpath = dto + "/" + f
		
		if ( os.path.isfile( spath ) ):
			for c in fileList:
				c = c.replace(" ","") # remove spaces
				if fnmatch.fnmatch( f, c ):
					# marker is filled or updated when necessary
					copyIfDiffAndNew( report, spath, dpath)
		
		elif ( os.path.isdir( spath ) ):
			if ( recursive ):
				doSyncDir( report, spath, dpath, files, recursive = 1)

	print "# %s --> %s" %(dfrom, dto)


def isToCopy( dpath, spath):
	"""
	precond : dpath, spath exists
	"""
	cmd = "diff %s %s | wc -l " %(dpath, spath)
	w = os.popen(cmd).readline().split()	
	if (w[0]=="0" ):
		return 1
	else: 
		return 0


def copyIfDiffAndNew( report, spath, dpath):
	"""
	
	"""

	PASS	= 0x00
	CREATE  = 0x01
	REPLACE = 0x02
	MKDIR   = 0x10
	BACKUP	= 0x20

	filename = os.path.basename( spath )
	dirname = os.path.dirname(dpath)
	mtimeSrc = int( os.stat( spath )[ stat.ST_MTIME ] )	

	action = PASS
	
	if ( os.path.exists( dirname )) :
		if os.path.exists( dpath ):
			mtimeDst = int( os.stat( dpath )[ stat.ST_MTIME ] )
			if (mtimeSrc > mtimeDst ) :
				# same file exist
				if isToCopy( dpath, spath) :
					action |= REPLACE	
		else:
			# if no dest file
			action |= CREATE
		
	else:
		# if no dest dir
		os.makedirs( dirname )
		os.chmod( dirname, 0777 )
		action |= ( MKDIR | CREATE )

		
			
	if ( action & ( CREATE | REPLACE ) ):
		#print "copy^^"
		shutil.copyfile( spath, dpath )
		#os.chmod( dpath, 0777 )


	CHECK_TITLE_LEN = 60
	rs = "%s" % spath
	rs += " " * ( CHECK_TITLE_LEN - len(rs) )
	if ( action == 0): rs += "  skip"
	if ( action & CREATE ): rs += "  New"
	if ( action & REPLACE ): rs += "  Update"
	if ( action & MKDIR ): rs += "  Mkdir"
	
	print rs


	#report
	if ( action == PASS ):		report[ I_RPT_PASSED ] += 1
	elif ( action & CREATE ):		report[ I_RPT_REPLACED ] += 1
	elif ( action & REPLACE ):		report[ I_RPT_COPIED ] += 1


