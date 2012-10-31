#!/usr/bin/python
# -*- coding: EUC-KR -*-
# 2008/3/10

import random
import re
import AdData
import AdEngStem
from AdUtil import *
import SocketServer
#import StringIO
import cStringIO # faster.  NO unicode

ADDIR = "/home/handol/ADSVCHOME/mysql_export/"
SENTENCE_MAXLEN = 256

EXLIST_TOP = """<div class="exlist"> <table> <tr><th width=75%>생생 예문</th><th width=18% align="right">URL</th><th width=7%>level</th></tr>"""
EXLIST_BOTTOM = """</table> </div>"""

#
#
class AdSearcher:
	def __init__(self):
		random.seed(id(self))
		self.startingWWW = re.compile("^www\.")
		pass

	def loadEnglishDict(self):
		self.wordListTab = AdData.WordList()
		self.wordListTab.loadDataFile( ADDIR + "wordList.dat" )
		self.wordListTab.info()
		print self.wordListTab.T.values()[1000:1002]

		self.idiomListTab = AdData.IdiomList()
		self.idiomListTab.loadDataFile( ADDIR + "idiomList.dat" )
		self.idiomListTab.info()
		print self.idiomListTab.T.values()[1000:1002]

	def loadHostDoc(self):

		self.hostTab = AdData.Host()
		self.hostTab.loadDataFile( ADDIR + "goodHosts.dat" )
		#self.hostTab.prn()	
		self.hostTab.info()	

		self.docTab = AdData.Doc()
		self.docTab.loadDataFile( ADDIR + "goodDocs.dat" )
		#self.docTab.prn()	
		self.docTab.info()	


	def loadEx(self, start='A', end='Z', numdocs=100000):
		print "loading Ex to '%c' ..." % (end)
		self.wordExTab = AdData.WordEx(self.docTab.T, self.wordListTab.T, debug=1)
		for alpha in chrange(start, end):
			self.wordExTab.loadDataFile( ADDIR + "wExam_%c.dat" % alpha)
			self.wordExTab.info()

		self.idiomExTab = AdData.IdiomEx(self.docTab.T, self.idiomListTab.T)
		for alpha in chrange(start, end):
			self.idiomExTab.loadDataFile( ADDIR + "iExam_%c.dat" % alpha)
			self.idiomExTab.info()

		#self.docTab.loadTexts()
		
		import threading
		thr = threading.Thread(target=self.loadDocsAndSortEx, kwargs={'maxdocs':numdocs})
		thr.start()
		print "called thread^^"

	def loadDocsAndSortEx(self, maxdocs=100):
		self.docTab.loadTexts(maxdocs)
		self.wordListTab.sortExList()


	def load(self, start='A', end='Z'):
		if start==end:
			numdocs = 1000
		else:
			numdocs = 100000

		self.loadHostDoc()
		self.loadEnglishDict()
		self.loadEx(start, end, numdocs)

	def query(self, query,debug=0):
		if ord(query[0]) >= 128:
			return

		stemmer = AdEngStem.stemmer(self.wordListTab.EDICT, self.idiomListTab.IDICT, self.wordListTab.EORG)
		stems = stemmer.stemQuery(query)
		if len(stems) == 0:
			#print "word '%s' NOT found" % query
			return ""
		
		###  display original form of words
		if debug: 
			for s in stems:
				print "%d %s %d ex" %(s[0], s[1], len(s[2]))

		for idxm, s in enumerate(stems):
			if len(s[2])==0:
				try:
					org_word = self.wordListTab.EORG[s[1]]
				except:
					continue
				stems[idx] = stemmer.stemQuery(org_word)[0]
				
				

		words = [s[1] for s in stems]
		#print "<center><b>%s</b></center>" % (" &nbsp; &nbsp; ".join(words))
		
		### display  list of ex
		if len(stems) == 1:
			self.prnExList(stems[0][2], [], sampling=True)
		else:

			merger = ExListMerger(stems[0][2])
			for i in range(1, len(stems)):
				merger.AND(stems[i][2])
	
			exlist, wposlist = merger.getExList()
			self.prnExList(exlist, wposlist, sampling=True)


	def prnExList(self, exlist, wposlist, sampling=False, page=0, pagesize=10):
		#print "Result: %d" % (len(exlist))
		#print "Result: %d" % (len(wposlist))

		if len(exlist)==0:
			return

		if sampling and len(exlist) > pagesize:
				sampleidx = random.sample(range(len(exlist)), pagesize)
				sampleidx.sort()
				exlist = [exlist[i] for i in sampleidx]
				if wposlist != []:
					wposlist = [wposlist[i] for i in sampleidx]

		begin = page*pagesize
		end = begin + pagesize
		if begin > len(exlist):
			return
		if end > len(exlist):
			end = len(exlist)

		print EXLIST_TOP
	

		if wposlist != []:
			for i in range(begin, end):
				self.prnExSentence(exlist[i], wposlist[i], i)
		else:
			for i in range(begin, end):
				self.prnExSentence(exlist[i], None, i)

		print EXLIST_BOTTOM
		
	def prnExSentence(self, exinfo, wordpos, loop_idx, debug=0):
		try:
			docinfo =  exinfo[0]
			if debug: print docinfo[:6]
			if debug: print exinfo[1:]

			self.docTab.getDoc(docinfo)
			txt = docinfo[6]
			if debug: print "txt leng=%d" % len(txt)
			
			host = self.hostTab.hostname(docinfo[0])
			host = self.startingWWW.sub("", host)

			url = host + docinfo[1]
			if exinfo[1] >= len(txt):
				return " "

			if exinfo[2] > SENTENCE_MAXLEN:
				exinfo[2] = SENTENCE_MAXLEN

			end = exinfo[1]+exinfo[2]
			if end > len(txt): end = len(txt)

			if wordpos == None:
				wordpos = [(exinfo[3], exinfo[4])]
				
			onesentence = txt[exinfo[1]:end]

			## 2008.6.17 : add previous sentence
			prevst_offset = (int)(exinfo[1] - exinfo[2] * 1.1)
			if prevst_offset < 0: prevst_offset = 0
			while prevst_offset < len(txt):
				if txt[prevst_offset].isspace(): break
				prevst_offset += 1

			prevsentence = txt[prevst_offset:exinfo[1]]
				
			#print sentence
			onesentence = self.getSentence(onesentence, wordpos)
			sentence = " ... %s <BR/> %s" % (prevsentence, onesentence)	
			
		except:
			raise
			sentence = "Error"
		else:
			#print "L[%d] U[%s] %s" % (exinfo[5], url, sentence)
			if loop_idx % 2 == 1:
				trclass = """class="alt" """
			else:
				trclass = ""
			
			print """<tr %s><td class="stc">%s</td><td><a href="http://%s" target="orgpage">%s</a></td><td>%d</td></tr>""" % \
					(trclass, sentence, url, host, exinfo[5])


	def  getSentence(self, org_stc, wordpos):
		wordpos.sort(lambda x,y: x[0]-y[0]) # sort by word_pos

		seglist = []
		last_pos = 0
		for w_pos,w_len in wordpos:
			seglist.append( org_stc[last_pos:w_pos] )
			seglist.append( "<b>%s</b>" % (org_stc[w_pos:w_pos+w_len]) )
			last_pos = w_pos+w_len
		if last_pos < len(org_stc):
			seglist.append(org_stc[last_pos:])
		return ''.join(seglist)
			
		
		
	
	def testit(self):
		import sys

		fname = "test.res"
		try:
			out = open(fname, "w")
			print """!! Output ==> "%s" """ % (fname)
		except:
			pass

		
		while 1:
			a = getinput("Enter a word:")
			if a=='.': break

			org_stdout = sys.stdout
			sys.stdout = out
		
			res = self.query(a)
			out.flush()
			sys.stdout = org_stdout
		
		out.close()


class ExListMerger(object):
	def __init__(self, exlist):
		# one item in mergelist = (exinfo, distance, word_position)
		self.mergelist = map(lambda ex: [ex,0, [(ex[3], ex[4])]], exlist) 
		self.mergelist.sort(lambda x,y: AdData.exIdCmpFunc(x[0],y[0]))
		self.mergeCount = 1

	def AND(self, exlistB):
		setA = self.mergelist
		setB = exlistB[:]
		setB.sort(AdData.exIdCmpFunc)

		self.mergeCount += 1
		setR = []
		idxA = idxB = 0
		matchCnt = 0
		while idxA < len(setA) and idxB < len(setB):
			A = setA[idxA][0]
			B = setB[idxB]
			cmp = AdData.exIdCmpFunc(A, B)
			if cmp==0:
				distance = abs(A[3] - B[3])
				setR.append((A, distance))
				#print setA[idxA]
				#print type(setA[idxA])
				#print setA[idxA][1]
				#print type(setA[idxA][1])
				setA[idxA][1] += distance
				setA[idxA][2].append( (B[3],B[4]) )
				idxA += 1
				idxB += 1
				matchCnt += 1
			elif cmp < 0:
				idxA += 1
			else:
				idxB += 1

		if matchCnt > 0:
			andlist = []
			for i in range(len(self.mergelist)):
				if len(self.mergelist[i][2]) == self.mergeCount:
					andlist.append(self.mergelist[i])
			
			#print "==matchCnt=%d, andlist=%d"  % (matchCnt, len(andlist))
			del self.mergelist
			self.mergelist = andlist
				

	def getExList(self):
		def mergeResultCmp(x,y):
			#cmp = x[1]-y[1]
			cmp = x[1]-y[1]
			if cmp == 0:
				return x[0][5]-y[0][5]
			else:
				return cmp

		#self.mergelist.sort(lambda x,y: x[1]-y[1])
		self.mergelist.sort(mergeResultCmp)
		exlist = map(lambda x:x[0], self.mergelist)
		wposlist = map(lambda x:x[2], self.mergelist)
		#print len(exlist), len(wposlist)
		#print "exlist", exlist
		#print "wposlist", wposlist
		return exlist,wposlist
		

### Global
ad = AdSearcher()

##
class MyHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		while 1:
			lenpart = self.request.recv(4)
			if not lenpart: break

			#print "LEN:", lenpart
			msglen = int(lenpart)

			msg = self.request.recv(msglen)
			if not msg: break
			if len(msg) != msglen:
				print "read msg incompletely"
				break

			#print "MSG:", msg
			func = 0
			if len(msg) >= 8 and msg[0]=='V':	
				func = int(msg[4:8])
				msg = msg[8:]

			print func, msg
		
			org_stdout = sys.stdout
	
			output = cStringIO.StringIO()
			sys.stdout = output
			ad.query(msg)
			sys.stdout = org_stdout
			
			self.request.send(output.getvalue())
			output.close()
			break


# #
def start_server(port):
	myServer = SocketServer.TCPServer(('',port), MyHandler)
	myServer.allow_reuse_address = True
	myServer.serve_forever( )

if __name__=="__main__":
	import sys

	if len(sys.argv) > 1:
		if sys.argv[1]=="ALL":
			start = 'A'
			end = 'Z'
		else:
			start = end = sys.argv[1][0].upper()

	ad.load(start, end)

	if len(sys.argv) > 2:
		start_server(int(sys.argv[2]))
	else:
		ad.testit()
