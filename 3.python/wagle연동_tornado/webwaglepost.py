#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

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

define("port", default=8888, help="run on the given port", type=int)


moimImgDict={}

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
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
        self.render("moimlogin.html")


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
        self.write("id=%s pass=%s" % (id, passwd))
	try:
		atoken = waglegood.login(id=id, passwd=passwd, mdn=MDN)
		self.set_secure_cookie("accesstoken", atoken)
	
		#self.write("id=%s pass=%s tok=%s" % (id, passwd, atoken))
		self.redirect("/moim/list")
	except:
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
