#!/usr/bin/python

import DbChamDemo
def getFileList(dirname, fileext):
	import os
	
	result = [ f for f in os.listdir(dirname) if f.endswith(fileext)]
	return result


def	parseMcdFile(mcdfile):
	result = []
	fd = open(mcdfile, "r")
	for line in  fd:
		flds = line.split()
		if len(flds) <= 1: continue
		result.append(flds)
	return result


def mobileId(id):
	return "mobile_" + id

def isNewId(db, id):
	uid = db.getUid(mobileId(id)) 
	return (uid == 0)

def isPasswdCorrect(db, id, passwd):
	uid = db.getUid(mobileId(id)) 
	return (uid == 0)
	
	
def insertUid(db, dirname, filelist):
	for file in filelist:
		id = file.split(".")[0]
		try:
			fname = "%s/%s" % (dirname, file)
			patterns = parseMcdFile(fname)
			dim = len(patterns[0])
		except:
			print "ERROR in file", file
			continue

		# check if the id exists already
		
		if db.getUid(mobileId(id)) != 0:
			print "'%s' exists already' % (mobileId(id))
			continue

		try:
			db.insertUid(mobileId(id), dim)
		except:
			print "ERROR in DB", file
			continue

IPADDRS = ["211.234.187.4", "203.226.193.192", \
	"203.226.200.171", "211.234.187.16", \
	"211.235.133.233", "59.5.42.3",  "211.115.25.156", \
	"147.46.94.177",  "211.234.198.77", "211.234.201.202" ]
	

def insertKsdlog(db, dirname, filelist):
	import random

	for file in filelist:
		id = file.split(".")[0]
		try:
			fname = "%s/%s" % (dirname, file)
			patterns = parseMcdFile(fname)
		except:
			print "ERROR in file", file
			continue

		uid = db.getUid("mobile_"+id)
		if uid==0:
			print "uid error for id '%s'" % (id)
			continue
		

		for i,vec in  enumerate(patterns):
			ksdvec = ' '.join(vec)
			ipaddr = random.choice(IPADDRS)
			logtime = len(patterns) - i + 1
			try:
				db.insertKsdlog(uid, ipaddr, logtime, ksdvec )
			except:
				print "ERROR in DB", file
			
		
if __name__ == "__main__":
	filelist =  getFileList("users", ".mcd")

	db = DbChamDemo.login()
	##insertUid(db, "users", filelist)
	insertKsdlog(db, "users", filelist)
