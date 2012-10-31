import sys

def	loadDomainCnt(filename):
	print "file:", filename
	try:
		fd = open(filename, "r")
	except:
		print "fail to read", filename
		return

	D = {}
	
	for line in fd:
		flds = line.split()
		if len(flds) < 2: continue
		try:
			D[flds[1]] = int(flds[0])
		except:
			print "failed line:", flds

	print "Size=%d" % len(D)
	return D



def compareDomainCnt(dA, dB):
	res = []
	for k,v in dA.iteritems():
		try:
			if dB[k] >= v*1.5 and v >= 400:
				res.append([k, dB[k], v])
				#print "%s %d %d"  % ( k, dB[k], v )
		except:
			if v>100:
				print "Only in A: %s %d"  % ( k, v )
			pass


	res.sort(cmp=lambda x,y: cmp(x[1], y[1]))
	for i in res:
		print "%25s\t%d\t%d" % (i[0], i[1], i[2])

dA = loadDomainCnt(sys.argv[1])
dB = loadDomainCnt(sys.argv[2])

compareDomainCnt(dA, dB)

