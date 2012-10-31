#!/usr/bin/python
# -*- coding: EUC-KR -*-
# 2008/3/10

import AdMysqlDb
import AdData

def	chrange(start, end):
	return map(chr, range(ord(start), ord(end)+1) )

def	saveDataFile_wExam_all():
	hostTab = AdData.Host()
	docTab = AdData.Doc()
	db = AdMysqlDb.login()
	db.loadGoodHosts(hostTab, minDocs=20)
	hostTab.info()	
	db.loadGoodDocs(docTab, minDocs=20, minStcs=10)
	docTab.info()	

	wordListTab = AdData.WordList()
	db.loadWordList(wordListTab)
	wordListTab.info()

	for alpha in chrange('A', 'Z'):
		outfile = "wExam_%c.dat" % alpha
		print "===== saveDataFile  %s" % (outfile)	
		wordExTab = AdData.WordEx(docTab.T, wordListTab.T)
		wordExTab.saveDataFile(outfile)
		db.loadWordEx(wordExTab, alpha)
		wordExTab.info()
		del wordExTab

def	saveDataFile_iExam_all():
	hostTab = AdData.Host()
	docTab = AdData.Doc()
	db = AdMysqlDb.login()
	db.loadGoodHosts(hostTab, minDocs=20)
	hostTab.info()	
	db.loadGoodDocs(docTab, minDocs=20, minStcs=10)
	docTab.info()	

	### Real English Dict
	IDICT = {}

	idiomListTab = AdData.IdiomList(IDICT)
	db.loadIdiomList(idiomListTab)
	idiomListTab.info()

	for alpha in chrange('A', 'Z'):
		outfile = "iExam_%c.dat" % alpha
		print "===== saveDataFile  %s" % (outfile)	
		idiomExTab = AdData.IdiomEx(docTab.T, idiomListTab.T)
		idiomExTab.saveDataFile(outfile)
		db.loadIdiomEx(idiomExTab, alpha)
		idiomExTab.info()
		del idiomExTab


def saveDataFile_hosts_and_docs():
	hostTab = AdData.Host()
	docTab = AdData.Doc()
	db = AdMysqlDb.login()
	db.loadGoodHosts(hostTab, minDocs=20)
	hostTab.info()	
	db.loadGoodDocs(docTab, minDocs=20, minStcs=10)
	docTab.info()	
	hostTab.saveDataFile("goodHosts.dat")
	docTab.saveDataFile("goodDocs.dat")


def	saveDataFile_word_idiom_list():
	db = AdMysqlDb.login()

	wordList = AdData.WordList()
	db.loadWordList(wordList)
	wordList.info()
	wordList.saveDataFile("wordList.dat")

	IDICT = {}
	idiomList = AdData.IdiomList()
	db.loadIdiomList(idiomList)
	idiomList.info()
	idiomList.saveDataFile("idiomList.dat")



def loadAdAll():

	hostTab = AdData.Host()
	docTab = AdData.Doc()
	#db = AdMysqlDb.AdDb()
	db = AdMysqlDb.login()
	db.loadGoodHosts(hostTab, minDocs=20)
	db.loadGoodDocs(docTab, minDocs=20, minStcs=10)
	#hostTab.prn()	
	hostTab.info()	

	#docTab.prn()	
	docTab.info()	

	wordListTab = AdData.WordList()
	db.loadWordList(wordListTab)
	wordListTab.info()

	wordExTab = AdData.WordEx(docTab.T, wordListTab.T)

	for alpha in range(ord('A'), ord('Z')+1):
		db.loadWordEx(wordExTab, chr(alpha))
		break
	wordExTab.info()



if __name__=="__main__":
	import sys
	#saveDataFile_wExam_all()
	saveDataFile_hosts_and_docs()
	#saveDataFile_word_idiom_list()
	#saveDataFile_iExam_all()
