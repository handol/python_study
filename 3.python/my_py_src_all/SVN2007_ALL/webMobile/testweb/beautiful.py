#!/usr/bin/env python
# -*- coding: euc-kr -*-
import urllib
import urlparse
import httplib
import urllib2

import BeautifulSoup

#httplib.HTTPConnection.debuglevel = 1 

urllib.URLopener.version = (	
		'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.7.8) '	
		'Gecko/20050609 Firefox/1.0.4')

def get1(urlstr):
	fp = urllib.urlopen(urlstr)
	html = fp.read()
	#print fp.headers
	cont_type = fp.headers['content-type']
	cont_type = cont_type.strip().upper()
	pos = cont_type.find("CHARSET=")
	if pos != -1:
		charset = cont_type[pos+8:]
	else:
		charset = "EUC-KR"
	#print len(html)

	return charset, html

def get2(urlstr):
	request = urllib2.Request(urlstr)
	opener = urllib2.build_opener()
	f = opener.open(request)
	#print f.status
	print f.url

def getHEAD(urlstr):
	urlfields = urlparse.urlparse(urlstr)
	host = urlfields[1]
	path = "".join(urlfields[2:])
	#path = "".join(list(urlfields[2:]))
	#print "Host = %s" % (host)
	#print "path = %s" % (path)
	conn = httplib.HTTPConnection(host)
	conn.request("HEAD", path)
	r2 = conn.getresponse()
	#print r2.getheaders()
	print r2.getheader('location')


urlstr = "http://blog.joins.com/media/go_Random_Blog.asp"

#get2(urlstr)


def get_text(htmltree):
	text = ""
	for item in htmltree:

		#print item, item.__class__.__name__
		if item.__class__.__name__ == "Tag":
			text += get_text(item)
		else:
			text += item
	return text


def saveLink(soup, out):
	for link in soup('a'):
		#print link
		if link.has_key('href'):
			href = link['href'].strip()
			out.write(href)
			out.write('\n')
		else:
			print "***", link

		#print link.contents
		try:
			link_name = get_text(link.contents)
			link_name = link_name.strip()
			print link_name.encode()
			out.write(link_name)
			out.write('\n\n')
		except:
			pass


def prettify_url(url):
	charset, html = get1(url)
	#print "CHARSET = ", charset
	soup = BeautifulSoup.BeautifulSoup(html, fromEncoding=charset)
	return charset, str(soup.body.prettify())


import sys
import codecs

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print "usage: -pretty url outfile"
		print "usage: -link url outfile"

		charset, html = prettify_url('http://www.anydic.com')
		print charset, html
		sys.exit(0)

	charset, html = get1(sys.argv[2])
	soup = BeautifulSoup.BeautifulSoup(html, fromEncoding=charset)
		
	#for i in dir(soup):
	#	print i

	#print "HEAD:", soup.head

	menu = sys.argv[1]
	if menu[0]=='-':
		menu = menu[1:]

	outfile = sys.argv[3]

	try:
		out = codecs.open(outfile, encoding='euc-kr', mode='w+')
	except:
		print "write fail:", outfile
		raise
		sys.exit(0)

	if menu == "pretty":
		print soup.prettify()
	elif menu == "link":
		saveLink(soup, out)


