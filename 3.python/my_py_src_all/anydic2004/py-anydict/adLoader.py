#!/usr/bin/env python
# -*- coding: EUC-KR -*-
# ���ѻ������� �ѿ� ������ �����.
# python�� dict �̿��Ͽ� ����.
# dict�� key �� �ѱ� �ܾ�, value = (�ѱ� ���ξ�, ���� ǥ����, �ǹ�)
#
# �ѱ� ����:
# ���ξ� = �ѱ�, ����Ÿ = ���� �ܾ� ���
# ���� ����.
# ABCC Atomic Bomb Casualties Commission : x, ���� ���� ���� ����ȸ
# --> ���ξ� ABCC, ǥ���� ABCC Atomic Bomb Casualties Commission

import os.path
import time

import util
import hangul
import adSearcher

class anydict:
	
	def __init__(self, wnfile, webster, ehpath, wlistfile, provfile):
		self.wnfile = wnfile
		self.webster = webster
		self.ehpath = ehpath
		self.wlistfile = wlistfile
		self.provfile = provfile
		self.HDICT = {}
		self.EDICT = {}
		self.eWordList = []
		self.provList = []
	
	def load(self, start='a', end='a' ):
		print 'loading EngHan Dict ...'
		t = time.time()
		self.loadEngHanDict(start, end)
		print "Total time %.3f" % (time.time()-t)

		print 'loading WordNet Dict ...'
		t = time.time()
		self.loadWordNetDict(self.wnfile)
		print "WordNet %.3f" % (time.time()-t)

		print 'loading Webster Dict ...'
		t = time.time()
		self.loadWebsterDict(self.webster)
		print "Webster %.3f" % (time.time()-t)


		print 'loading WordList Dict ...'
		t = time.time()
		self.loadEngWordList(self.wlistfile)
		print "WordList %.3f" % (time.time()-t)

		print 'loading Proverb Dict ...'
		t = time.time()
		self.loadProverbList(self.provfile)
		print "Proverb %.3f" % (time.time()-t)

		t = time.time()
		self.eWordList.sort()
		print "Sorting %.3f" % (time.time()-t)

	def __del__(self):
            pass
        
	def prn_hdict(self):
		for (k,v) in self.HDICT.iteritems():
			print "@", k
			for e in v:
				print "  ", e

	def prn_edict(self):
		for (k,v) in self.EDICT.iteritems():
			print "@", k
			for e in v:
        			print "%s : %s" % (e[0], e[1])

	def search(self, func, word):
		try:
			e = self.EDICT[word]
			print "len of EDICT val = %d" % (len(e))
			print e
		except:
			pass

		if word == "reloadreload":
			reload(adSearcher)
			return "\n<BR/> OK "
		else:
			return adSearcher.search(self, func, word)

	def stem_eng(self, eng):
		return adSearcher.stem_eng(eng)

 
	def info(self):
		print "=== HDICT: %d keys, %d vals" % ( len(self.HDICT), 
			len(self.HDICT) )

		print "=== EDICT: %d keys, %d vals" % ( len(self.EDICT), 
			len(self.EDICT) )

		return

		print self.HDICT.keys()[:4]
		print self.HDICT.values()[:4]
		print self.EDICT.keys()[:4]
		print self.EDICT.values()[:4]
	
	### Webster ���� ���� �ε�
	def loadWebsterDict(self, fpath, debug=0):
		all = range(ord('a'), ord('z')+1)
		all = map(chr, all) + ['new']
		total = 0
		for c in all:
			fname = "%s%s.html" % (fpath , c)
			cnt = self.loadWebsterDict_one(fname)
			if debug: print "%s  -- %d" % (fname, cnt)
			total += cnt
		if debug: print "Total %d words" % total

	def loadWebsterDict_one(self, fname, debug=0):
		try:
			fd = open(fname,'r')
		except:
			print "read fail:", fname
			return

		cnt = 0

		all = fd.read()
		maxlen = len(all)
		pos = 0

		while pos < maxlen:
			p1 = all.find('\n', pos)
			if p1==-1: break

			p2 = all.find('\n\n', p1)
			if p2==-1: break

			w = all[pos:p1]
			expl = all[p1+1:p2]

			pos = p2+2

			self.insertE_WB(w, expl)
			cnt += 1
			#if cnt > 4: break
		
		if debug: print "Total:", cnt
		return cnt

	### WordNet ���� ���� �ε�
	def loadWordNetDict(self, fname):
		try:
			fd = open(fname,'r')
		except:
			print "read fail:", fname
			return

		cnt = 0

		all = fd.read()
		maxlen = len(all)
		pos = 0

		while pos < maxlen:
			p1 = all.find('\n', pos)
			if p1==-1: break

			p2 = all.find('\n\n', p1)
			if p2==-1: break

			w = all[pos:p1]
			expl = all[p1+1:p2]

			pos = p2+2

			self.insertE_EE(w, expl)

			cnt += 1
			#if cnt > 4: break
		
		print "Total:", cnt

	## ���� ��� �ε�
	def loadProverbList(self, fname):
		try:
			fd = open(fname, 'r')
		except:
			print "reading failed:", fname

		isenglish = 1
		eng = ''
		han = ''
		cnt = 0
		for line in fd.xreadlines():
			if line[0].isspace(): continue
			if line[0].isalpha():
				if not isenglish: 
					self.insert_proverb(eng, han)
					cnt += 1
					eng = ''
					han = ''
					#print len(self.provList)

				isenglish = 1
				eng += "<li> " + line
			else:
				isenglish = 0
				han += "<li> " + line
			
		if not isenglish: 
			self.insert_proverb(eng, han)
			cnt += 1
	


	## ���� �ܾ� ��� ���Ͽ��� �ܾ��� ����, ����� �� ���� �ܾ� ã��
	def loadEngWordList(self, fname):
		try:
			fd = open(fname, 'r')
		except:
			print "reading failed:", fname

		for line in fd.xreadlines():
			sp = line.split(':')
			if len(sp) < 2: continue

			sp2 = sp[1].split()
			if len(sp2) > 7:
				self.insertE_related(sp[0].strip(), sp2[7])



	## ���� ����: ���ĺ����� ȭ�� �и��Ǿ� ����. -- ����.
	## �ٸ� �������� ���� ���� �ε��ؾ� �Ѵ�.
	def loadEngHanDict(self, start, end, debug=0):	
		start = start.lower()
		end = end.lower()
		for alpha in range(ord(start), ord(end)+1):
			fname = os.path.join(self.ehpath, chr(alpha) + ".dic")
			
			t = time.time()
			self.oneEngHanDict(fname)
			if debug: print "EngHan %.3f" % (time.time()-t)


	## ���� ���� ȭ�� �ϳ� ó��
	def oneEngHanDict(self, fname, debug=0):
		try:
			fd = open(fname, 'r')
		except:
			print "reading failed:", fname
	
		n = 0
		for line in fd.xreadlines():
			self.parseEngHanDict(line)
			n += 1
			#if n > 5: return
		if debug: print "%d word from %s" % (n, fname)

	## ���մܾ� ó��
	def stemHanComplex(self, word):
		basewords = hangul.stem_complex(word)

		res = []
		for b in basewords:
			if self.HDICT.has_key(b):		
				res.append(b)

		return res
			

	def getEngIndexWord(self, head):
		s = head.split()
		if len(s) > 2 and s[0].isupper(): 
		# �빮�� ����̸� �� ���ξ�� �Ѵ�.
			return s[0]

		p = head.find(',')
		if p != -1:
			return head[:p-1]	
		else:
			return head

	def parseEngHanDict(self, line):
		s = line.split(":")
		if len(s)==1:
			s = line.split("[")
		if len(s)==1:
			s = line.split("]")

		if len(s) < 2: 
			print "error :"
			print line
			return

		head = s[0].strip()
		expl = s[1].strip()

		idxword = self.getEngIndexWord(head)

		#item = (head, expl)
		#print idxword
		self.insertE_EH(idxword, expl)

		hwords = self.get_han_stem(expl)
		for h in hwords:
			self.insertH_EW(h, idxword)
		return idxword

	
	def get_han_stem(self, expl):
	# return �ѱ� ���ξ� ���. ���ο��� �ѱ۸� ���� ���� ó��.
		stems = []

		expl = util.remove_in_marks(expl, '(', ')')
		hwords = hangul.filterHanWords(expl)

		## ���� �ܾ� ���� ������ ��� �ϱ� �ܾ ����
		## stem�� ���Ѵ�.
		for h in hwords:
			for stem in hangul.stemHanWord(h):
				stems.append(stem)

				if len(stem) > 6: ## ���մܾ�
					#stems += self.stemHanComplex(stem)	
					pass
					
		return stems


	## ���� �ܾ� ��� ���Ͽ��� �ܾ��� ����, ����� �� ���� �ܾ� ã��
	def	insertE_related(self, word, related):
		try:
			self.EDICT[word][0] = related
		except:
			pass

	## ���� �߰�
	def insert_proverb(self, eng, han):
		prov = (eng,han)
		self.provList.append(prov)

		## ���� �ܾ�
		for e in eng.split():
			if not e.isalpha(): continue
			low = e.lower()
			if low=='a' or low=='an' or low=='the' : continue
			self.insertE_PROV(e, prov)

		## �ѱ� ���� �۾�
		for h in han.split():
			for stem in hangul.stemHanWord(h):
				self.insertH_PROV(stem, prov)
			

	## �Ӵ㿡 ���ѵ� �ܾ key. �ε��� �۾��� �����ϴ�.
	def insertE_PROV(self, key, prov):
		try:
			if not prov in self.EDICT[key][3]:
				self.EDICT[key][3].append(prov)
		except:
			pass

	## ���� �������� ���� ���� �ܾ� �ֱ�
	def insertE_EH(self, key, hanexpl):
		try:
			## ���� ������ ���� ǥ��� �� ���� �ܾ�� �� ��찡 �ִ�.
			expl = self.EDICT[key][2]
			if expl == None: 
				expl = "%s<br/>\n" % hanexpl
			else:
				expl += "%s<br/>\n" % hanexpl
		except:
			newone = [None, None, hanexpl, [], None]
			self.EDICT[key] = newone
			self.eWordList.append(key)
		pass

	## Webster 
	def insertE_WB(self, key, expl):
		keyorg = key
		key = key.lower()
		try:
			self.EDICT[key][4] = expl
			return
		except:
			pass

		try:
			self.EDICT[keyorg][4] = expl
			return
		except:
			pass
	
		newone = [None, None, None, [], expl ]
		self.EDICT[key] = newone
		self.eWordList.append(key)

	## ���� �������� ���� ���� �ܾ� �ֱ�
	def insertE_EE(self, key, expl):
		try:
			self.EDICT[key][1] = expl
		except:
			newone = [None, expl, None, [], None]
			self.EDICT[key] = newone
			self.eWordList.append(key)
		pass

	## �ѱ� �ܾ�� ���� ���� �ܾ� ��� �����.
	def insertH_EW(self, key, eng):
		try:
			ewords = self.HDICT[key][0]
			if eng not in ewords:
				ewords.append(eng)
		except:
			self.HDICT[key] = [[eng], []]

	## �ѱ� �ܾ�� ���� ���� ��� �����.
	def insertH_PROV(self, key, prov):
		try:
			self.HDICT[key][1].append(prov)
		except:
			self.HDICT[key] = [[], [prov]]



	
	def testit(self):
		fname = "/tmp/a.html"
		try:
			out = open(fname, "w")
			print "Result will be saved to:", fname
		except:
			pass

		
		while 1:
			a = util.getinput("Enter a word:")
			if a=='.': break
			if a=='': continue

			res = self.search(3, a)
			print res
			if out != None: 
				out.write(res)
				out.flush()
	

def	load():
	ADDIR = os.getenv("ANYDICT_HOME")

	AD = anydict(
		ADDIR + "/data/wn17.html",
		ADDIR + "/data/webster/", 
		ADDIR + "/data/engdic/", 
		ADDIR + "/data/word.dict",
		ADDIR + "/data/hometopia.dict"
	)
	
	return AD
		
	

if __name__ == "__main__":
	if os.getenv("SHELL") != None:
	   ADDIR = os.getenv("ANYDICT_HOME")

	   AD = anydict(
		   ADDIR + "/data/wn17.html",
		   ADDIR + "/data/webster/", 
		   ADDIR + "/data/engdic/", 
		   ADDIR + "/data/word.dict",
		   ADDIR + "/data/hometopia.dict"
	   )
	else:
		#AD = anydict("C:/Works/ad_svc_backup/ad_svc_data/engdic/")
		pass

	#AD.load('a', 'a')
	AD.loadEngHanDict('a', 'z')

	AD.info()
	#AD.prn_ADt()
	#AD.prn_edict()

	AD.testit()



