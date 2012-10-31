#Copyright Jon Berg , turtlemeat.com

import string,cgi,time
import os
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import sys

import beautiful

#import pri

def	logit(msg):
	try:
		fp = open("httplog.txt", "a")
	except:
		print "Logging Failed"
		return

	tm = time.localtime()
	tmstr = "%d/%02d/%02d %02d:%02d:%02d\n" % (tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec)
	fp.write(tmstr)
	fp.write(msg)
	fp.write("\n\n")
	fp.close()

def getcgivars():
	forms = cgi.FieldStorage()
	print forms


def test_cgi():
	print "<strong>Python %s</strong>" % sys.version
	keys = os.environ.keys( )
	keys.sort( )

	print "<pre>"
	for k in keys:
		print "%s\t%s" % (cgi.escape(k), cgi.escape(os.environ[k]))
	print "</pre>"


class MyHandler(BaseHTTPRequestHandler):

	def do_debug(self):
		print dir(self)
		print self.client_address
		print self.address_string()
		#test_cgi()
		getcgivars()

		print "HEADER"
		print dir(self.headers)
		print self.headers

		print "PARAM"
		print self.path
		print self.headers.getparamnames()
		print self.headers.getplist()

		if os.environ.has_key("REMOTE_ADDR"):
			print "REMOTE", cgi.escape(os.environ["REMOTE_ADDR"])

		print "CLASS", self.headers.__class__.__name__
		print self.headers.getencoding()

	def do_pretty(self, url):
		if not url.startswith("http://"):
			url = "http://" + url
		print "URL=", url
		charset, html = beautiful.prettify_url(url)
		html = "============== %s ==========" % (html)
		contentType = 'text/plain; charset=%s' % (charset)

		self.send_response(200)
		self.send_header('Content-type',	contentType)
		self.send_header('Content-length',	str(len(html)))
		self.end_headers()
		self.wfile.write(html)


	def do_GET(self):
		self.do_debug()
		useragent = self.headers.getheader('user-agent')
		print "AGENT = %s" % (useragent)
		if useragent.find('Windows') == -1:
			logit(str(self.headers))

		if useragent.find("SKT") != -1:
			print "==== SKT ===="
		else:
			print "==== KTF ===="

		if self.path == '/':
			self.path = 'index.html'

		if self.path.startswith("/pretty?"):
			self.do_pretty(self.path[8:])
		else:
			self.do_serv_file()


	def do_serv_file(self):
		try:
			print "PATH:", self.path
			self.serv_file()

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	def serv_file(self):
		f = open(curdir + sep + self.path) #self.path has /test.html
		self.send_response(200)
		if self.path.find('utf') != -1:
			contentType = 'text/html; charset=utf-8'
		else:
			contentType = 'text/html; charset=euc-kr'

		self.send_header('Content-type',	contentType)
		self.end_headers()
		self.wfile.write(f.read())
		f.close()

	def serv_time(self):
		self.send_response(200)
		if self.path.find('utf') != -1:
			contentType = 'text/html; charset=utf-8'
		else:
			contentType = 'text/html; charset=euc-kr'

		self.send_header('Content-type',	contentType)
		self.end_headers()
		self.wfile.write("hey, today is the" + str(time.localtime()[7]))
		self.wfile.write(" day in the year " + str(time.localtime()[0]))
			

	def do_POST(self):
		global rootnode
		try:
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				query=cgi.parse_multipart(self.rfile, pdict)
			self.send_response(301)
			
			self.end_headers()
			upfilecontent = query.get('upfile')
			print "filecontent", upfilecontent[0]
			self.wfile.write("<HTML>POST OK.<BR><BR>");
			self.wfile.write(upfilecontent[0]);
			
		except :
			pass

def main(port=8200):
	try:
		server = HTTPServer(('', port), MyHandler)
		print 'started httpserver...'
		server.serve_forever()
	except KeyboardInterrupt:
		print '^C received, shutting down server'
		server.socket.close()


if __name__ == '__main__':
	if len(sys.argv) > 1:
		port = int(sys.argv[1])
	else:
		port = 8200
	print "start serving at port %d" % (port)
	main(port)

