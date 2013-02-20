import os
import sys

f = open('lott.dat', 'r')

for l in f.readlines():
	cols = l.split()
	if len(cols)==0: break

	nums=[]
	terms = int (cols[0])
	odds = int (cols[1])
	for i in range(odds):
		nums.append( int(cols[2+i]) )
	for i in range(6-odds):
		nums.append( int(cols[odds+3+i]) )

	nums.sort()

	print "%03d : %02d %02d %02d %02d %02d %02d" % (terms, nums[0],\
		nums[1], nums[2], nums[3], nums[4], nums[5])

