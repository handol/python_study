#!/usr/bin/env python
import sys
import random

# memory manager dict
MMD = {}

# memory dict
MD = {}


##
# info == "[588C70]  PL A 4K 4K".split()
# info == "[588C70]  PL F 4K".split()
# info == "[588C70]  OS A 4K 4K".split()
# info == "[588C70]  OS F 4K".split()
def md_doit(flds):
	global MMD, MD
	#print flds
	if len(flds) < 4: 
		return

	memaddr = int(flds[0][1:-1], 16)
	blocksize = int(flds[3][:-1])
	#print "%X" % memaddr, blocksize

	#try:
	#	info = MMD[blocksize]
	#except:
	#	MMD[blocksize] = [0,0,0,0]

	mmdinfo = MMD.get(blocksize, [0,0,0,0])
	mdinfo = MD.get(memaddr, [0,0,0,0])

	if flds[1]=='OS':
		idx = 0
	else:
		idx = 2
	if flds[2]=='F':
		idx += 1
	
	mmdinfo[idx] += 1
	mdinfo[idx] += 1
	MMD[blocksize] = mmdinfo
	MD[memaddr] = mdinfo
	#print mmdinfo
	#print MMD, MD

			

def prn_mmd():
	global MMD, MD
	print '='*40, "Mem Manger"
	for k,v in MMD.iteritems():
		print "%dK\t" % k, v, v[2]-v[3]
	print '-'*40
	print

def prn_md():
	global MMD, MD
	print '='*40
	for k,v in MD.iteritems():
		if v[2]-v[3] != 0:
			print "[%X]\t" % k, v, v[2]-v[3]
	print '-'*40
	print
				
				
	

def doit(memlogfile, starttime="00:00:00", endtime="23:59:59"):
	try:
		fd = open(memlogfile, 'r')
	except:
		print "file NOT found:", fname
		return

	for line in fd:
		flds = line.split()
		if len(flds) <= 1: continue
		if flds[0].count(':') != 2: continue
		if flds[0] >= starttime: break


	for line in fd:
		flds = line.split()
		if len(flds) <= 1: continue

		if flds[0].count(':') == 2 and flds[0] > endtime: break

		if flds[0].count(':') == 2:
			flds = flds[1:]
		if len(flds)==0: continue

		if flds[0].count(':') == 2:
			flds = flds[1:]
		if len(flds)==0: continue

		if flds[0][0]=='[':
			md_doit(flds)


	prn_mmd()
	prn_md()

if __name__=="__main__":
	print "usage: input_file start_time end_time"
	if len(sys.argv) > 2:
		doit(sys.argv[1], sys.argv[2], sys.argv[3])
	else:
		doit(sys.argv[1])
		


