### 
#-*- #oding: euc-kr -*-
import sys
import os

f = open(sys.argv[1])

n=0
while 1:
	line = f.readline().strip()
	if line and line[0]=='#': continue

	n += 1
	print line
	print len(line.split())
	if n>10: break
