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
def showuserjoin(host='https://m2.wagle.me', id='handola'):	
	# 주의사항: wagle ID에 한글인 경우도 있다. URL에 한글포함하는 처리를 별도로 해주어야 한다. 
	url = "%s/v3.0/account/showUserJoin/%s" % (host, id)
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
		print obj
		
		# 회원가입시간. int형. epoch time.
		# 1/1,000 초 단위까지 포함한 것으므로, 1000으로 나누면 초단위가 된다.		
		currsec = int(time.time())  # 초단위
		joinsec = int (obj["userJoinDttm"] / 1000) # 초단위로 변환

		print "JOIN TIME:", joinsec
		print "CURR TIME:", currsec
		
		# 72 시간 비교
		if (currsec - joinsec) > 3600*24*3: 
			print	"==> 가입한지 72시간이 초과하였습니다"
		else:
			print	"==> 신규가입자입니다."
		
		print "JSON MESG:", obj		

	except urllib2.URLError, e: 
		print "<-- error", e
		#print e.read()


#####################################		
if __name__ == "__main__":
	print "##### 회원 가입 시간 조회 ####"
	showuserjoin(id='handol')



