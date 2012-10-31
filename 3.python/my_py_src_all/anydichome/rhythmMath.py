#!/usr/bin/env python
########################################################
# 2008.1.24  handol@gmail.com
# 
# For vector implementation in python , 
# refer to http://www.math.okstate.edu/~ullrich/PyPlug/
########################################################

import math

## print out a given vector
def prnVector(vector, msg=''):
	#print ' '.join(map(str, vector))
	print msg + ' '.join(map(lambda x: "%-6.2f" % x, vector))
	#print vector

def vecToStr(vector, msg=''):
	return msg + ' '.join(map(lambda x: "%-6.2f" % x, vector))

def prnVectors(vectors):
	for v in vectors:
		print v

## simple vector add
def VectorAddition(v1, v2):
	v3 = map(lambda x, y: x+y, v1, v2)
	return v3

## simple vector sub
def VectorSubtraction(v1, v2):
	v3 = map(lambda x, y: x-y, v1, v2)
	#print "vector Sub:", v3
	return v3

## get the Euclidean Norm of a given vector
def EuclideanNorm(vector):
	res = 0
	for a in vector:
		res += a*a
		#print a, res
	return math.sqrt(res)

## Euclidean Norm == Euclidean distance
def EuclideanDistance(vector):
	return EuclideanNorm(vector)

## Distance between two vectors
def EuclideanDistance2(v1, v2):
	v3 = VectorSubtraction(v1, v2)
	return EuclideanNorm(v3)

## get the KSD distance of a given vector
def KsdDistance(vector):
	dist = 0
	for a in vector:
		dist += a*a
		#print a, res
	kdist = math.sqrt(dist/float(len(vector)))
	#print "Ksd Dist:: ", vector, " --> ", kdist
	return kdist


## Distance between two vectors
def KsdDistance2(v1, v2):
	v3 = VectorSubtraction(v1, v2)
	return KsdDistance(v3)


## Vector Normalization
def NormVector(vector):
	norm = EuclideanNorm(vector)
	normV = map(lambda v: v/norm, vector)
	return norm, normV



## get the Mean vector of the given vectors. == P
def getMeanVector(vectors):
	dimension = len(vectors[0])
	goodcnt = 0
	sumVector = [0] * dimension

	for v in vectors:
		if len(v) != dimension:
			continue
		goodcnt += 1
		sumVector = VectorAddition(sumVector, v)
	
	#print "Sum: ", sumVector
	meanVector = map(lambda x: x/float(goodcnt), sumVector)
	#print "Mean: ", meanVector

	return meanVector		
			
	
##
def getKsdAvgDistance(vectors, debug=0):
	meanVec = getMeanVector(vectors)
	if debug: print "Mean Vector = ", meanVec

	distSum = 0
	for v in vectors:
		vdiff = VectorSubtraction(v, meanVec)
		dist = KsdDistance(vdiff)
		distSum += dist
		#print v, "-", meanVec, "==", vdiff, "-->", dist
	avgDist = distSum/len(vectors)

	if debug: print "Avg dist = ", avgDist
	return meanVec, avgDist



### CLASS
class ksdModel:
	def __init__(self, vectors):
		self.learnVectors = vectors
		self.centerVec, self.avgDistToCenter = getKsdAvgDistance(self.learnVectors)
		self.centerSize = KsdDistance(self.centerVec)
		self.ratios = []

	def	diffToAvg(self, y):
		ydiff = VectorSubtraction(y, self.centerVec)
		distY = KsdDistance( ydiff )
		return distY

	def ratioToAvg(self, y):
		distY = self.diffToAvg(y)
		ratio = distY / self.avgDistToCenter
		return	ratio

	def getRatios(self):
		if len(self.ratios) > 0: 
			return self.ratios

		for v in self.learnVectors:
			self.ratios.append( self.ratioToAvg(v) )
		return self.ratios
		

## new interal measure
## old interval: b's press time - a's release time
## new interval: b's press time - a's press time
def	getNewIntervalVector(oldV):
	newVec = []
	halfLeng = len(oldV) / 2
	for i in range(halfLeng):
		newInterval = oldV[i*2] + oldV[i*2 + 1]
		newVec.append(oldV[i*2])	
		newVec.append(newInterval)	
	if len(newVec) < len(oldV):
		newVec.append(oldV[-1])	
	return newVec
		

def getNewVectors(vectors):
	newVectors = []
	for v in vectors:
		newVectors.append( getNewIntervalVector(v) )
	return newVectors

##
class myList:
	def __init__(self, arr):
		self.arr = arr
		self.sum = sum(self.arr)
		self.average = float(self.sum) / len(self.arr)
		
		## calculate deviation
		# (x-avg) ^ 2
		tmparr = map(lambda x: math.pow(x - self.average, 2), self.arr)
		# sum
		sumDev = sum(tmparr)
		
		self.deviation = math.sqrt(sumDev)


##### test #####
def testEuclidean(vector):
	print "-"*20
	prnVector(vector)
	norm, normV = NormVector(vector)
	print "Norm = ", norm
	print "NormV = ", normV
	print "-"*20
	print

## show
def doKsdDecision(vectors, y):
	meanVec, avgDist = getKsdAvgDistance(vectors)
	ydiff = VectorSubtraction(y, meanVec)
	distY = KsdDistance( ydiff )
	#print y, "-", meanVec, "==", ydiff, "-->", distY
	ratio = distY / avgDist
	print ratio
	


if __name__ == "__main__":
	print 'Content-Type: plain/text\n'

	v = [10, 20, 20, -10, 30]
	t = [1, 2, 3, 4, 3]
	t2 = [2, 3, 5, 5, 5]
	t3 = [3, 3, 4, 5, 1]
	t4 = [3, 4, 4, 6, 3]
	tall = [t, t2, t3]

	newV = getNewIntervalVector(v)
	prnVector(v)
	prnVector(newV)

	print "===== Old KSD"
	print tall
	m = ksdModel(tall)
	print "center:", m.meanVec
	ratios = m.getRatios()
	print "ratios:", ratios
	rr = myList(ratios)
	print "sum., avg, std dev:", rr.sum, rr.average, rr.deviation

	print "===== New KSD"
	tall2 = getNewVectors(tall)
	print tall2
	m2 = ksdModel(tall2)
	print "center:", m2.meanVec
	ratios2 = m2.getRatios()
	print "ratios:", ratios2
	rr2 = myList(ratios2)
	print "sum., avg, std dev:", rr2.sum, rr2.average, rr2.deviation
	



	#testEuclidean(t)
	#doKsdDecision(tall, t4)
		
