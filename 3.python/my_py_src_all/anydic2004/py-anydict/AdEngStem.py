#!/usr/bin/env python
# -*- coding: EUC-KR -*-

rules = [
	('ing', ''),
	('ing', 'e'),
	('rring', 'r'),
	('tting', 't'),
	('lling', 'l'),
	('ying', 'ie'),
	('est', ''),
	('iest', 'y'),
	('ttest', 't'),
	('llest', 'l'),
	('rrest', 'r'),
	('er', ''),
	('ier', 'y'),
	('ier', ''),
	('es', ''),
	('ies', 'y'),
	('ves', 'fe'),
	('s', ''),
	('ed', 'e'),
	('ed', ''),
	('ied', 'e'),
	('d', ''),
	('', '')
	]

MAX_IDIOM_LEN  =  4    ## max number of words  in an idiom

class stemmer(object):
	def __init__(self, EDICT, IDICT, EORG):
		self.EDICT = EDICT
		self.IDICT = IDICT
		self.EORG = EORG

	def stemQuery(self, query,debug=0):
		orgwords = query.split()
		terms = map(self.stemWord, orgwords)
		if debug: print "First stemming:", orgwords,"==>", terms

		res = []
		idx = 0
		while idx < len(terms):
			idiom_len, idiom = self.searchIdiom(terms, idx)
			if idiom != None:
				res.append( (idiom_len, idiom, self.IDICT[idiom]) )
				idx += idiom_len
			else:
				try:
					res.append( (1, terms[idx], self.EDICT[terms[idx]]) )
				except:
					pass
				idx += 1
		return res
				

	def searchIdiom(self, terms, idx):
			if idx >= len(terms)-1:
				return None,None

			for idiom_len in range(MAX_IDIOM_LEN, 1, -1):
				if idx+idiom_len-1 >= len(terms):
					continue
				idiom = ' '.join(terms[idx:idx+idiom_len])
				idiom = self.stemIdiom(idiom)
				if idiom != '':
					return (idiom_len, idiom)
			
			return None, None
				
	def stemIdiom(self, idiom):
		if self.IDICT.has_key(idiom):
			return idiom
		else:
			return ''

	def stemWord(self, givenw):
		if self.EDICT.has_key(givenw):
			# "retardation" --> "retard"
			#try:
			#	w = self.EORG[givenw]
			#except:
			#	return givenw
			w = givenw
			return w

		if givenw[0].isupper():
			w = givenw.lower()
			w = self.stemConjugation(w)
			if w != '':
				return w

			w = givenw.title()
			w = self.stemConjugation(w)
			if w != '':
				return w
			return ""
		else:
			w = givenw
			w = self.stemConjugation(w)
			if w != '':
				return w

			w = givenw.title()
			w = self.stemConjugation(w)
			if w != '':
				return w
			return ""
		return ""
			
			

	def stemConjugation(self, givenw, debug=0):
		if debug: print "stemConjugation --", givenw
		if self.EDICT.has_key(givenw):
			return givenw

		for idx, rule in  enumerate(rules):
			if rule[0]=='': break

			if givenw.endswith(rule[0]):
				w = givenw[:-len(rule[0])] + rule[1]
				if debug: print "try --", givenw, rule[0], w
				if self.EDICT.has_key(w):
					return w
				else:
					if not rules[idx+1][0].endswith(rule[0]):
						break
					if debug: print "go to next try --", rules[idx+1][0], rule[0]
		return ''


if __name__=="__main__":
	import sys
	import AdData
	import AdSearch
	
	ad = AdSearch.AdSearcher()
	ad.loadEnglishDict()
	stem = stemmer(ad.wordListTab.EDICT, ad.idiomListTab.IDICT, ad.wordListTab.EORG)	
	while True:
		q = AdSearch.getinput("Enter a query:")
		if q=='.': break
		print stem.stemQuery(q)
