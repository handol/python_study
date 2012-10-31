#!/usr/bin/env python
# -*- coding: EUC-KR -*-
import sys
import os
import os.path
import cgi
import socket
import time

import adtemplate


CON_KEYS = [
"����, �н���, ����, ���, ����, �ʵ� �ϱ�, ���б�, ����ϱ�, SAT, ����, ����, ���� ���� ",
"����, ��ȭ, DVD, ����, ����,  ��ī��, �ʰ�� ���ͳ� ",
"����, ����, ������, �ܵ�, �Ҽ�, ����, ����, ����, �����, ����",
"����, �ʵ� �б�, ��ġ��, ���̹�, �����, ����, ",
"����, ����, ����, ����, ���伥, ������, ���� ",
"��ȭ, ��ȭ, ���, ����, ������, �����, ���� ����, ��������, �Ե�����, ���﷣��",
"��Ʈ�� �߰� ����, TV, �����, ���� û����, ������, DTV, DMB, ���� ��� ",
"TV, �����, ���� û����, ������, DTV, DMB, ���� ��� ",
"MP3, ������, ���� ��ǰ, PSP, X box, ����, ����, �޴�� DPA, �޴���, ��ȭ��, �ִ��� " ]


### protocol 
### cgi --> server: Len(4bytes) + Ver(4bytes) + Func(4bytes) + Words
### server --> cgi: Ver(4bytes) + Words + \n + results

ADWEB = '/var/www/lib'
ADWEB = '/export/home/anydict/anydichome'
ADDIC = ADWEB + '/ad.dic.new'
PROTO_VER = 'V001'

def save_spell(misspell, good):
	try:
		fd = open(ADWEB + "/misspell.txt", "a+")
	except:
		return

	fd.write("%s %s\n" % (misspell, good))
	fd.flush()

def google_spell(word):
	import google
	
	if ord(word[0]) > 128: return ## �ѱ��̸� 
	if word.find(' ') != -1: return
	if word.find('-') != -1: return

	key = 'Nx3n4NtQFHJLZCH32gaWjrZsEPiXvRr7'
	suggested = google.doSpellingSuggestion(word, key)

	if suggested !=None:
		print """<br/><font color="red"> <b>���,  �� �ܾ��  �˻��غ����� </b> </font> <font color="green"> <a href="/ad.py?F=3&W=%s"><b>%s</b></a> </font> <br/><br/>""" % (suggested, suggested)
		save_spell(word, suggested)


###
def test_dict():
	import util
	while 1:
		a = util.getinput("Enter a word:")
		if a=='.': break

		req_dic([], 1, a)
		
def req_dic(argv, func, word):
	global orgword
	if len(argv) >= 2:
		port = int(argv[1])
	else:
		port = 8900

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		#sock.connect ( (socket.gethostbyname('localhost'), port) )
		sock.connect ( ("127.0.0.1", port) )
		time.sleep(0.2)

	except:
		handle_fail()
		#raise
		return

	body = "%s %2d %s" % (PROTO_VER, func, word) 
	msg = "%-4d%s" % (len(body), body)
	sock.send (msg)

	
	buf = sock.recv (128)
	if len(buf) > 10 and buf[:3]=="ORG":
		pos = buf.find('\n',3)
		if pos != -1:
			orgword = buf[4:pos]
			#print "ORG: %s" % orgword
			buf = buf[pos:]

	print """
	<!-- google_ad_section_start --> 
	<font color="blue"> <b>%s</b> </font> <br/><br/>
	<!-- google_ad_section_end --> 
	""" % orgword
	if len(buf) < 100:
		try:
			google_spell(orgword)
		except:
			pass

	sys.stdout.write(buf)

	while 1:
		buf = sock.recv (1024*2)
		if buf == '': break
		#print buf
		sys.stdout.write(buf)
 
	sock.close()


def handle_fail():
	print "<br/>�ִϵ� ������ �⵿ ���Դϴ�. <br/>\n ��ø� ��ٷ� �ּ���. <br/>"  


def exec_addic(query):
	cmd = "%s %s" % (ADDIC, query)
	#print cmd
	print os.popen(cmd).read()
		
def test_cgi():
	print "<strong>Python %s</strong>" % sys.version
	keys = os.environ.keys( )
	keys.sort( )

	print "<pre>"
	for k in keys:
		print "%s\t%s" % (cgi.escape(k), cgi.escape(os.environ[k]))
	print "</pre>"

PIDICDIR = ADWEB + '/dictimg/'
POOMSA = ['verb', 'adjective', 'noun', 'adverb']

def pidic(word):

	poomsa = []
	for p in POOMSA:
		path = "%s%s-%s.jpg" % (PIDICDIR, word, p)
		if os.path.exists(path): 
			poomsa.append(p)

	if len(poomsa)==0: return

	print "<table><tr>"
	for p in poomsa: 
		name = "%s-%s" % (word, p)
		print "<td align='center'><img src='/dictimg/%s.jpg' border=0> <br/> <b>%s</b> (%s)</td>" % \
			(name, word, p)
	print "</tr></table>"


## write log
def write_log(word, func):
	if word != '' and func != 0:
		browser = os.getenv("HTTP_USER_AGENT")
		if browser != None and browser.find("Google") != -1: sys.exit(0)

		try:
			fd = open("/tmp/adword.log", "a+")
		except:
			sys.exit(0)
		
		fd.write(cgi.escape(word)+'\n')
		fd.flush()

def clean_word(word):
	clean = [w for w in word if w.isalpha() or w.isspace() or w=='\'' or w=='-']
	clean = ''.join(clean)
	sp = clean.split()
	if len(sp) > 1:
		clean = ' '.join(sp)
	
	return clean



## HTML form �� ���� GET �޼ҵ�� �� parameter �� ���ϱ�
def get_query(debug=0):
	global FUNC, WORD, QUERY, PAGE

	forms = cgi.FieldStorage()

	#for k in forms.keys():
	#	QUERY += "%s=%s\\&" % (k, forms[k].value.replace(' ','+'))

	#print forms.keys()

	try : FUNC = int(forms['F'].value)
	except: FUNC = 0 

	try : WORD = forms['W'].value.strip()
	except: WORD = '' 

	try : PAGE = int(forms['P'].value.strip())
	except: PAGE = 0
 
	if len(WORD)>0 and WORD[0].isalpha():
		WORD = clean_word(WORD)

	if debug: 
		print "Func=%d Word=%s" % (FUNC, WORD)
		print "QUERY: %s" % QUERY


#### main
PAGE = 0
FUNC = 0
WORD = ''
QUERY = ''

orgword = ''

NAVER = """ <img src="http://static.naver.com/common/lg/naver03.gif"> 
<img src="http://static.naver.com/dic/top2/gnb_diction01_on.gif"> &nbsp;
<A href="http://endic.naver.com/search.nhn?dic_where=endic&query=%s&query_euckr=" target="naverdic">
<br/>
<center> %s </center>
</A> <BR/> <BR/>"""


GOOGLE = """<div id="searchcontrol">Google searching...</div>"""


def do_naver_and_google(orgword, urlword):
	print """<table><tr><td valign="top">"""
	try:
		pidic(orgword)
	except:
		pass

	print """</td><td valign="top">"""
	print NAVER % (urlword, orgword)

	print """</td><td>&nbsp;&nbsp;&nbsp;</td><td>"""
	print GOOGLE
	print """</td></tr></table>"""

if __name__=='__main__':

	debug = 0	

	print 'Content-Type: text/html\n'

	if len(sys.argv)>1: debug = 1
	
	get_query(debug)

	if len(WORD) > 0:
		r = ord(WORD[0])
		r %= len(CON_KEYS)
		keywords = CON_KEYS[r]
	else:
		keywords = CON_KEYS[0]

	orgword = WORD
	urlword = orgword.replace(' ','+')
		
	#adtemplate.adHead(keywords, "�ִϵ�: %s" % WORD)
	adtemplate.googleHead(orgword)
	adtemplate.adLogo(keywords)
	adtemplate.adForm("ad.py", WORD)



	print "<br/> &nbsp; &nbsp;"
	adtemplate.adGoogle()


	if WORD != '' and FUNC == 3:
		try:
			req_dic(sys.argv, FUNC, WORD)
		except:
			pass

	do_naver_and_google(orgword, urlword)



	print "<br/> &nbsp; &nbsp;"
	adtemplate.adGoogle()
	
	QUERY = "F=%d\\&W=%s" % (FUNC, orgword.replace(' ','+') )
	if PAGE != 0:
		QUERY += "\\&P=%d" % PAGE

	#if FUNC != 3: print QUERY

	if WORD != '' and QUERY != '':
		exec_addic(QUERY)
		print "</table>"


	
	adtemplate.adFooter()

	sys.stdout.flush()
	sys.stdout.close()

	## write WORD log
	write_log(WORD, FUNC)
