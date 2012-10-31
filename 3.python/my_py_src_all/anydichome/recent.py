#!/bin/env python
# -*- coding: EUC-KR -*-

import adtemplate
import adstatic

## return true if  the word is English or full Korean word
def ishangul(word):
	if ord(word[0]) < 128: return 1

	i = 0
	while i <len(word) and ord(word[i]) > 128 :
		val = (ord(word[i]) << 8) + ord(word[i+1])

		if val >= 0xB0A1 and val <= 0xC8FE:
			i += 2
		else:
			break

	if i == len(word): return 1
	else: return 0

NUM_COLS = 5
SEEK_OFFSET = -500
def recent_words(columns=NUM_COLS):
	try:
		fd = open("adword.log", "r")
	except:
		return

	wdict = {}
	wlist = [] 
	try:
		fd.seek(SEEK_OFFSET, 2)
	except:
		fd.seek(0, 0)
		pass
	fd.readline()
	prev_word = ""
	while 1:
		word = fd.readline().strip()
		if word == '': break
		if word == 'reloadreload': continue
		if ishangul(word)==0: continue
		if len(word)==1: continue
		if word == prev_word:
			continue
		prev_word = word
			
		if not wdict.has_key(word):
			wdict[word] = None
			wlist.append(word)

	wlist.reverse()


	print "<center><font size=-1 color='green'> <b> 다른 사람들이  현재 검색하는 단어들 (최신순) </b></font></center><br/>"
	print "<table>"
	prev = ''
	n = 0
	for word in wlist:
		if word != prev:
			if n % columns == 0: print "<tr>"
			print """<td align="left" width=150><font size=-1><a class="q" href="/ad.py?F=3&W=%s">%s</a></font></td>""" % (word.replace(' ','+'), word)
			if n % columns == 0: print "<td>&nbsp;</td>"
			if n % columns == columns-1: print "</tr>"
			prev = word
			n += 1

	leftcols = n % columns
	print "<td>&nbsp;</td>" * leftcols
	if leftcols > 0: print "</tr>"

	print "</table></font>"


def prn_recent():
	#print """<center> <table><tr><td align="left" width=60%%>"""
	print """ <table><tr align="left">"""
	print """<td align="left" width=100%%>"""
	recent_words()
	print "</td></tr></table> "

if __name__ == "__main__":
	print 'Content-Type: text/html\n'
	
	keywords = "컴퓨터, 인터넷, 무선공유기, 학원 "
	WORD = adstatic.randWord()

	adtemplate.adHead(keywords, "애니딕: %s" % WORD)
	adtemplate.adLogo()
	adtemplate.adForm("ad.py", WORD)
	adtemplate.adGoogle()
	
	prn_recent()

	adstatic.adFooter()

