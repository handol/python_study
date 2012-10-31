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
import util
import profile

from hangul import *

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


class hanengdict:
	
	def __init__(self, dictpath):
		self.dictpath = dictpath
		self.HDICT = {}
		self.EDICT = {}
	
	def prepare(self, start='a', end='z' ):
		self.all_engdic(start, end)

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
		res = ''
		try:
			ss = self.EDICT[e]
			for s in ss:
				res += "%s : %s\n" % (s[0], s[1])
		except:
			res += "not found\n"
		return res

	def search(self, a):
			if ord(a[0]) > 128:
					return self.search_h(a)
			else:
					return self.search_e(a)

	def search_h_prn(self, h):
		try:
			print self.HDICT[h]
			print
		except:
			print "not found"
			print

	def search_e_prn(self, e):
		try:
			ss = self.EDICT[e]
			for s in ss:
				print "%s : %s" % (s[0], s[1])
		except:
			print "not found"
			print

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

	def all_engdic(self, start, end):	
		for alpha in range(ord(start), ord(end)+1):
			print "processing %c ..." % chr(alpha)
			fname = os.path.join(self.dictpath, chr(alpha) + ".dic")
			self.proc_engdic(fname)

	def proc_engdic(self, fname):
		try:
			fd = open(fname, 'r')
		except:
			print "reading failed:", fname
	
		n = 0
		for line in fd.xreadlines():
			self.build_handict(line)
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

		res = [b for b in basewords if self.HDICT.has_key(b)]
		return res
			

	def build_handict(self, line):
		s = line.split(":")

		if len(s) < 2: 
			print "error :"
			print line
			return

		head = s[0].strip()
		expl = s[1].strip()

		s = head.split()
		if len(s) > 2 and s[0].isupper(): 
		# �빮�� ����̸� �� ���ξ�� �Ѵ�.
			idxword = s[0]
		else:
			idxword = head

		item = (head, expl)
		#print idxword
		self.insert_e_item(idxword, item)

		hwords = self.get_han_stem(expl)
		for h in hwords:
			self.insert_h_item(h, idxword)

	
	def get_han_stem(self, expl):
	# return �ѱ� ���ξ� ���. ���ο��� �ѱ۸� ���� ���� ó��.
		stems = []

		expl = remove_in_marks(expl, '(', ')')
		hwords = filterHanWords(expl)
		for h in hwords:
			for stem in stemHanWord(h):
				stems.append(stem)

				if len(stem) > 6: ## ���մܾ�
					stems += self.stemHanComplex(stem)	
					
		return stems


	def insert_e_item(self, key, item):
		try:
			self.EDICT[key].append(item)
		except:
			self.EDICT[key] = [item]
		pass

	def insert_h_item(self, key, item):
		try:
			ewords = self.HDICT[key]
			if item not in ewords:
				ewords.append(item)
		except:
			self.HDICT[key] = [item]
		pass


	
	def testit(self):
		while 1:
			a = util.getinput("Enter a word:")
			if a=='.': break
			if a=='': continue

			self.search_prn(a)
	

if __name__ == "__main__":
	if os.getenv("SHELL") != None:
		hdic = hanengdict("/data1/AD/data/engdic/")
	else:
		hdic = hanengdict("C:/Works/ad_svc_backup/ad_svc_data/engdic/")

	profile.run ("hdic.prepare('a', 'a')")

	hdic.info()
	#hdic.prn_hdict()
	#hdic.prn_edict()

	hdic.testit()



