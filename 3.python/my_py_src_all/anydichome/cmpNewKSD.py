#!/usr/bin/env python
import ksdMySQL
import rhythmMath

def	getConsistency(vectors, debug=0):
	if debug: rhythmMath.prnVectors(vectors)
	m = rhythmMath.ksdModel(vectors)
	if debug: rhythmMath.prnVector(m.centerVec, "center:")
	ratios = m.getRatios()
	if debug: rhythmMath.prnVector(ratios, "ratios:")
	rr = rhythmMath.myList(ratios)
	ksdDevi = rhythmMath.KsdDistance(ratios)
	if debug: print "sum., avg, std dev:", rr.sum, rr.average, rr.deviation, ksdDevi
	if debug: print 
	return rr.deviation


def doit(auser=''):
	allData = ksdMySQL.loadTable('localhost', 'root', 'wpxk00', 'rhythmpass_web')

	oldBetter = 0
	newBetter = 0
	sameCnt = 0

	oldC = []
	newC = []
	
	debug = 0
	if auser != '': 
		debug = 1

	cnt = 0
	for user, vectors in allData.iteritems():
		if auser != '' and auser != user:
			continue
		cnt += 1
			
		if debug: print "--------- Old KSD"
		c1 = getConsistency(vectors, debug)

		newVectors = rhythmMath.getNewVectors(vectors)
		if debug: print "--------- new KSD"
		c2 = getConsistency(newVectors, debug)

		oldC.append(c1)
		newC.append(c2)

		if c1 > c2:
			newBetter += 1
		elif c1 < c2:
			oldBetter += 1
		else:
			sameCnt += 1

		
		print "%15s  %0.3f  %0.3f" % (user, c1, c2)

	print "----------------------------"
	print "SUM: old= %0.3f  new= %0.3f" % ( sum(oldC), sum(newC) )
	print "AVG: old= %0.3f  new= %0.3f" % ( sum(oldC)/cnt, sum(newC)/cnt )
	print "----------------------------"
	print "Old = %d, New = %d, Even = %d" % (oldBetter, newBetter, sameCnt)



if __name__=="__main__":
		print 'Content-Type: text/plain\n'
		doit()
		print "===== bighands ====="
		doit("bighands")
		print "===== bob ====="
		doit("bob")

