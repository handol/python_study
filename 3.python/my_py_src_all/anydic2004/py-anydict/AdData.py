#!/usr/bin/python
# -*- coding: EUC-KR -*-
# anydic2004  anydict 예문 서비스를 위한 데이타 관리 모듈
# -- 각 테이블을 클래스화. 검색 등 제공.
# 2008/3/10

## Host Table: host id, name, # of docs
class Host(object):
	def __init__(self):
		self.T = {}
		self.alldocs = 0

	def add(self, hostid, numdocs, hostname):
		try:
			self.T[hostid] = [numdocs, hostname]
			self.alldocs += int(numdocs)
		except:
			print "hostid %d duplicate" % (hostid)

	def hostname(self, hostid):
		try:
			hname = self.T[hostid][1]
		except:
			return "Unknown"
		else:
			return hname
	

	def prn(self):
		for id, vals in self.T.iteritems():
			print "%4d %4d %s" % (id, vals[0], vals[1])

	## saveDataFile to a text file
	def saveDataFile(self, outfile):
		try:
			self.out = open(outfile, 'w')
		except:
			return

		for id, vals in self.T.iteritems():
			self.out.write("%4d %4d %s\n" % (id, vals[0], vals[1]))
		self.out.close()

	## loadDataFile from a text file == load
	def	loadDataFile(self, infile):
		try:
			self.infd = open(infile, 'r')
		except:
			print "read file:", infile
			return

		for line in self.infd:
			r = line.split()
			if len(r) < 3:
				print "** ERROR in Host Data", line
				continue
			self.add(int(r[0]), int(r[1]), r[2])
		self.infd.close()


	def info(self):
		print "hosts=%d docs=%d" % ( len(self.T), self.alldocs)


## Doc Table: doc id, host id , url, title, filepath, doc level, no_sentences.

OLD_ADTXT = "/data1/AD/txt/"
NEW_ADTXT = "/home/handol/ADSVCHOME/txt/"
DELIMITER = " -|- "

class Doc(object):
	"""
	doc = [hostid, url, title, filepath, doclevel, no_stc, text]
	"""
	def __init__(self):
		self.T = {}

	def add(self, docid, hostid, url, title, filepath, doclevel, no_stc):
		title = title.replace('\n', ' ')
		title = title.replace('\r', ' ')
		filepath = filepath.replace(OLD_ADTXT, "")
		try:
			self.T[docid] = [hostid, url, title, filepath, doclevel, no_stc]
		except:
			print "docid %d duplicate" % (docid)

	def prn(self):
		for id, vals in self.T.iteritems():
			print "%4d %s" % (id, vals)
			break

	def saveDataFile(self, outfile):
		try:
			self.out = open(outfile, 'w')
		except:
			return

		for id, vals in self.T.iteritems():
			vals = map(str, vals)
			vals = DELIMITER.join(vals)
			self.out.write("%4d%s%s\n" % (id, DELIMITER, vals))
		self.out.close()

	## loadDataFile from a text file == load
	def	loadDataFile(self, infile):
		try:
			self.infd = open(infile, 'r')
		except:
			print "read file:", infile
			return

		for line in self.infd:
			r = line.split(DELIMITER)
			if len(r) < 7: 
				print "** ERROR in Doc Data", line
				continue
			self.add(int(r[0]), int(r[1]), r[2], r[3], r[4], int(r[5]), int(r[6]))
		self.infd.close()

	def info(self):
		print "docs=%d" % ( len(self.T) )

	# load all the text files
	def loadTexts(self, maxdocs=10):
		print "starting loading text files... : max %d" % (maxdocs)
		cnt = 0
		for k,v in self.T.iteritems():
			v.append( self.loadText(v[3]) )	
			cnt += 1
			if cnt >= maxdocs: break
		print "finished loading all text files..."

	# load one file
	def loadText(self, filepath, debug=0):
		filepath = NEW_ADTXT + filepath
		if debug: print "loading...", filepath
		try:
			f = open(filepath, 'r')
			txt = f.read()
			if txt.startswith("###"):
				pos = txt.find('\n')
				txt = txt[pos+1:] 	
			return txt
		except:
			print "read fail:", filepath
			return None

	# get the doc info
	def	getDoc(self, docid):
		try:
			docinfo = self.T[docid]
		except:
			return None
		if len(docinfo)==6:
			txt = self.loadText( docinfo[3] )
			docinfo.append(txt)
		return docinfo

	def	getDoc(self, docinfo):
		if len(docinfo)==6:
			txt = self.loadText( docinfo[3] )
			docinfo.append(txt)
		return docinfo


class	EngDict:
	def __init__(self):
		self.T = {}

	def add(self, word, wordid):
		try:
			self.T[word] = [None]*5
		except:
			pass

	def info(self):
		print "EngDict=%d" % ( len(self.T) )

## Word List: word ID ==> word mapping
# engDict is adLoader.anydict.EDICT
# len of EDICT val = 5
# [None, '<table><tr><td valign=top><b>n</b></td> <td valign=top>:</td> <td><font color=\'green\'><b>syn</b></font> <font color=\'blue\'> hullo, hi, howdy, how-do-you-do </font><br/> an expression of greeting<br/>\n &nbsp; <i> "every morning they exchanged\npolite hellos" </i><br/>\n</td></tr></table>', None, [], '<TABLE><tr><td width=20 class="pm" valign="top">interj & n</td>\n<td class="xp" valign="top">See Halloo.</td></tr>\n</TABLE>']

class	WordList(object):
	def __init__(self):
		self.T = {}
		self.EDICT = {}
		self.EORG = {}

	def add(self, word, wordid, org_word):
		try:
			exlist = self.EDICT[word]
		except:
			exlist = []
			self.EDICT[word] = exlist
		if org_word != None:
			self.EORG[word] = org_word

		try:
			self.T[wordid] = [exlist, word, org_word]
		except:
			print "wordid %d duplicate" % (wordid)

	def prn(self):
		for id, vals in self.T.iteritems():
			print "%4d %s" % (id, vals)
			break

	def saveDataFile(self, outfile):
		try:
			self.out = open(outfile, 'w')
		except:
			return

		for id, vals in self.T.iteritems():
			if vals[2] != None:
				line = "%4d\t%s\t%s\n" % (id, vals[1], vals[2])
			else:
				line = "%4d\t%s\n" % (id, vals[1])
			self.out.write(line)
		self.out.close()

	## loadDataFile from a text file == load
	def	loadDataFile(self, infile):
		try:
			self.infd = open(infile, 'r')
		except:
			print "read file:", infile
			return

		for line in self.infd:
			r = line.split()
			if len(r) < 2: continue
			if len(r)==3:
				self.add(r[1], int(r[0]), r[2])
			else:
				self.add(r[1], int(r[0]), None)
		self.infd.close()

	def info(self):
		print "wordLists=%d" % ( len(self.T) )
		print "wordLists=%d" % ( len(self.EDICT) )

	def sortExList(self):
		for id, vals in self.T.iteritems():
			vals[0].sort(exCmpFunc)


## idiom_list table: idiom_id ==> idiom, mapping
class	IdiomList(object):
	def __init__(self):
		self.T = {}
		self.IDICT = {}

	def add(self, idiom, idiomid):
		try:
			idict = self.IDICT[idiom]
		except:
			idict = []
			self.IDICT[idiom] = idict

		try:
			self.T[idiomid] = [idict, idiom]
		except:
			print "idiomid %d duplicate" % (idiomid)

	def prn(self):
		for id, vals in self.T.iteritems():
			print "%4d %s" % (id, vals[1])
			break

	def saveDataFile(self, outfile):
		try:
			self.out = open(outfile, 'w')
		except:
			return

		for id, vals in self.T.iteritems():
			line = "%4d\t%s\n" % (id, vals[1])
			self.out.write(line)
		self.out.close()

	## loadDataFile from a text file == load
	def	loadDataFile(self, infile):
		try:
			self.infd = open(infile, 'r')
		except:
			print "read file:", infile
			return

		for line in self.infd:
			r = line.split('\t')
			if len(r) < 2: continue
			self.add(r[1].strip(), int(r[0]))
		self.infd.close()

	def info(self):
		print "idiomIds=%d" % ( len(self.T) )
		print "idiomIds=%d" % ( len(self.IDICT) )


## Word Examples
class	WordEx(object):
	def	__init__(self, docDict, wordListDict, debug=0):
		self.T = {}
		self.docList = docDict
		self.wordList = wordListDict
		self.wordCnt = 0
		self.exCnt = 0
		self.out = None
		self.debug = debug

	def	saveDataFile(self, outfile):
		try:
			self.out = open(outfile, 'w')
		except:
			if self.debug: raise
			return

	def add(self, wordid, docid, s_pos, s_len, w_pos, w_len, stc_level):
		try:
			docinfo = self.docList[docid]
		except:
			if self.debug: 
				print "docid=", docid
				raise
			return

		try:
			exlist = self.wordList[wordid][0]
		except:
			if self.debug: raise
			return

		if exlist == None:
			print "exlist", exlist
			return

		try:
			exlist.append( [docinfo, s_pos, s_len, w_pos, w_len, stc_level] )
			if len(exlist)==1:
				self.wordCnt += 1
		except:
			print "append insert: idiom"

		self.exCnt += 1

		if self.out != None:
		   self.out.write("%d\t%d\t%d\t%d\t%d\t%d\t%d\n" % (wordid, docid, s_pos, s_len, w_pos, w_len, stc_level))


	## loadDataFile from a text file == load
	def	loadDataFile(self, infile):
		try:
			self.infd = open(infile, 'r')
		except:
			print "read file:", infile
			return

		for line in self.infd:
			r = line.split()
			if len(r) < 7: continue
			r = map(int, r)
			self.add(r[0],r[1],r[2],r[3],r[4],r[5],r[6]) 
		self.infd.close()

	def info(self):
		print "Word=%d ,  Ex=%d" % (self.wordCnt, self.exCnt)


	
##
## Idiom Examples
class	IdiomEx(object):
	def	__init__(self, docDict, idiomListDict, debug=0):
		self.T = {}
		self.docList = docDict
		self.idiomList = idiomListDict
		self.idiomCnt = 0
		self.exCnt = 0
		self.out = None
		self.debug = debug

	def	saveDataFile(self, outfile):
		try:
			self.out = open(outfile, 'w')
		except:
			return

	def add(self, idiomid, docid, s_pos, s_len, w_pos, w_len, stc_level):
		try:
			docinfo = self.docList[docid]
		except:
			return

		try:
			idict = self.idiomList[idiomid][0]
		except:
			return

		if idict == None:
			return

		try:
			idict.append( [docinfo, s_pos, s_len, w_pos, w_len, stc_level] )
			if len(idict)==1:
				self.idiomCnt += 1
		except:
			print "append insert: idiom"

		self.exCnt += 1

		if self.out != None:
		   self.out.write("%d\t%d\t%d\t%d\t%d\t%d\t%d\n" % (idiomid, docid, s_pos, s_len, w_pos, w_len, stc_level))

	## loadDataFile from a text file == load
	def	loadDataFile(self, infile):
		try:
			self.infd = open(infile, 'r')
		except:
			print "read file:", infile
			return

		for line in self.infd:
			r = line.split()
			if len(r) < 7: continue
			r = map(int, r)
			self.add(r[0],r[1],r[2],r[3],r[4],r[5],r[6]) 
		self.infd.close()

	def info(self):
		print "Idiom=%d ,  Ex=%d" % (self.idiomCnt, self.exCnt)


## compare values of two exinfo. for sorting by sentence level
def exCmpFunc(ex1, ex2):
	#print "+++++++", ex1, ex2
	cmp = ex1[5] - ex2[5]  # sentence level
	if cmp != 0: return cmp
	cmp = id(ex1[0]) - id(ex2[0]) # docinfo (docid)
	return cmp


# to define the same sentence.       
# if docinfo(docid) and s_pos are equal, return 0
def exIdCmpFunc(ex1, ex2):
	cmp = id(ex1[0]) - id(ex2[0])
	if cmp != 0: return cmp
	cmp = ex1[1] - ex2[1]
	return cmp
