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

from hangul import *
from wndict import *

## a, n, A(��)����, A�� Ʋ(���ſ� ����, ȣ�̽�Ʈ, ����Ʈ, ������ ���� ��ġ�� �� ��)
## --> remove_in_marks(str, '(', ')' )
## a, n, A����, A�� Ʋ
def remove_in_marks(str, mark1, mark2):
	res = ''
	pos = 0
	while 1:
		p = str[pos:].find(mark1)
		if p == -1: 
			res += str[pos:]
			break

		else:
			res += str[pos:pos+p]
			pos = pos+p+1

			p = str[pos:].find(mark2)
			if p == -1: break
			pos = pos+p+1

	return res


class anydict:
	
	def __init__(self, wnfile, ehpath, wlistfile):
		self.wnfile = wnfile
		self.ehpath = ehpath
		self.wlistfile = wlistfile
		self.HDICT = {}
		self.EDICT = {}
		self.eWordList = []
	
	def prepare(self, start='a', end='a' ):
		print 'loading EngHan Dict ...'
		t = time.time()
		self.loadEngHanDict(start, end)
		print "Total time %.3f" % (time.time()-t)
		print 'Done'

		print 'loading WordNet Dict ...'
		t = time.time()
		self.loadWordNetDict(self.wnfile)
		print "WordNet %.3f" % (time.time()-t)
		print 'Done'

		print 'loading WordList Dict ...'
		t = time.time()
		self.loadEngWordList(self.wlistfile)
		print "WordList %.3f" % (time.time()-t)
		print 'Done'

		print 'Soring ...'
		self.eWordList.sort()
		print 'Done'

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


	def search_h(self, h):
		try:
			res = ' '.join( self.HDICT[h])
		except:
			res = "not found"

		return res + '\n'

	def search_e(self, e, outfd=None):
		try:
			res = self.prnAnydictItem(self.EDICT[e])
		except:
			res = "not found\n"
		return res

	def search(self, a):
			if ord(a[0]) > 128:
					return self.search_h(a)
			else:
					return self.search_e(a)

	def search_h_prn(self, h):
		try:
			print self.HDICT[h]
		except:
			print "not found"

	def search_e_prn(self, e):
		try:
			self.prnAnydictItem(self.EDICT[e])
		except:
			print "not found"

	def search_prn(self, a):
			if ord(a[0]) > 128:
					#print "�ѱ�"
					self.search_h_prn(a)
			else:
					#print "English"
					self.search_e_prn(a)


 
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
	
	### WordNet ���� ���� �ε�
	def loadWordNetDict(self, fname):
		cnt = 0
		init(fname)

		while 1:
			w,expl = next()
			if w == '': break
			cnt += 1

			#print w, expl
			html = proc_oneword(w, expl)
			self.insertE_EE(w, html)
			#if cnt > 4: break
		
		print "Total:", cnt

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
	def loadEngHanDict(self, start, end):	
		for alpha in range(ord(start), ord(end)+1):
			fname = os.path.join(self.ehpath, chr(alpha) + ".dic")
			
			t = time.time()
			self.oneEngHanDict(fname)
			print "EngHan %.3f" % (time.time()-t)


	## ���� ���� ȭ�� �ϳ� ó��
	def oneEngHanDict(self, fname):
		try:
			fd = open(fname, 'r')
		except:
			print "reading failed:", fname
	
		n = 0
		for line in fd.xreadlines():
			self.parseEngHanDict(line)
			n += 1
			#if n > 5: return
		print "%d word from %s" % (n, fname)

	## ���մܾ� ó��
	def stemHanComplex(self, word):
		basewords = stem_complex(word)

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

		if len(s) < 2: 
			print "error :"
			print line
			return

		head = s[0].strip()
		expl = s[1].strip()

		idxword = self.getEngIndexWord(head)

		item = (head, expl)
		#print idxword
		self.insertE_EH(idxword, item)

		hwords = self.get_han_stem(expl)
		for h in hwords:
			self.insert_h_item(h, idxword)

	
	def get_han_stem(self, expl):
	# return �ѱ� ���ξ� ���. ���ο��� �ѱ۸� ���� ���� ó��.
		stems = []

		expl = remove_in_marks(expl, '(', ')')
		hwords = filterHanWords(expl)

		## ���� �ܾ� ���� ������ ��� �ϱ� �ܾ ����
		## stem�� ���Ѵ�.
		for h in hwords:
			for stem in stemHanWord(h):
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

	## ���� �������� ���� ���� �ܾ� �ֱ�
	def insertE_EH(self, key, item):
		try:
			self.EDICT[key][2].append(item)
			print "Multi EH:", key
		except:
			newone = [None]* 6
			newone[2] = [item]
			self.EDICT[key] = newone
			self.eWordList.append(key)
		pass

	## ���� �������� ���� ���� �ܾ� �ֱ�
	def insertE_EE(self, key, expl):
		try:
			self.EDICT[key][1] = expl
		except:
			newone = [None]* 6
			newone[1] = expl
			self.EDICT[key] = newone
			self.eWordList.append(key)
		pass

	def insert_h_item(self, key, item):
		try:
			ewords = self.HDICT[key]
			if item not in ewords:
				ewords.append(item)
		except:
			self.HDICT[key] = [item]
		pass

	
	###
	def prnAnydictItem(self, item):
		if item[0] == None: item[0] = ''

		res = "%s\n%s\n%s : %s\n" % ( item[0], item[1], item[2][0][0], item[2][0][1])

		print '-'*10, "����"
		if item[0] != None: print item[0]
		print '-'*10, "����"
		print item[1]
		print '-'*10, "����"
		for eh in item[2]:
			print "%s : %s" % (eh[0], eh[1])

		return res
	
	def testit(self):
		while 1:
			a = util.getinput("Enter a word:")
			if a=='.': break
			if a=='': continue

			self.search_prn(a)
	


if __name__ == "__main__":
	if os.getenv("SHELL") != None:
		hdic = anydict (
			"/data1/AD/data/wn17.dict",
			"/data1/AD/data/engdic/",
			"/data1/AD/data/word.dict"
		)
	else:
		hdic = anydict("C:/Works/ad_svc_backup/ad_svc_data/engdic/")

	hdic.prepare('a', 'z')

	hdic.info()
	#hdic.prn_hdict()
	#hdic.prn_edict()

	hdic.testit()



