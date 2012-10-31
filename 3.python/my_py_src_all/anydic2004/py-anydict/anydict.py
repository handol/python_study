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

		print 'loading Webster Dict ...'
		t = time.time()
		#self.loadWebsterDict(self.webster)
		print "Webster %.3f" % (time.time()-t)
		print 'Done'


		print 'loading WordList Dict ...'
		t = time.time()
		self.loadEngWordList(self.wlistfile)
		print "WordList %.3f" % (time.time()-t)
		print 'Done'

		print 'loading Proverb Dict ...'
		t = time.time()
		self.loadProverbList(self.provfile)
		print "Proverb %.3f" % (time.time()-t)

		print 'Soring ...'
		t = time.time()
		self.eWordList.sort()
		print "Done %.3f" % (time.time()-t)

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


	def deco_prov(self, word, provlist):
		if len(provlist)==0:
			return ''

		tmp = ''
		for prov in provlist:
			eng = prov[0]
			han = prov[1]

			if ord(word[0]) > 128: ## �ѱ��̸�
				han = han.replace(word, "<font color='green'>%s</font>" % word)
			else:
				eng = eng.replace(word, "<font color='green'>%s</font>" % word)

			#eng = eng.replace('\n','<br/>\n')
			#han = han.replace('\n','<br/>\n')

			tmp += """<tr><td valign="top"><ul><font size=-1>%s</font></ul></td> <td valign="top"><ul><font size=-1>%s</font></ul></td></tr>\n""" % (eng, han)

		res = """<br/><table><tr><td><font clor="blue"><b>�Ӵ�</b></font> \
<font size=-1><a href="http://hometopia.com/proverb/indexpro.html" target="adext">��ó - �Ӵ����Ǿ�</a> \
</font></td><td>&nbsp;</td></tr>\n%s</table>""" % tmp
		return res
				
	def search_h_multi(self, h1, h2):
		#res = "ORG %s %s\n<br/>\n" % (h1, h2)
		res = ''
		try:
			ew1 = self.HDICT[h1][0]
			ew2 = self.HDICT[h2][0]

			pv1 = self.HDICT[h1][1]
			pv2 = self.HDICT[h2][1]
		except:
			return '' 

		from sets import Set
		s1 = Set(ew1)
		s2 = Set(ew2)
		s1.intersection_update(s2)
		res += self.deco_ew_list(h1, list(s1))

		s1 = Set(pv1)
		s2 = Set(pv2)
		s1.intersection_update(s2)
		res += self.deco_prov(h1, list(s1))
		return res
		
	def search_h(self, h):
		res = "ORG %s\n<br/>\n" % (h)

		hlist = stemHanWord(h)
		hlist.sort()

		prev = ''
		for sh in hlist:
			if len(prev) >= 4 and sh[:len(prev)] == prev: 
				# Ȱ��, Ȱ���� : sh==Ȱ���� �� ��� prev �� Ȱ�� �̸� skip
				continue
			prev = sh
			res += self.search_h_one(sh)
		return res

	def search_h_one(self, h):
		try:
			ewlist = self.HDICT[h][0]
		except:
			hl = h.split()
			if len(hl) > 1:
				return self.search_h_multi(hl[0], hl[1])
			else:
				return ''

		res = ''
		res += self.deco_ew_list(h, ewlist)
		res += self.deco_prov(h, self.HDICT[h][1])

		return res
	
	def deco_ew_list(self, hw, ewlist):

		table = ''
		for e in ewlist:
			try:
				hexpl = self.EDICT[e][2]
				hexpl = hexpl.replace(hw, """<font color="green">%s</font>""" % hw)

				table += "<tr><td valign='top'><font color='blue'>%s</font></td><td valign='top'>:</td><td valign='top'><font size=-1> %s </font></td></tr>\n" \
					% (e, hexpl)
			except:
				pass

		head = ',&nbsp; '.join( ewlist )
		res = """<font color="blue">%s</font><br/><br/>\n<table>%s</table>\n""" % (head, table)
		return res

	def stem_eng(self, eng):
		if eng[0].isupper():
			w = eng.lower()
			if self.EDICT.has_key(w):
				return w
			w = eng.upper()
			if self.EDICT.has_key(w):
				return w

			w = eng.title()
			if self.EDICT.has_key(w):
				return w
		else:
			w = eng.title()
			if self.EDICT.has_key(w):
				return w
			
		eng = eng.lower()

		if eng.endswith('ing'):
			w = eng[:-3]
			if self.EDICT.has_key(w):
				return w

			w = eng[:-3] + 'e'
			if self.EDICT.has_key(w):
				return w
			return ''

		if eng.endswith('iest'):
			w = eng[:-4] + 'y'
			if self.EDICT.has_key(w):
				return w
			else:
				return ''

		if eng.endswith('est'):
			w = eng[:-3] 
			if self.EDICT.has_key(w):
				return w
			else:
				return ''

		if eng.endswith('ier'):
			w = eng[:-3] + 'y' 
			if self.EDICT.has_key(w):
				return w
			else:
				return ''

		if eng.endswith('er'):
			w = eng[:-2] 
			if self.EDICT.has_key(w):
				return w
			else:
				return ''


		if eng.endswith('ies'):
			w = eng[:-3] + 'y'
			if self.EDICT.has_key(w):
				return w
			else:
				return ''

		if eng.endswith('es'):
			if self.EDICT.has_key(eng[:-2]):
				return eng[:-2]

		if eng.endswith('s'):
			if self.EDICT.has_key(eng[:-1]):
				return eng[:-1]
			else:
				return ''
		if eng.endswith('ed'):
			if self.EDICT.has_key(eng[:-2]):
				return eng[:-2]

		if eng.endswith('d'):
			if self.EDICT.has_key(eng[:-1]):
				return eng[:-1]
			else:
				return ''
		#return ''
			
	def search_e(self, e):
		if not self.EDICT.has_key(e):
			e = self.stem_eng(e)
			if e=='': return ''
		
		try:
			res = self.prnAnydictItem(e, self.EDICT[e])
		except:
			res = ''
		return res

	def search(self, func, word):
			if ord(word[0]) > 128:
					return self.search_h(word)
			else:
					return self.search_e(word)

 
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
	def loadWebsterDict(self, fpath):
		all = range(ord('a'), ord('z')+1)
		all = map(chr, all) + ['new']
		total = 0
		for c in all:
			fname = "%s%s.html" % (fpath , c)
			cnt = self.loadWebsterDict_one(fname)
			print "%s  -- %d" % (fname, cnt)
			total += cnt
		print "Total %d words" % total

	def loadWebsterDict_one(self, fname):
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
		
		print "Total:", cnt
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

	def loadWordNetDict_old(self, fname):
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
			for stem in stemHanWord(h):
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
		try:
			self.EDICT[key][4] = expl
		except:
			newone = [None, None, None, [], expl ]
			self.EDICT[key] = newone
			self.eWordList.append(key)
		pass

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

	
	###
	def prnAnydictItem(self, word, item):
		res = "ORG %s\n<br/>\n" % word

		if item[0] != None: 
			res += "���� �ܾ� : %s<br/>\n" % item[0]

		if item[1] != None:
			res += "%s<br/>\n" % item[1]
		if item[2] != None:
			res += "<table width=80%% ><tr><td></td><td><font clor='blue'>%s</font></td></tr></table>\n" % (item[2])

		res += self.deco_prov(word, item[3])
		return res
	
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
	


if __name__ == "__main__":
	if os.getenv("SHELL") != None:
		hdic = anydict (
			"/data1/AD/data/wn17.html",
			"/data1/AD/data/webster/",
			"/data1/AD/data/engdic/",
			"/data1/AD/data/word.dict",
			"/data1/AD/data/hometopia.dict"
		)
	else:
		#hdic = anydict("C:/Works/ad_svc_backup/ad_svc_data/engdic/")
		pass

	hdic.prepare('a', 'a')

	hdic.info()
	#hdic.prn_hdict()
	#hdic.prn_edict()

	hdic.testit()



