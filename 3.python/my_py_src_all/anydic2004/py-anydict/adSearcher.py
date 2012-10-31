#!/usr/bin/env python
# -*- coding: EUC-KR -*-
# anydict.py 에서 HTML 출력 부분을 분리.
# anydict.py 에서 이 모듈을 reload 하도록 할려고.

import hangul

EDICT = None
HDICT = None

def deco_prov(word, provlist):
	if len(provlist)==0:
		return ''

	tmp = ''
	for prov in provlist:
		eng = prov[0]
		han = prov[1]

		if ord(word[0]) > 128: ## 한글이면
			han = han.replace(word, "<b><font color='green'>%s</font></b>" % word)
		else:
			eng = eng.replace(word, "<b><font color='green'>%s</font></b>" % word)

		#eng = eng.replace('\n','<br/>\n')
		#han = han.replace('\n','<br/>\n')

		tmp += """<tr><td valign="top"><ul><font>%s</font></ul></td> <td valign="top"><ul><font size=-1>%s</font></ul></td></tr>\n""" % (eng, han)

	res = """<br/><table><tr ><td background="img/bg_lightblue.gif"><font clor="blue"><b>속담</b></font> \
<font size=-1><a href="http://hometopia.com/proverb/indexpro.html" target="adext">출처 - 속담토피아</a> \
</font></td><td background="img/bg_lightblue.gif">&nbsp;</td></tr>\n%s</table>""" % tmp
	return res
			
def search_h_multi( h1, h2):
	#res = "ORG %s %s\n<br/>\n" % (h1, h2)
	res = ''
	try:
		ew1 = HDICT[h1][0]
		ew2 = HDICT[h2][0]

		pv1 = HDICT[h1][1]
		pv2 = HDICT[h2][1]
	except:
		return '' 

	from sets import Set
	s1 = Set(ew1)
	s2 = Set(ew2)
	s1.intersection_update(s2)
	res += deco_ew_list(h1, list(s1))

	s1 = Set(pv1)
	s2 = Set(pv2)
	s1.intersection_update(s2)
	res += deco_prov(h1, list(s1))
	return res
	
def search_h( h):
	res = "ORG %s\n<br/>\n" % (h)

	#hlist = hangul.stemHanWord(h)
	if h.find(' ') != -1:
		h = h.split()[0]

	hlist = hangul.stem_complex(h)
	hlist.append(h)
	hlist.sort()

	prev = ''
	for sh in hlist:
		if len(sh)==2 and sh != h: continue
		if len(prev) >= 6 and sh[:len(prev)] == prev: 
			# 활발, 활발한 : sh==활발한 인 경우 prev 가 활발 이면 skip
			continue
		prev = sh
		res += search_h_one(sh)
	return res

def search_h_one( h):
	try:
		ewlist = HDICT[h][0]
	except:
		hl = h.split()
		if len(hl) > 1:
			return search_h_multi(hl[0], hl[1])
		else:
			return ''

	if len(ewlist) > 30:
		ewlist = ewlist[:30]
	res = """\n<BR/> <font color="green"><b>%s</b></font><BR/><BR/>\n""" % (h)
	res += deco_ew_list(h, ewlist)
	res += deco_prov(h, HDICT[h][1])

	return res

def deco_ew_list( hw, ewlist):

	table = ''
	for e in ewlist:
		try:
			hexpl = EDICT[e][2]
			hexpl = hexpl.replace(hw, """<font color="green">%s</font>""" % hw)

			url = "/ad.py?F=3&W=%s" % e.replace(' ',  '+')
			table += """<tr><td valign='top'><a class="qb" href="%s">%s </a></td><td valign='top'>:</td><td valign='top'><font size=-1> %s </font></td></tr>\n""" \
				% (url, e, hexpl)
		except:
			pass

	head = ',&nbsp; '.join( ewlist )
	res = """<font color="#3364C3">%s</font><br/><br/>\n<table>%s</table><BR/>\n""" % (head, table)
	return res


def stem_eng( eng):
		
	pos = eng.find('\'')
	if pos != -1:
		eng = eng[:pos]

	if eng[0].isupper():
		w = eng.lower()
		if EDICT.has_key(w):
			return w
		w = eng.upper()
		if EDICT.has_key(w):
			return w

		w = eng.title()
		if EDICT.has_key(w):
			return w
	else:
		w = eng.title()
		if EDICT.has_key(w):
			return w
		
	eng = eng.lower()

	if eng.endswith('ing'):
		w = eng[:-3]
		if EDICT.has_key(w):
			return w

		w = eng[:-3] + 'e'
		if EDICT.has_key(w):
			return w
		return ''

	if eng.endswith('iest'):
		w = eng[:-4] + 'y'
		if EDICT.has_key(w):
			return w
		else:
			return ''

	if eng.endswith('est'):
		w = eng[:-3] 
		if EDICT.has_key(w):
			return w
		else:
			return ''

	if eng.endswith('ier'):
		w = eng[:-3] + 'y' 
		if EDICT.has_key(w):
			return w
		else:
			return ''

	if eng.endswith('er'):
		w = eng[:-2] 
		if EDICT.has_key(w):
			return w
		else:
			return ''


	if eng.endswith('ies'):
		w = eng[:-3] + 'y'
		if EDICT.has_key(w):
			return w
		else:
			return ''

	if eng.endswith('es'):
		if EDICT.has_key(eng[:-2]):
			return eng[:-2]

	if eng.endswith('s'):
		if EDICT.has_key(eng[:-1]):
			return eng[:-1]
		else:
			return ''
	if eng.endswith('ed'):
		if EDICT.has_key(eng[:-2]):
			return eng[:-2]

	if eng.endswith('d'):
		if EDICT.has_key(eng[:-1]):
			return eng[:-1]
		else:
			return ''
	#return ''
		
def search_e( e):
	if not EDICT.has_key(e):
		e = stem_eng(e)
		if e=='': return ''
	if EDICT[e][0] != None:
		e = EDICT[e][0]
	
	try:
		res = prnAnydictItem( e, EDICT[e])
	except:
		res = ''
	return res

def search(adLoader, func, word):
		global HDICT, EDICT
		HDICT = adLoader.HDICT
		EDICT = adLoader.EDICT

		#if word=='aaa': return "reload OK"

		if ord(word[0]) > 128:
				res = search_h( word)
				#if len(res) < 80:
				#	stems = hangul.stem_complex(word)
				#	for h in stems:
				#		res +="%s<br/>" % h
				#		res += search_h( h)
		else:
				res = search_e( word)
		return res


###
def prnAnydictItem( word, item):
	res = "ORG %s\n" % word

	if item[0] != None: 
		res += """관련 단어 : <a class="q" href="/ad.py?F=3&W=%s">%s</a><br/>\n""" \
			% (item[0].replace(' ','+'), item[0])

	if item[1] != None: wndict = item[1]
	else: wndict = ''
	if item[4] != None: webster = item[4]
	else: webster = ''

	res += """<table>\n<tr><td width=50%% background="img/bg_lightblue.gif" >영영사전 - WordNet</td><td width=50%% background="img/bg_lightblue.gif">영영사전 - Webster</td></tr>\n<tr><td valign="top">%s</td>\n<td valign="top">%s</td></tr></table><br/>\n""" % (wndict, webster)

	if item[2] != None:
		res += """<br/><table width=100%% ><tr><td colspan=2 background="img/bg_lightblue.gif">한영사전 </td> </tr><tr><td width=15%%> <b>%s</b></td><td><font clor="blue">%s</font></td></tr></table><br/>\n""" % (word, item[2])

	res += deco_prov(word, item[3])
	return res



if __name__ == "__main__":
	import os
	import adLoader
	if os.getenv("SHELL") != None:
		hdic = adLoader.anydict (
			"/data1/AD/data/wn17.html",
			"/data1/AD/data/webster/",
			"/data1/AD/data/engdic/",
			"/data1/AD/data/word.dict",
			"/data1/AD/data/hometopia.dict"
		)
	else:
		#hdic = anydict("C:/Works/ad_svc_backup/ad_svc_data/engdic/")
		pass

	hdic.load('a', 'a')

	hdic.info()
	#hdic.prn_hdict()
	#hdic.prn_edict()

	hdic.testit()



