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
# $uid : string type. the actual value of user id. user id is a string like "handol". 
#        if a user id contains a white space, it must be given (converted before) as "%20".
# $cid : integer type. the actual value of contents id. 
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

import logging

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

	# load all the friends. <uid, [uid]> 
	def load_all_friends(self):
		try:
			query = "select userID, followerUserID from twt_follower_list where state=1 " 
			self.cursor.execute(query)
			rows = self.cursor.fetchall()
		except:
			return []
		print "loaded all friends", len(rows)
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
	def __init__(self, dbhandler, logger):
		## user hash table 
		self.usertab = {} 		
		## db handler
		self.dbhandler = dbhandler
		self.log = logger
		
	def add_contents_list(self):
		print('start load_all_contents()')
		self.log.info('start load_all_contents()')
		c_u_list = self.dbhandler.load_all_contents()
		self.log.info('finish load_all_contents()')
		self.log.info('# of contents = %d' % (len(c_u_list)))
		print('# of contents = %d' % (len(c_u_list)))
		for cu_pair in c_u_list:
			c = cu_pair[0] # content id
			u = cu_pair[1] # user id
			if len(u)==0: continue	
			user = self._get_user(u)	
			user[1].append(c)
		self.log.info("building usertab done: size=%d" % (len(self.usertab)))
		print("building usertab done: size=%d" % (len(self.usertab)))

	def add_friends_list(self):
		print('start load_all_friends()')
		self.log.info('start load_all_friends()')
		u_f_list = self.dbhandler.load_all_friends()
		self.log.info('finish load_all_friends()')
		self.log.info('# of friends = %d' % (len(u_f_list)))
		print('# of friends = %d' % (len(u_f_list)))
		for u_f_pair in u_f_list:
			u = u_f_pair[0] # content id
			f = u_f_pair[1] # user id
			if len(u)==0: continue	
			user = self._get_user(u)	
			user[0].append(f)
		self.log.info("building usertab done: size=%d" % (len(self.usertab)))
		print("building usertab done: size=%d" % (len(self.usertab)))

	def test(self):
		ulist = self.usertab.keys()
		#ulist.sort()
		for i in range(20):
			uinfo = self._get_user(ulist[i])
			print "[%s]" % ulist[i], uinfo 
	
	# private method
	def _get_user(self, uid):
		try:
			userinfo = self.usertab[uid]
			#self.log.info("usertab: found [%s]" % uid) 
		except:
			#self.log.info("usertab: not found [%s]" % uid) 
			userinfo = [ [], [], time.time() ]  # add empty follow_list and empty contents_list
			self.usertab[uid] = userinfo
		return userinfo
		
	## public to WagleCacheHandler
	def	timeline(self, uid, limit=100):		
		user = self._get_user(uid)	
	
		# build timeline from each friend
		c_list = []
		for friend in user[0]:
			f_info = self._get_user(friend)	
			c_list += f_info[1]
		c_list.sort()
		self.log.debug("CMD: timeline: uid=%s friends=%d timeline=%d" % 
			(uid, len(user[0]), len(c_list)))
		c_list = map(str, c_list)
		if len(c_list) > limit:
			c_list =  c_list[len(c_list)-limit : ]

		return ','.join(c_list)
	
	def	login(self, uid):
		# if a user log-in, then reload the follow list from DB
		user = self._get_user(uid)
		new_f_list = self.dbhandler.load_follow(uid)
		if len(new_f_list) > 0: 
			new_f_list.sort()
			# update usertab for 'uid'
			user[0] = new_f_list

		new_c_list = self.dbhandler.load_contents(uid)
		if len(new_c_list) > 0: 
			new_c_list.sort()
			# update usertab for 'uid'
			user[1] = new_c_list

		self.log.info("CMD: login: uid=%s friends=%d contents=%d" % 
			(uid, len(user[0]), len(user[1])))
		return 'OK'
	
	def	post(self, uid, cid):
		cid = int(cid)
		user = self._get_user(uid)	
		# check duplicate
		if cid not in user[1]:
			user[1].append(cid)
		else:
			self.log.warn("already posted: uid=%s cid=%d" % (uid, cid))
		self.log.debug("CMD: post: uid=%s cid=%d" % (uid, cid))
		return 'OK'
	
	def	follow(self, uid, uid2):
		user = self._get_user(uid)	
		# check duplicate
		if uid2 not in user[0]:
			user[0].append(uid2)
		else:
			self.log.warn("already follow: uid=%s uid2=%s " % (uid, uid2))
		self.log.debug("CMD: follow: uid=%s uid2=%s" % (uid, uid2))
		return 'OK'
	
	def	unfollow(self, uid, uid2):		
		user = self._get_user(uid)	
		if uid2 in user[0]:
			user[0].remove(uid2)
		else:
			self.log.warn("already unfollow: uid=%s uid2=%s " % (uid, uid2))
		self.log.debug("CMD: unfollow: uid=%s uid2=%s" % (uid, uid2))
		return 'OK'
	
## Wagle Cacher Server Module	
class WagleCacheHandler(BaseHTTPServer.BaseHTTPRequestHandler):
		
	def send_good(self, bodymsg, charset='utf-8'):
		#print "TO client: ", bodymsg 
		self.send_response(200)
		self.send_header("Content-type", "text/html;charset=%s" % charset)
		self.send_header("Content-Length", "%d" % len(bodymsg))
		self.end_headers()		
		self.wfile.write(bodymsg)
		
		
	def do_GET(self):
		#print "FROM client: ", self.path
		paras = self.path
		paras = unicode(paras, 'ascii')
		paras = paras.encode('utf-8')
		
		flds = paras.split('/')
		flds = filter(len, flds) # get the list of a string which is not empty. len(x) > 0
		uid = flds[1]
		
		logger.debug('REQ: %s' % ','.join(flds))

		res = ''
		if flds[0] == "timeline":
			res = waglecache.timeline(uid)
		elif flds[0] == "login":
			res = waglecache.login(uid)
		elif flds[0] == "post":
			res = waglecache.post(uid, flds[2])
		elif flds[0] == "follow":
			res = waglecache.follow(uid, flds[2])
		elif flds[0] == "unfollow":
			res = waglecache.unfollow(uid, flds[2])
		else:
			# 404 Not-found
			msg = 'Command "%s" not	supported !' % (flds[0])
			self.send_error(404, msg)
			return 

		self.send_good(res)
	

###### main()		
if __name__ == "__main__":
	global waglecache
	global logger
	PORT = 8000
	
	logger = logging.getLogger('wagle')
	hdlr = logging.FileHandler('./waglecache.log')
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr)
	logger.setLevel(logging.WARN)
	logger.info('==== starts: %s' % ' '.join(sys.argv))

	if len(sys.argv)==2:
		PORT = int(sys.argv[1])
	
	## load DB first
	## 211.233.77.6 = wagle 1st db
	## 211.233.77.7 = wagle 2nd db
	dbhandler = WagleDB('211.233.77.7')	
	waglecache = WagleCache(dbhandler, logger)
	waglecache.add_contents_list()
	waglecache.add_friends_list()
	#waglecache.test()
	
	print "serving at port", PORT		
	httpd = BaseHTTPServer.HTTPServer(("", PORT), WagleCacheHandler)
	
	## start web server
	httpd.serve_forever()
