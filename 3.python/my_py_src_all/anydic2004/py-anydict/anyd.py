#!/usr/bin/env python
# -*- coding: EUC-KR -*-
import sys
import os
import os.path
import cgi
import socket

import adtempl

### protocol 
### cgi --> server: Len(4bytes) + Ver(4bytes) + Func(4bytes) + Words
### server --> cgi: Ver(4bytes) + Words + \n + results
ADDIC = '/var/www/html/ad.dic.new'
PROTO_VER = 'V001'

def test_dict():
	import util
	while 1:
		a = util.getinput("Enter a word:")
		if a=='.': break

		req_dic([], 1, a)
		
def req_dic(argv, func, word):
	if len(argv) >= 2:
		port = int(argv[1])
	else:
		port = 8900

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		sock.connect ( (socket.gethostbyname('localhost'), port) )

	except:
		handle_fail()
		#raise
		return

	body = "%s %2d %s" % (PROTO_VER, func, word) 
	msg = "%-4d%s" % (len(body), body)
	sock.send (msg)

	orgword = word
	
	buf = sock.recv (128)
	if len(buf) > 10 and buf[:3]=="ORG":
		pos = buf.find('\n',3)
		if pos != -1:
			orgword = buf[4:pos]
			#print "ORG: %s" % orgword
			buf = buf[pos:]

	print """<font color="blue"> <b>%s</b> </font> <br/><br/>""" % orgword
	sys.stdout.write(buf)

	while 1:
		buf = sock.recv (1024*2)
		if buf == '': break
		#print buf
		sys.stdout.write(buf)
 
	sock.close()


def handle_fail():
	print "<br/>애니딕 서버가 기동 중입니다. <br/>\n 잠시만 기다려 주세요. <br/>"  


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

PIDICDIR = '/var/www/html/dictimg/'
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



## HTML form 을 통해 GET 메소드로 온 parameter 값 구하기
def get_query(debug=0):
	global FUNC, WORD, QUERY

	forms = cgi.FieldStorage()
	for k in forms.keys():
		QUERY += "%s=%s\\&" % (k, forms[k].value.replace(' ','+'))

	#print forms.keys()

	try : FUNC = int(forms['F'].value)
	except: FUNC = 0 

	try : WORD = forms['W'].value.strip()
	except: WORD = '' 
 
	if len(WORD)>0 and WORD[0].isalpha():
		WORD = clean_word(WORD)

	if debug: 
		print "Func=%d Word=%s" % (FUNC, WORD)
		print "QUERY: %s" % QUERY


#### main
FUNC = 0
WORD = ''
QUERY = ''


if __name__=='__main__':

	debug = 0	

	print 'Content-Type: text/html\n'

	if len(sys.argv)>1: debug = 1
	
	get_query(debug)

	try:
		adtempl.do_upper(WORD)
	except:
		pass


	if WORD != '' and FUNC != 1:
		req_dic(sys.argv, FUNC, WORD)

	pidic(WORD)

	if WORD != '' and QUERY != '':
		exec_addic(QUERY)
		print "</table>"

	try: adtempl.do_lower()
	except: pass

	sys.stdout.flush()
	sys.stdout.close()

	## write WORD log
	write_log(WORD, FUNC)
