#!/usr/bin/env python
# -*- coding: EUC-KR -*-
# anydict.py ���� HTML ��� �κ��� �и�.
# anydict.py ���� �� ����� reload �ϵ��� �ҷ���.



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
<font size=-1><a href="http://hometopia.com/proverb/indexpro.html">��ó - �Ӵ����Ǿ�</a> \
</font></td><td>&nbsp;</td></tr>\n%s</table>""" % tmp
		return res
				
	def search_h_multi(self, h1, h2):
		try:
			ew1 = self.HDICT[h1][0]
			ew2 = self.HDICT[h2][0]

			pv1 = self.HDICT[h1][1]
			pv2 = self.HDICT[h2][1]
		except:
			return []

		from sets import Set
		s1 = Set(ew1)
		s2 = Set(ew2)
		s1.intersection_update(s2)
		res = self.deco_ew_list(h1, list(s1))

		s1 = Set(pv1)
		s2 = Set(pv2)
		s1.intersection_update(s2)
		res += self.deco_prov(h1, list(s1))
		return res
		
	def search_h(self, h):
		try:
			ewlist = self.HDICT[h][0]
		except:
			hl = h.split()
			if len(hl) > 1:
				return self.search_h_multi(hl[0], hl[1])
			else:
				return ''

		res = self.deco_ew_list(h, ewlist)
		res += self.deco_prov(h, self.HDICT[h][1])

		return res
	
	def deco_ew_list(self, hw, ewlist):

		table = ''
		for e in ewlist:
			try:
				hexpl = self.EDICT[e][2]
				hexpl = hexpl.replace(hw, """<font clor="green">%s</font>""" % e)

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
			
	def search_e(self, e, outfd=None):
		if not self.EDICT.has_key(e):
			e = self.stem_eng(e)
			if e=='': return ''

		try:
			res = self.prnAnydictItem(e, self.EDICT[e])
		except:
			res = ''
			raise
		return res

	def search(self, a):
			if ord(a[0]) > 128:
					return self.search_h(a)
			else:
					return self.search_e(a)

 
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

	def prnAnydictItem(self, word, item):
		if item[0] == None: 
			res =  ''
		else:
			res = "���� �ܾ� : %s<br/>\n" % item[0]

		if item[1] != None:
			res += "%s<br/>\n" % item[1]
		if item[2] != None:
			res += "<table width=80%% ><tr><td></td><td><font clor='blue'>%s</font></td></tr></table>\n" % (item[2])

		res += self.deco_prov(word, item[3])
		return res
	

