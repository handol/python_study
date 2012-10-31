#!/usr/bin/env python
########################################################
# 2008.3.12  handol@gmail.com
########################################################

import math
import time
import random
import sys
from Vector import * 

class Cluster(object):
	## Constructor: give initial item set (data set)
	def __init__(self, itemset=[]):
		# itemset must be a list of objects of Vector class
		self.debug = 0
		self.loop = 0
		self.iteminfo = []

		random.seed(time.time())

		if len(itemset)==0:
			return

		## one iteminfo = [item, distance to centroid, cluster id]

		self.dim = len(itemset[0])
		for i in range(len(itemset)):
			if len(itemset[i]) != self.dim: ## check dimenstion
				continue
			self.iteminfo.append([ itemset[i], None, None])  

		self.clusterDistanceMatrix = []
		
	## add a new item
	def add(self, item):
		self.iteminfo.append([item[i], None, None])
	
	def runWithCenters(self, centers, debug=0):
		for c in centers:
			self.cluster[i][0] = c

		self.k = len(centers)
		change = self.assignClusterToItem()
		#if debug: self.prnItemInfo()
		self.calcCentroid()
		if debug: self.prnCluster()



	def run(self, k, debug=0):
		self.debug = debug
		if len(self.iteminfo) == 0:
			return

		self.k = k
	
		## Cluster = [centroid(vector), # of items, radius]

		self.cluster = []
		for i in range(self.k):
			self.cluster.append([None, None, None ])  
		
		self.setInitialCentroid()
		if self.k >= 2:
			self.getMinMaxItems()
			self.cluster[0][0] = self.itemMAX
			self.cluster[1][0] = self.itemMIN
			if debug: print self.itemMAX.str()
			if debug: print self.itemMIN.str()
			if self.k >= 3:	
				self.cluster[2][0] = self.itemMEAN
				if debug: print self.itemMEAN.str()
		

		#self.prnCluster()

		while True:
			self.loop += 1
			change = self.assignClusterToItem()

			if self.debug: self.prnItemInfo()
			if change == 0:
				break

			self.calcCentroid()

			if self.debug: self.prnCluster()

		self.calcCentroid()
		self.calcRadius()

		# sort Clusters
		self.cluster = filter(lambda c: c[1] > 0, self.cluster)
		self.k = len(self.cluster)

		cmpfunc = lambda x,y: x[1]-y[1]  ## sort by the number of items in the cluster
		self.cluster.sort(cmpfunc)

		self.calcIntraClusterDistance()
	
	## randomly select the initial centroids
	def setInitialCentroid(self):
		randlist = random.sample(range(len(self.iteminfo)), self.k)

		for i,r in zip(range(self.k), randlist):
			#self.prnCluster()
			self.cluster[i][0] = self.iteminfo[r][0]
		if self.debug: self.prnCluster()

	
	## find the nearest cluster of a given item
	## return: the cluster id, the distance to the centroid
	def findNearestCentroid(self, item):
		mindist = 1000000
		nearest = -1  # nearest cluster
		for idx, cluster in enumerate(self.cluster):
			v = item - cluster[0]
			distance = v.ksdsize()
			if distance < mindist:
				mindist = distance
				nearest = idx
		return nearest, mindist
				
			
	## assign each item to its nearest cluster
	## return: the number of items whose cluster has changed
	def assignClusterToItem(self):		
		changeCount = 0
		for idx, item in enumerate(self.iteminfo):
			#print idx
			#item.prn()
			prev_c = self.iteminfo[idx][1]
			self.iteminfo[idx][1], self.iteminfo[idx][2] = self.findNearestCentroid(item[0])
			if prev_c != self.iteminfo[idx][1]:
				changeCount += 1
				#print "CHANGE: %d --> %d" % (prev_c, self.iteminfo[idx][1])
		return changeCount

	def calcCentroid(self):
		# init cluster info
		for c in self.cluster:
			c[0] = Vector(self.dim)
			c[1] = 0

		# calc centroid: SUM of all items in each cluster
		for idx, info in enumerate(self.iteminfo):
			c = self.cluster[info[1]]
			c[0] += self.iteminfo[idx][0]
			c[1] += 1
			#print "Item[%d] --> Cluster[%d]" % (idx, info[1])

		# calc centroid: AVG of all items in each cluster
		for c in self.cluster:
			if c[1] > 0:
				#c[0] = c[0] / c[1]
				c[0] /= c[1]

	def	calcRadius(self):
		# init cluster info
		for c in self.cluster:
			c[2] = 0.0

		for idx, info in enumerate(self.iteminfo):
			c = self.cluster[info[1]]
			diff = info[0] - c[0]
			c[2] += diff.ksdsize()

		for c in self.cluster:
			if c[1] > 0:
				c[2] = c[2] / c[1]

	def getMinMaxItems(self):
		self.itemMAX = Vector(self.iteminfo[0][0])
		self.itemMIN = Vector(self.iteminfo[0][0])
		self.itemMEAN = Vector(self.iteminfo[0][0])
		for idx in range(1, len(self.iteminfo)):
			self.itemMAX.upper( self.iteminfo[idx][0] )
			self.itemMIN.lower( self.iteminfo[idx][0] )
			self.itemMEAN += self.iteminfo[idx][0]
			#print self.iteminfo[idx][0].str()
			#print self.itemMAX.str()
			#print self.itemMIN.str()
		self.itemMEAN /= len(self.iteminfo)

	def calcIntraClusterDistance(self, debug=0):
		#if len(self.cluster) < 2:
		#	return

		for i in range(self.k):
			self.clusterDistanceMatrix.append([None] * self.k)

		for i in range(self.k):
			for j in range(i+1):
				if i==j:
					self.clusterDistanceMatrix[i][j] = 0.0
					continue
				
				D = self.cluster[i][0] - self.cluster[j][0]
				self.clusterDistanceMatrix[i][j] = self.clusterDistanceMatrix[j][i] = D.ksdsize()
				#print "%d %d : %.2f" % (i,j, D.ksdsize())
				if debug: print "Intra: %d %d : %.2f" % (i,j, self.clusterDistanceMatrix[i][j])
				

	def prnIntraCluster(self, fd=sys.stdout):
		if self.clusterDistanceMatrix == None:
			return
		
		print "-"*10, "Intra-Cluster Distance"
		for i in range(self.k):
			for j in range(self.k):
				fd.write("%.2f\t" % (self.clusterDistanceMatrix[i][j]))
			fd.write("\n")

		print "-"*10, "Intra-Cluster Distance / each radius"
		for i in range(self.k):
			for j in range(self.k):
				try:
					ratio = self.clusterDistanceMatrix[i][j] / self.cluster[i][2]
					fd.write("%.1f\t" % (ratio))
				except:
					fd.write("NA\t")
			fd.write("\n")
		print "-"*10, "Intra-Cluster Distance / sum of two radius"
		for i in range(self.k):
			for j in range(self.k):
				try:
					ratio = self.clusterDistanceMatrix[i][j] / (self.cluster[i][2] + self.cluster[j][2])
					fd.write("%.1f\t" % (ratio))
				except:
					fd.write("NA\t")
			fd.write("\n")
		print "-"*20

	def	prnItemset(self):
		for idx, info in enumerate(self.iteminfo):
			print "I[%2d]: [%s]" % (idx, self.iteminfo[idx][0].str())
		

	def	prnItemInfo(self):
		for idx, info in enumerate(self.iteminfo):
			print "I[%2d]: C-%d %.2f" % (idx, self.iteminfo[idx][1], self.iteminfo[idx][2])
		
	def	prnCluster(self):
		#for c in self.cluster:
		#	print "CLUSTER ID:", id(c), id(c[0]), id(c[1])
		for idx, c in enumerate(self.cluster):
			if c[2] != None:
				print "C[%2d]: %3d items [R %.2f] [Center %s] [Size %.1f]" % (idx, c[1], c[2], c[0].str(), c[0].ksdsize())
			else:
				print "C[%2d]: %3d items [Center %s] [Size %.1f]" % (idx, c[1], c[0].str(), c[0].ksdsize())

	def	prn(self):
		self.prnItemInfo()
		self.prnCluster()
		print "Loop = %d" % (self.loop)

	## id sharing probability
	def _distinction(self, ci, cj):
		diffV = ci[0] - cj[0]
		Dij = diffV.ksdsize()
		Si = ci[0].ksdsize()
		Sj = cj[0].ksdsize()
		res = (Dij/Si + Dij/Sj) * 50
		return res

	def getSharing(self):
		""" Assumption: clusters must in the sorted order
		"""
		shProb = 0.0
		Ck = self.cluster[-1]
		for idx in range(len(self.cluster)-1):
			Ci = self.cluster[idx]
			prob = self._distinction(Ci, Ck) * (float(Ci[1])/ len(self.iteminfo))
			shProb += prob
	
		shProb *= 0.9
		if shProb > 100:
			shProb = 99
		return shProb
			
	def getConsistency_old(self):
		consistency = 0
		for idx, c in enumerate(self.cluster):
			if c[1]==0: continue
			# radius/centersize * 100 * population ratio	
			if c[2] != 0:
				rr = (c[0].ksdsize()/c[2])
			else:
				rr = 0.0
			consistency += rr * 100 * (float(c[1]) / len(self.iteminfo))

		consistency /= 2 
		if consistency < 0:
			consistency = 1
		if consistency > 100:
			consistency = 99
		return consistency

	def getConsistency(self):
		inconsistency = 0
		for idx, c in enumerate(self.cluster):
			if c[1]==0: continue
			# radius/centersize * 100 * population ratio	
			inconsistency += (c[2] / c[0].ksdsize()) * 100 * (float(c[1]) / len(self.iteminfo))

		consistency = 100 - inconsistency
		if consistency < 0:
			consistency = 1
		if consistency > 100:
			consistency = 99
		return consistency

		
			

if __name__ == "__main__":
	import sys
	tarr = [
	Vector("110, 0, 93, -15, 125, 31, 94, -32, 94, -15, 93"),
	Vector("109, -15, 109, -15, 78, 47, 78, -16, 109, -46, 93"),
	Vector("109, -16, 79, 15, 94, 47, 78, -31, 109, -31, 94"),
	Vector("94, 16, 109, -63, 110, 47, 78, -47, 94, 0, 78"),
	Vector("110, 31, 109, -15, 109, 31, 78, -15, 109, -31, 109")
	]

	t = Vector([1, 2, 3, 4, 3])
	t2 = Vector([2, 3, 20, 10, 5])
	t3 = Vector([3, 3, 40, 5, 1])
	t4 = Vector([3, 15, 4, 6, 3])
	t5 = Vector([10, 4, 4, 6, 90])
	t6 = Vector([3, 3, 45, 5, 1])
	tall = [t,t2,t3,t4, t5, t6]

	cl = Cluster(tarr)
	cl.run(3)
	cl.prn()
	print cl.getSharing()
	#cl.prn()
	#cl.prnIntraCluster()
	
	# to check if calc was done in run()
	#cl.calcCentroid()
	#cl.calcRadius()
	cl.prnCluster()
	print "consistency %d"% (cl.getConsistency())


