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

import waglegood
import adminview
import time
import codecs

define("port", default=8888, help="run on the given port", type=int)


moimImgDict={}

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/43oETzKXQAGaYdkL5gEmGeJJFuYh", MainHandler),
            (r"/43oETzKXQAGaYdkL5gEmGeJJFuYh0", ClearHandler),
            (r"/moim/post", MoimPostHandler),
            (r"/login", LoginHandler),
            (r"/home", HomeHandler),
            (r"/logout", LogoutHandler),
            (r"/moim/list", MoimListHandler),
            (r"/moim/write/*", MoimWriteHandler)
        ]
        settings = dict(
            cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            #login_url="/login",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            #xsrf_cookies=True,
            xsrf_cookies=False,
            autoescape="xhtml_escape",
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json: return None
        return tornado.escape.json_decode(user_json)


class MainHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
	self.set_secure_cookie("xxx", "GeJJFuYh7EQnp2XdTP1o/Vo=")
        self.render("moimlogin.html")

class ClearHandler(BaseHandler):
    def get(self):
	self.clear_all_cookies()
	self.redirect("/")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("accesstoken")
        self.write("You are now logged out")
	#self.redirect("/")

import urllib
class LoginHandler(BaseHandler):
    def post(self):
        id = self.get_argument("userID", None)
	id = urllib.quote(id)
        passwd = self.get_argument("userPWD", None)
        MDN = self.get_argument("MDN", None)
	xxx = self.get_secure_cookie("xxx")
	if xxx != "GeJJFuYh7EQnp2XdTP1o/Vo=":
		self.redirect("/")
		return

	lasttime = self.get_secure_cookie("lasttime")
	try:
		lasttime = int(lasttime)
	except:
		lasttime = 0
	now = int(time.time())
	lasttime =  now
	if now - lasttime < 60*2:
		#self.write("you can acces ONLY onetime per minute !!<p>\n")
		daystr = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
		fname = id+".tweets." + daystr
		inf = codecs.open(fname, "r", "utf-8")	
		for line in inf.xreadlines():
			if line.find("Birzzle") != -1:
				self.write(line)
				self.write("<p>")
		inf.close()
		
		return
		
	self.set_secure_cookie("lasttime", str(int(time.time())))
	try:
		print id, passwd
		adminview.login(id=id, passwd=passwd)
		print adminview.TOKEN
		fname = adminview.mytimelineAll(atoken=adminview.TOKEN)
		inf = codecs.open(fname, "r", "utf-8")	
		for line in inf.xreadlines():
			if line.find("Birzzle") != -1:
				self.write(line)
				self.write("<p>")
		inf.close()
		
	except:
		raise
		self.redirect("/")

class HomeHandler(BaseHandler):
    def get(self):
	token = self.get_secure_cookie("accesstoken")
        self.write("token=%s" % (token))

####
def html_moimlist(obj):
	global moimImgDict
	res = ''
	res += """<table  align="center" border="0" cellspacing="0" cellpadding="0">"""
	
	moims = obj["gathList"]
	for moim in moims:
		line = \
 """<tr><td align="center"><a href="/moim/post?moimid=%s"> <img src="%s" width="60"></a></td>
&nbsp;<td>%s</td></tr>""" % \
		 (moim["gathID"], moim["imgPrvwPath"], moim["gathNm"])
		 #(moim["gathID"], moim["imgPrvwPath"], moim["gathAdminAuthYn"], moim["gathID"], moim["gathNm"])
		res += line
		moimid = moim["gathID"]
		moimid = str(moimid)
		moimImgDict[moimid] = moim["imgPrvwPath"]
	res += "</table>"
	return res


class MoimListHandler(BaseHandler):
    def get(self):
	token = self.get_secure_cookie("accesstoken")
	if token==None or len(token)<5: 
		self.redirect("/")
		return

	obj = waglegood.moimlist(atoken=token)
	if obj==None or len(obj)==0: 
		self.redirect("/")
		return
	res = html_moimlist(obj)
        self.write(res)


class MoimPostHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        moimid = self.get_argument("moimid")
	moimid = str(moimid)
	self.set_secure_cookie("moimid", moimid)
	try:
		moim_img_url = moimImgDict[moimid]
	except:
		moim_img_url = ""
	print "MOIM", moimid, moim_img_url
        self.render("moimpost.html", moimimgurl=moim_img_url)
	print moimid


class MoimWriteHandler(BaseHandler):
    def post(self):
	token = self.get_secure_cookie("accesstoken")
	moimid = self.get_secure_cookie("moimid")
	print token, moimid
	content = self.get_argument("content")
	waglegood.moimpost(atoken=token, gathID=moimid, wterConts=content)
	self.redirect("/moim/post?moimid=%s" % moimid)
	


def main():
    tornado.options.parse_command_line()
    app = Application()
    print "tornado server: port=%d" % options.port
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
