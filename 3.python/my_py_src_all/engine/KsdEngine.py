#!/usr/bin/python
# -*- coding: EUC-KR -*-
# 2008/3/26

import DbChamDemo
from KsdData import KsdData
from KsdModel import KsdModel
from Vector import Vector
from Clustering import Cluster

	
MIN_FOR_TRAINING = 3
MIN_FOR_CLUSTERING = 10
OUTLIER_SCORE = 3.0

def getKsdVectors(loglist, maxscore=10000.0):
	vectors = []
	for log in loglist:
		if log[5] > maxscore:
			continue
		v = Vector(log[3])
		vectors.append( Vector(log[3]))
	return vectors



### using KSD Model
def analyzeKsd(db, user, vectors):
	centerorg, radius = db.getCenter(user)
	center = Vector(centerorg)
	
	model = KsdModel()

	if radius==0.0: ### new Learning
		if len(vectors) < MIN_FOR_TRAINING:
			return 

		model.DoTraining(vectors)

	else: ### use old Learning
		model.UseTrained(center, radius)
	return model		


## update Scores in ksdlog table whose score is NOT set (==0)
def updateScores(db, user, loglist, model):
	for log in loglist:
		if log[5] != 0: # score != 0
			continue
		
		Y = Vector(log[3])
		if Y.dim() != model.dim:
			continue
		distance, theta = model.getDistanceAndTheta(Y)
		log[4], log[5] = distance, theta
		db.updateScore(user, log[0], distance, theta, debug=1)
		


### get Consistency And Sharing using Clustering
def updateConsistencyAndSharing(db, user, vectors):
	if len(vectors) < MIN_FOR_CLUSTERING:
		return	
	cl = Cluster(vectors)
	cl.run(3)
	cl.prnCluster()
	consistency = cl.getConsistency()
	sharing = cl.getSharing()
	print "User=%d, consistency: %d" % (user, consistency )
	print "User=%d, Shareing: %.2f " % (user, sharing)
	db.updateConsistency(user, int(consistency), debug=1)
	db.updateSharing(user, int(sharing), debug=1)


def	main(userid=None):
	data = KsdData()

	db = DbChamDemo.login()
	if userid==None:
		db.load(data)	
	else:
		db.load(data, WHERE="uid =%d" % (userid))	
	data.prn()
	
	for user,loglist in data.T.iteritems():
		print "====User %d: %d items" % (user, len(loglist))	
		vectors = getKsdVectors(loglist)
		updateConsistencyAndSharing(db, user, vectors)

		model = analyzeKsd(db, user, vectors)
		if model==None:
			continue

		updateScores(db, user, loglist, model)

		if model.trainset != None:
			print "  --- New Learning"
			db.updateCenter(user, model.center, model.radius, debug=1)
		else:
			print "  --- Old Learning"
			cleanvectors = getKsdVectors(loglist, maxscore=OUTLIER_SCORE)
			model = KsdModel()
			model.DoTraining(cleanvectors)
			db.updateCenter(user, model.center, model.radius, debug=1)
			


	
		
if __name__=="__main__":
	import sys
	
	try:
		if len(sys.argv) > 1:
			main(int(sys.argv[1]))
		else:
			main()
			
		sys.exit(0)
	except:
		raise
		sys.exit(-1)

		
