#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: 한대희
#         daheehan@lguplus.co.kr 
#         handol@gmail.com 
#         010-8080-5909
#
import urllib2
import time
import hashlib
import json

# 주의사항: 발급받은 appID, appKey로 변경하여야 한다.
#            appID, appKey 가 잘못되면 실적 정산이 제대로 되지않는다.
MY_APPID = 'lgtemp'
MY_APPKEY = 'yS4rPk2DDpbl8+3IuI7G2I55IY8=#MTM='
#
def login(host='https://m2.wagle.me', id='handola', passwd='gksehf', mdn='01080805909'):
	# passwd는 SHA-1 방식으로 인코딩한 후 hex 문자열로 변환하여야 한다.
	# ex) "handola" --> "f3e9e6e4ac00b618302b2218ea51407e38b8ad91"
	sha = hashlib.sha1()
	sha.update(passwd)
	passwdenc = sha.hexdigest()
	
	# 주의사항: wagle ID에 한글인 경우도 있다. URL에 한글포함하는 처리를 별도로 해주어야 한다. 
	url = "%s/v3.0/account/login?userId=%s&userPw=%s" % (host, id, passwdenc)
	print "URL:", url
	
	# HTTP Request 에 아래와 같이 wagle용 header 값을 설정하여야 한다.
	req = urllib2.Request(url)
	req.add_header("Accept", "*/*")
	req.add_header("Host", "m2.wagle.me")
	req.add_header("Content-Type", "application/x-www-form-urlencoded")	
	req.add_header("App-Agent", "Etc;Etc;01080805909;%s;1.0;Etc;Etc" % MY_APPID)
	req.add_header("AKey", MY_APPKEY)
	#print "HEADERS:", req.headers
	
	# HTTP Response 에는 JSON 메시지가 담겨있다.
	try:
		u = urllib2.urlopen(req)
		res = u.read()		
		decoder = json.JSONDecoder()
		obj,end = decoder.raw_decode(res)
		# resultCode==0 이면 login 성공, 그외는 실패
		rescode = obj["resultCode"]
		if rescode == 0:
			print "Login Success !!"
		else:
			print "Login Fail !! ID 및 password를 확인하세요."
			
		print "RESULTCODE:", obj["resultCode"]
		print "JSON MESG:", obj		

	except urllib2.URLError, e: 
		print "<-- error", e
		#print e.read()


#####################################		
if __name__ == "__main__":
	print "##### 로그인 성공 케이스 ####"
	login(passwd='gksehf')

	print "\n\n"
	print "##### 로그인 실패 케이스 ####"
	login(passwd='gksehfxx')
