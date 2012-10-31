#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
import math
from Vector import Vector

def loadUserInfo(fname):
	fp = open(fname)
	userdict = {}
	for line in fp:
		flds = line.split(",")
		if len(flds) < 2: continue
		user = int(flds[0])
		numcoms = int(flds[1])
		userdict[user] = numcoms
	fp.close()
	return userdict

class DataList:
	def __init__(self):
		self.data =[]
		pass


	def load(self, fname):
		try:
			fp = open(fname)
		except:
			return 0

		for line in fp:
			self.data.append(Vector(line))	
		fp.close()

MIN_ITEMS_IN_CLUSTER = 5
class Cluster:
	def __init__(self):
		self.pi = 0.0
		self.radius = 0.0
		self.mean = None

	def prn(self):
		print "%f, %f, %s" % (self.pi, self.radius, self.mean.str())
	
class ClusterResult:
	def __init__(self, numcluster, expectationValue):
		self.numClusters = numcluster
		self.rissanen = expectationValue
		self.clusters = [None] * self.numClusters
		self.numItemsList = [None] * self.numClusters
		self.totalItems = 0
		self.cnt = 0

	def addCluster(self, cluster):
		if self.cnt >= len(self.clusters):
			return
		self.clusters[self.cnt] = cluster
		self.cnt += 1

	def prn(self):
		print "%d clusters, %f rissanen" % (self.numClusters, self.rissanen)
		for c in self.clusters:
			c.prn()
	
	def findSmallClusters(self):
		numItemsList = [0] * self.numClusters
		smallClsCount = 0
		smallsRatio = 0.0
		goodClusters = []
		for i in range(self.numClusters):
			numitems = self.totalItems * self.clusters[i].pi
			self.numItemsList[i] = math.ceil(numitems)
			if self.numItemsList[i] < MIN_ITEMS_IN_CLUSTER:
				smallsRatio += self.clusters[i].pi
				smallClsCount += 1
			else:
				goodClusters.append(self.clusters[i].mean)
		if smallClsCount:
			#print "small custers: %d / %d" % (smallClsCount, self.numClusters)
			#print "ratio: %f" % (smallsRatio)	
			pass
		
		numGoodClusters = self.numClusters - smallClsCount
		if smallsRatio >= 0.1:
			numGoodClusters += 1
		return numGoodClusters, goodClusters

		
	

## GMM result 파일에서 cluster 개수 구함.
def getClusterResult(resfile):
	try:
		fp = open(resfile)
	except:
		print "read failed", resfile
		return 0

	# number of clusters
	line = fp.readline()
	flds =  line.split()
	if len(flds) < 3: return None
	num = int(flds[1])

	# Rissanen
	line = fp.readline()
	flds =  line.split()
	if len(flds) < 2: return None
	riss = float(flds[1])
	clResult = ClusterResult(num, riss)

	for i in range(num):
		line = fp.readline()
		flds =  line.split(",")
		if len(flds) < 3: return None
		if len(flds) > 3: flds = flds[1:]

		flds = map(str.strip, flds)
		cluster = Cluster()
		cluster.pi = float(flds[0])
		cluster.radius = float(flds[1])
		cluster.mean = Vector(flds[2])
		clResult.addCluster(cluster)

	#clResult.prn()
	fp.close()
	return clResult
	

def wc(fname):
	try:
		fp = open(fname)
		return len(fp.readlines())
	except:
		return 0

def doit(userfile, dirname, extname):
	userdict = loadUserInfo(userfile)

	files = os.listdir(dirname)
	#print "all files: %d" % (len(files))

	filterfunc = lambda x: x.endswith(extname)
	files = filter(filterfunc, files)
	#print "filtered files: %d" % (len(files))

	for file in files:
		print "====", file
		basename = file.split(".")[0]
		numcoms = userdict.get(int(basename), 0)
		clResult = getClusterResult(file+".res")
		datalist = DataList()
		datalist.load(file)
		clResult.totalItems = numlines
		goodClsCount, goodClusters = clResult.findSmallClusters()
		clustering = Clustering.Cluster(datalist.data)
		clustering.runWithCenters(goodClusters, debug=1)
		print "%s, %d, %d, %d, %d, %f" % 
			(basename, numcoms, clResult.numClusters, goodClsCount,  numlines, clResult.rissanen)
		break
	
	

if __name__=="__main__":
	import sys
	clResult = getClusterResult("999593.intval.res")
	clResult.totalItems = 62
	clResult.findSmallClusters()
	clResult.prn()
	if len(sys.argv) > 3:
		doit(sys.argv[1], sys.argv[2], sys.argv[3])
	else:
		print "usage: userfile dirname fileextension"	
