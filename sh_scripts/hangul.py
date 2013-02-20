### 
#-*- #oding: euc-kr -*-
import sys
import os

f = open(sys.argv[1])

n=0
while 1:
	line = f.readline()
	#print line
	if line.find("¿¹¹®")>=0:
		print line
	else:
		continue
	s = line.split()
	for i in range(len(s)):
		print "\t-\t",s[i]
	n += 1
	if n>10: break
