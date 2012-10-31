#!/usr/bin/python
# -*- coding: EUC-KR -*-
# 2008/3/10

import AdData

def	chrange(start, end):
	return map(chr, range(ord(start), ord(end)+1) )


def loadAdAll():

	ADDIR = "/home/handol/ADSVCHOME/mysql_export/"
	hostTab = AdData.Host()
	hostTab.loadDataFile( ADDIR + "goodHosts.dat" )
	#hostTab.prn()	
	hostTab.info()	

	docTab = AdData.Doc()
	docTab.loadDataFile( ADDIR + "goodDocs.dat" )
	#docTab.prn()	
	docTab.info()	

	wordListTab = AdData.WordList()
	wordListTab.loadDataFile( ADDIR + "wordList.dat" )
	wordListTab.info()
	print wordListTab.T.values()[:2]

	idiomListTab = AdData.IdiomList()
	idiomListTab.loadDataFile( ADDIR + "idiomList.dat" )
	idiomListTab.info()
	print idiomListTab.T.values()[:2]

	wordExTab = AdData.WordEx(docTab.T, wordListTab.T, debug=1)
	for alpha in chrange('A', 'A'):
		wordExTab.loadDataFile( ADDIR + "wExam_%c.dat" % alpha)
		wordExTab.info()

	idiomExTab = AdData.IdiomEx(docTab.T, idiomListTab.T)
	for alpha in chrange('A', 'A'):
		idiomExTab.loadDataFile( ADDIR + "iExam_%c.dat" % alpha)
		idiomExTab.info()

	docTab.loadTexts()

	###  search word
	word = 'area'
	try:
		exlist = wordListTab.EDICT[word]
	except:
		print "word '%s' NOT found" % word
	exinfo  = exlist[0]
	docinfo =  exinfo[0]
	print docinfo[:6]
	print exinfo[1:]

	txt = docinfo[6]
	print "txt leng=%d" % len(txt)
	print txt[exinfo[1]:exinfo[1]+exinfo[2]]
	


if __name__=="__main__":
	import sys
	loadAdAll()
