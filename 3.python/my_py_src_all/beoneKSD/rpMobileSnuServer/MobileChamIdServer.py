#!/usr/bin/python
# -*- coding: EUC-KR -*-
# 2008/3/10

import SocketServer

class MyHandler(SocketServer.BaseRequestHandler):
	mymesg = "Orginal val"

	@staticmethod
	def setMyMesg(msg):
		MyHandler.mymesg = msg

	def handle(self):
		ipaddr, port =  self.request.getpeername()
		#print "Remote: ", ipaddr, port

		print MyHandler.mymesg
		chamid = ChamIdServer(self.request)
		chamid.run()
		

## mimic Java's StringTokenizer
class	StringTokenizer:
		def __init__(self, orgstr, delimiter):
			self.flds = orgstr.split(delimiter)
			self.idx = 0
		
		def nextToken(self):
			if self.idx >= len(self.flds):
				return ""
	
			token = self.flds[self.idx]
			self.idx += 1
			return token

		# return n tokens
		def nToken(self, n):
			if self.idx >= len(self.flds):
				return [] 
			tmpidx = self.idx

			self.idx += n
			if self.idx >= len(self.flds):
				self.idx = len(self.fds)

			return self.flds[tmpidx:]

		# return all the token left so far
		def allToken(self):
			if self.idx >= len(self.flds):
				return [] 
			return self.flds[self.idx:]
			
	


## ChamId Server's Client Hander. Main Biz Logic
import time
import InsertMobileId
import DbChamDemo

NUM_PATTERNS = 5
PASSWD_LENG = 4

class	ChamIdServer:
	def __init__(self, cliSock):
		self.cliSock = cliSock
		self.cliIp, self.cliPort =  self.cliSock.getpeername()
		self.CONST_THSHD = 300

		print "Client: %s:%d" % (self.cliIp, self.cliPort)

	def run(self):
		self.db = DbChamDemo.login()
		msg = self.cliSock.recv(1000)
		print msg
		self.cliSock.send("from Server : " + msg)
		cnt = 0
		while True:
			time.sleep(2)
			print "port=%d" % (self.cliPort)

		self.db.close()

	def parse(self, orgmsg):
		# convert utf8 to euc-kr
		msg = unicode(orgmsg, "utf-8")
		#msg = msg.encode("euc-kr", "ignore")
		token = StringTokenizer(msg, None) # delimiter == all white spaces (space, tab, ...)
		
		moduleType = token.nextToken();
		userID = token.nextToken();
		
		if moduleType=="NEWID":
			self.newId(userId)
		elif moduleType=="Enroll":
			self.enroll(token)
		else:

	def newId(self, id):
		if InsertMobileId.isNewId(self.db, id):
			replyMsg = "ID 사용 가능"
		else:
			replyMsg = "사용 중인 ID"
		return replyMsg
			
	def enroll(self, token, id):
		passwd = token.nextToken()

		for i in range(NUM_PATTERNS):
			pattern = token.nToken(PASSWD_LENG*2-1)
			if len(pattern) != PASSWD_LENG*2-1:
				break
			# insert into "ksdlog" table

		replyMsg = "등록 완료"
		return replyMsg

	def auth(self, token, id):
		passwd = token.nextToken()
	
		if InsertMobileId.isNewId(id):
			replyMsg = "로그인 실패\nID 미등록"
		else:
			if InsertMobileId.isPasswdCorrect(self.db, id, passwd):
				replyMsg = self.applyModel(token, id)
			else:
				replyMsg = "로그인 실패\n문자열 오류"
		return replyMsg

	
	def applyModel(self, token, id):
		pattern = token.nToken(PASSWD_LENG*2-1)
		if len(pattern) != PASSWD_LENG*2-1:
			replyMsg = "로그인 실패\n"
			return replyMsg

		pattern = map(int, pattern)
		given_thshd = token.nextToken()
		if given_thshd != "":
			CONST_THSHD = int(given_thshd)

		if CONST_THSHD == 300:
			c_thd = 1.6
		elif CONST_THSHD == 400:
			c_thd = 2.2
		elif CONST_THSHD == 500:
			c_thd = 2.8
		else:
			c_thd = 2.8


		result = "로그인 성공\n"+(int)temp+" (MAX:" + c_thd*temp2 + ")";
		result = "로그인 실패\n"+(int)temp+" (MAX:" + c_thd*temp2 + ")";


# #
def start_server(port):
	myServer = SocketServer.ThreadingTCPServer(('',port), MyHandler)
	myServer.allow_reuse_address = True
	myServer.serve_forever( )

if __name__=="__main__":
	import sys

	MyHandler.mymesg = "Jennifer"
	MyHandler.setMyMesg("Handol")

	if len(sys.argv) > 1:
		start_server(int(sys.argv[1]))
