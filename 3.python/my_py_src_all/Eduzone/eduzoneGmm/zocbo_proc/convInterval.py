#!/usr/bin/env python


def makeIntervals(nums):
	res = [0]*(len(nums)/2)
	for i in range(len(res)):
		res[i] = nums[2*i] + nums[2*i+1]
	return res

def convOnlyInterval(fname):
	try:
		fp = open(fname+".dat")
	except:
		print "read failed", fname
		return

	
	out = open(fname+".intval", "w")

	linecnt = 0
	dim = 0
	for line in fp:
		linecnt += 1
		nums = map(int, line.split())
		res = makeIntervals(nums)
		dim = len(res)
		#print nums, res
		convline = " ".join(map(str, res))
		out.write(convline)
		out.write("\n")

	fp.close()
	out.close()

	infoout = open(fname+".intval.info", "w")
	infoout.write("1\n")
	infoout.write("%d\n" % dim)
	infoout.write("%s.intval %d\n" % (fname, linecnt))
	infoout.close()	
	
	print fname+".intval", fname+".intval.info", dim, linecnt


if __name__=="__main__":
	import sys
	if len(sys.argv) > 1:
		convOnlyInterval(sys.argv[1])
	else:
		print "enter file name"	
