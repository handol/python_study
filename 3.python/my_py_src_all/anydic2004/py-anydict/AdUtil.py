#!/usr/bin/python
# -*- coding: EUC-KR -*-
# 2008/3/10

import readline

#
#
#
def getinput(prompt):
	while True:
		try:
			a = raw_input(prompt).strip()
		except: 
			a = '.'
		if a=='': continue
		else: break
	return a

#
#
def chrange(start, end):
	return map(chr, range(ord(start), ord(end)+1) )

#
# set operation on list object
# python 'set' does NOT support set operation on list.
# setA, setB must be in sorted order by the given cmpfunc

def	setOpAND(setA, setB, cmpfunc):
	setR = []
	idxA = idxB = 0
	while idxA < len(setA) and idxB < len(setB):
		cmp = cmpfunc(setA[idxA], setB[idxB])
		if cmp==0:
			setR.append(setA[idxA])
			idxA += 1
			idxB += 1
		elif cmp < 0:
			idxA += 1
		else:
			idxB += 1

	return setR

def setOpAND_NoEmpty(setA, setB, cmpfunc):
	R = setOpAND(setA, setB, cmpfunc)
	if len(R) > 0:
		print "setA %d setB %d ==> R %d" % (len(setA), len(setB), len(R))
		return R
	else:
		print "setA %d setB %d ==> 0 ==> setA" % (len(setA), len(setB))
		return setA
	

def setOpAND_NoEmpty_List(setList, cmpfunc):
	R = reduce(lambda x, y: setOpAND_NoEmpty(x, y, cmpfunc), setList)


if __name__=="__main__":
	
	A = [ [4,"handol"], [5, "handol"], [6, "yy"]]
	B = [ [2,"xxxx"], [5, "xxxx"], [6, "kkk"]]
	C = [ [2,"xxxx"], [5, "xxxx"]]
	D = [ [2,"xxxx"], [4, "xxxx"]]


	cmpf = lambda x,y: x[0]-y[0]
	R = setOpAND(A, B, cmpf)  ## A AND B
	print R

	R = setOpAND(R, C, cmpf)  ## A AND B AND C
	print R

	R = reduce(lambda x, y: setOpAND(x, y, cmpf), [A, B, C])
	print R

	R = reduce(lambda x, y: setOpAND(x, y, cmpf), [A, B, C, D])
	print R

	R = reduce(lambda x, y: setOpAND_NoEmpty(x, y, cmpf), [A, B, C, D])
	print R

	R = reduce(lambda x, y: setOpAND_NoEmpty(x, y, cmpf), [A, D, B, C])
	print R
