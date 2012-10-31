
def doit(fname):
	fp = open(fname)
	arr = []
	for line in fp:
		flds = line.split()
		arr += flds

	arr.sort()
	for a in arr:
		print '"%s", ' % (a)

doit("megastudy_user.txt")
		
