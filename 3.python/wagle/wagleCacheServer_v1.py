#!/usr/bin/env python
# 
### -*- coding: UTF8 -*-
# @author handol@gmail.com
# @date 2011/04/23
# @start 2011/04/23 13:00
# @finish 2011/04/23 13:00
#
# Cache server for Wagle
#
# === serving URLs ===
# /login/$uid
# /post/$uid/$cid
# /follow/$uid/$uid2
# /unfollow/$uid/$uid2
#
# === meaning of each URL ===
# $uid : the actual value of user id. user id is a string like "handol". 
#        if a user id contains a white space, it must be given (converted before) as "%20".
# $cid : the actual value of contents id. 
#
# /login
#   ex) /login/handol --> a user 'handol' logged in
# /post
#   ex) /post/handol/12345 --> a user 'handol' posted a tweet, whose contents id is '123456'
# /follow
#   ex) /follow/handol/aldotori --> a user 'handol' follows a user 'aldotori'
# /unfollow
#   ex) /unfollow/handol/aldotori --> a user 'handol' unfollows a user 'aldotori'

import sys
import time
import BaseHTTPServer
import pyodbc

# ODBC: {MySQL} must be defined  /etc/odbcinst.ini 
## DB handler for Wagle		
class WagleDB:
	def __init__(self, ipaddr, port='3306'):			
		self.conn_str = 'DRIVER={MySQL};CHARSET=UTF8;SERVER=%s;PORT=%s;DATABASE=lgu;UID=lgu;PWD=lgu_pwd!' % (ipaddr, port)
		self.cnxn = None
		self.cursor = None
		
		self.open_db()
	
	def open_db(self):
		self.close_db()
		
		self.cnxn = pyodbc.connect(self.conn_str)
		self.cursor = self.cnxn.cursor()
	
	def close_db(self):
		if self.cursor:	self.cursor.close()
		if self.cnxn:	self.cnxn.close()
	
	# load all the contents. <cid, uid> 
	def load_all_contents(self):
		try:
			query = "select contentID, userID from twt_contents where isDel=0 " 
			self.cursor.execute(query)
			rows = self.cursor.fetchall()
		except:
			return []
		print "loaded all contents", len(rows)
		return rows
		
	# load the list of contents which a user 'uid' has posted
	def load_contents(self, uid, limit=1000):
		try:
			query = "select contentID, userID from twt_contents where userID='%s' and isDel=0 limit %d" % (uid, limit)
			self.cursor.execute(query)
			rows = self.cursor.fetchall()
		except:
			return []
		print "loaded contents: uid=", uid, len(rows)
		return rows
	
	# load the list of users whom a user 'uid' follows	
	def load_follow(self, uid, limit=1000):
		try:
			query = "select followerUserID from twt_follower_list where userID='%s' and state=1  limit %d" % (uid, limit)
			self.cursor.execute(query)
			rows = self.cursor.fetchall()
		except:
			return []
		print "loaded friend: uid=", uid, len(rows)
		return rows
	

# usertab
# key: user id,  value: [follow_list, users_contents_list, update_time] 
class WagleCache:
	def __init__(self, dbhandler):
		## user hash table 
		self.usertab = {} 		
		## db handler
		self.dbhandler = dbhandler
		
	def add_contents_list(self):
		c_u_list = self.dbhandler.load_all_contents()
		for cu_pair in c_u_list:
			c = cu_pair[0] # content id
			u = cu_pair[1] # user id
			
			user = self._get_user(u)	
			user[1].append(c)
	
	# private method
	def _get_user(self, uid):
		try:
			userinfo = self.usertab[uid]
		except:
			userinfo = [ [], [], time.time() ]  # add empty follow_list and empty contents_list
			self.usertab[uid] = userinfo
		return userinfo
		
	## public to WagleCacheHandler
	def	timeline(self, uid):		
		user = self._get_user(uid)	
		return user[1]
	
	def	login(self, uid):
		# if a user log-in, then reload the follow list from DB
		user = self._get_user(uid)
		new_f_list = self.dbhandler.load_follow(uid)
		if len(new_f_list) > 0:
			user[0] = new_f_list
	
	def	post(self, uid, cid):
		user = self._get_user(uid)	
		user[1].append(cid)
	
	def	follow(self, uid, uid2):
		user = self._get_user(uid)	
		user[0].append(uid2)
	
	def	unfollow(self, uid, uid2):		
		user = self._get_user(uid)	
		user[0].remove(uid2)
	
## Wagle Cacher Server Module	
class WagleCacheHandler(BaseHTTPServer.BaseHTTPRequestHandler):
		
	def send_good(self, bodymsg):
		print "TO client: ", bodymsg 
		self.send_header("Content-type", "text/html;charset=euc-kr")
		self.send_header("Content-Length", "%d" % len(bodymsg))
		self.end_headers()		
		self.wfile.write(bodymsg)
		
	def send_errmsg(self, bodymsg, errcode):
		print "TO client: ", bodymsg 
		self.send_error(errcode)
		self.send_header("Content-type", "text/html;charset=euc-kr")
		self.send_header("Content-Length", "%d" % len(bodymsg))
		self.end_headers()		
		self.wfile.write(bodymsg)
		
		
	def do_GET(self):
		print "FROM client: ", self.path
		flds = self.path.split('/')
		flds = filter(len, flds) # get the list of a string which is not empty. len(x) > 0
		
		if flds[0] == "login":
			waglecache.login(flds[1])
		elif flds[0] == "post":
			waglecache.post(flds[1], flds[2])
		elif flds[0] == "follow":
			waglecache.follow(flds[1], flds[2])
		elif flds[0] == "unfollow":
			waglecache.unfollow(flds[1], flds[2])
		else:
			pass
		self.send_good("hello")
	

###### main()		
if __name__ == "__main__":
	global waglecache
	PORT = 8000
	
	if len(sys.argv)==2:
		PORT = int(sys.argv[1])
	
	## load DB first
	## 211.233.77.6 = wagle 1st db
	## 211.233.77.7 = wagle 2nd db
	dbhandler = WagleDB('211.233.77.7')	
	waglecache = WagleCache(dbhandler)
	waglecache.add_contents_list()
	
	print "serving at port", PORT		
	httpd = BaseHTTPServer.HTTPServer(("", PORT), WagleCacheHandler)
	
	## start web server
	httpd.serve_forever()
