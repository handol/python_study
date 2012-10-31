#!/usr/bin/env python

import logging
import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import uuid
from tornado.options import define, options
import time
import codecs

define("port", default=9123, help="run on the given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/clear", ClearHandler),			
			(r"/[0-9\-]+", LogHandler)		   
		]
		settings = dict(
			cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
			#login_url="/login",
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			#xsrf_cookies=True,
			xsrf_cookies=False,
			#autoescape="xhtml_escape",
			autoescape="none"
		)
		tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		user_json = self.get_secure_cookie("user")
		if not user_json: return None
		return tornado.escape.json_decode(user_json)


class MainHandler(BaseHandler):	
	def get(self):
		try:
			datestr = self.get_argument("file")
		except:
			self.write("""<p> try "?file=xxx" <p>""")
			return
		print datestr
		load_file(datestr, self)

class ClearHandler(BaseHandler):
	def get(self):
		self.clear_all_cookies()
		self.redirect("/")

class LogHandler(BaseHandler):
	def get(self):
		self.clear_cookie("accesstoken")
		self.write("You are now logged out")
		#self.redirect("/")


def load_file(fname, outf):
	#inf = codecs.open(fname, "r", "utf-8")
	try:
		inf = open(fname)
	except:
		outf.write("<p> file name NOT good<p> " + fname)
		return
	for line in inf.xreadlines():		
		outf.write(line)		
	inf.close()

####
def main():
	tornado.options.parse_command_line()
	app = Application()
	print "tornado server: port=%d" % options.port
	app.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
