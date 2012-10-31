import sys

import dictWithCnt

fd = open(sys.argv[1], "r")


d = dictWithCnt.DictWithCnt()

for line in fd:
	flds = line.split()
	if len(flds) < 12:
		f = flds[6]
		
	else:
		f = flds[7]

	d.add(f)
	#print f


d.prn()
