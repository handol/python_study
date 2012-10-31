#!/usr/bin/env python
# -*- coding: cp949 -*-

import urllib
import urllib2
import time
import hashlib
import base64
import json
import codecs
import os

"""
GET /v3.0/account/login?userId=handola&userPw=f3e9e6e4ac00b618302b2218ea51407e38b8ad91 HTTP/1.1
Accept: */*
Host: m2.wagle.me:8070
Content-Type: application/x-www-form-urlencoded
Accept-Encoding: deflate
App-Agent: Android;Android OS2.1.2;01080805909;wagle;3.0;SHW-M130L;WiFi

"""

TOKEN=''
USERSEQ='12345'
BOUNDARY="--$%handol%$--"

def get_multipart_header():
	return "multipart/form-data;boundary=%s" % BOUNDARY

def build_multipart_posting(fields):
	"""
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
	"""
	# fields = {"accessType":'010', "text":'Hi~~'}
	#print fields
	CRLF = '\r\n'
	L = []
	for key, value in  fields.iteritems():
		L.append('--'+BOUNDARY)
		L.append('Content-Disposition: form-data; name="%s"' % key)
		L.append('') # add empty line
		L.append(value)
	L.append('--' + BOUNDARY + '--')
	L.append('') # add empty line
	body = CRLF.join(L)
	return body
	
def get_val(obj):
	global TOKEN, USERSEQ

	print obj
	loginfo = obj["loginInfo"]
	if loginfo == None:
		return ""
	#print loginfo
	acesToken = loginfo["acesToken"]
	#print "acesToken=", acesToken
	userSeq = loginfo["userSeq"]
	#print "userSeq=", userSeq
	seqenc = base64.b64encode(str(userSeq))
	token = acesToken+"#"+str(userSeq)
	atoken = acesToken+"#"+seqenc

	USERSEQ = str(userSeq)
	TOKEN = atoken
	print "TOKEN, USERSEQ", TOKEN, USERSEQ

	return atoken


def basic_headers(req, mdn):
	req.add_header("Accept", "*/*")
	req.add_header("Host", "m2.wagle.me")
	req.add_header("Content-Type", "application/x-www-form-urlencoded")
	req.add_header("App-Agent", "Android;Android OS2.1.2;%s;wagle;3.0;SHW-M130L;WiFi" % mdn)
	req.add_header("App-Agent", "Etc;Etc;%s;wagle;3.0;SHW-M130L;WiFi" % mdn)
	req.add_header("AKey", "KZLv9SqivAwAyDR7R6HPn36STIs=#MA==")



def proc_res(req):
	print "-->", req.get_full_url()
	try:
		u = urllib2.urlopen(req)
		res = u.read()
		#print res

		#sss = res.decode('utf-8')
		sss = res
		decoder = json.JSONDecoder()
		obj,end = decoder.raw_decode(sss)
		#print obj, end
		return obj

	except urllib2.URLError, e: 
		print "<-- error", e
		print e.read()
		return None 

####
LOGIN_ID = 'handola'

def login(host='https://m2.wagle.me', id='handola', passwd='gksehf',
	  mdn='01080805909'):
	global   LOGIN_ID
	LOGIN_ID = id
	sha = hashlib.sha1()
	sha.update(passwd)
	passwdenc = sha.hexdigest()
	id = id.encode('utf-8')
	url = "%s/v3.0/account/login?userId=%s&userPw=%s" % (host, id, passwdenc)
	print url
	req = urllib2.Request(url)
	basic_headers(req, mdn)
	obj = proc_res(req)
	atoken = ""
	if obj:
		atoken = get_val(obj)
	return atoken

	

def post(host='https://m2.wagle.me', mdn='01080805909', 
	 atoken='abcde', 
	 accessType="010", text="Hi ~~"):
	url = "%s/v3.0/statuses/update" % (host)
	text = text.decode('euc-kr')
	text = text.encode('utf-8')

	req = urllib2.Request(url)
	basic_headers(req, mdn)	
	req.add_header("accessToken", atoken)
	req.add_header("Content-Type", get_multipart_header())
	
	#postdata = u"""{"accessType":%s,"text":%s}""" % (accessType, text)
	fields = {}
	fields["accessType"] = accessType
	fields["text"] = text
	postdata = build_multipart_posting(fields)
	req.add_data(postdata)
	#print postdata
	#print req.get_method()
	#print req.headers
	#print dir(req)
	
	obj = proc_res(req)
	print obj
	
def show(host='https://m2.wagle.me', mdn='01080805909', userseq='12345',
	 atoken='abcde'):
	url = "%s/v3.0/account/show/%s" % (host, userseq)
	print url
	print atoken
	req = urllib2.Request(url)
	basic_headers(req, mdn)	
	req.add_header("accessToken", atoken)
	obj = proc_res(req)

def read_cid_from_tweets():
	try:
		inf = codecs.open(outfname, "r", "utf-8")
		#inf.seek(-2000, os.SEEK_END)
		while 1:
                        
			line = inf.readline()
			#line = line.decode('utf-8')
			if len(line)==0: break
			if line[0]=='[':
				try:
					startid = int(line[1:9])
				except:
					print line
		inf.close()
	except:
		raise
		startid = 0

# mesges from me	
def mytimelineAll(host='https://m2.wagle.me', mdn='01080805909', atoken='abcde'):
	daystr = time.strftime("%Y-%m-%d", time.localtime(int(time.time())))
	outfname = LOGIN_ID+".tweets." + daystr
	PAGESIZE = 200
	startid = 0;
	print "startid = ", startid
        
	if startid>0:
		url = "%s/v3.0/statuses/myTimelineAll?lineContentsId=%d&pageSize=%d&direction=0" % (host, startid, PAGESIZE)
	else:
		url = "%s/v3.0/statuses/myTimelineAll?pageSize=%d&direction=0" % (host, PAGESIZE)
		
	print url
	#print atoken
	req = urllib2.Request(url)
	basic_headers(req, mdn)	
	req.add_header("accessToken", atoken)
	obj = proc_res(req)
	#print obj
	#outf = open(LOGIN_ID+".tweets", "a")
	outf = codecs.open(outfname, "a", "utf-8")
	line = "=== %s ===\n" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))))
	outf.write(line)
	contents = obj['contents']
	contents = sorted(contents, key=lambda x: x['id'])
	max_cid = startid
	for ctents in contents:
		cid = ctents['id']
		if cid > max_cid: max_cid = cid
		
		t = ctents['createdAt']
		t = t/1000
		time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(1313646439))
		tstr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
		line = "[%8d] %s\t%s\t%s\n" % (cid, tstr, ctents['author']['displayId'], ctents['text'])
		outf.write(line)
	outf.close()
	
# tweets, mesges to me
def mytimeline(host='https://m2.wagle.me', mdn='01080805909', atoken='abcde'):
	url = "%s/v3.0/statuses/myTimelineMe" % (host)
	print url
	print atoken
	req = urllib2.Request(url)
	basic_headers(req, mdn)	
	req.add_header("accessToken", atoken)
	obj = proc_res(req)
	#print obj
	contents = obj['contents']
	for ctents in contents:
		t = ctents['createdAt']
		#print t
		t = t/1000
		time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(1313646439))
		tstr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
		print tstr, ctents['author']['displayId'], ctents['text']

# mesges from me	
def mydirectmesg(host='https://m2.wagle.me', mdn='01080805909', atoken='abcde'):
	url = "%s/v3.0/statuses/userTimeline?pageSize=10&direction=0" % (host)
	print url
	print atoken
	req = urllib2.Request(url)
	basic_headers(req, mdn)	
	req.add_header("accessToken", atoken)
	obj = proc_res(req)
	#print obj
	contents = obj['contents']
	for ctents in contents:
		t = ctents['createdAt']
		t = t/1000
		time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(1313646439))
		tstr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
		print tstr, ctents['author']['displayId'], ctents['text']
	
def proc_moinlist(obj):
	moims = obj["gathList"]
	for moim in moims:
		print moim["gathAdminAuthYn"], moim["gathID"], moim["gathNm"] 
                
def moimlist(host='https://m2.wagle.me', mdn='01080805909', atoken='abcde'):
	url = "%s/v3.0/community/myCommunity" % (host)
	print url
	print atoken
	req = urllib2.Request(url)
	basic_headers(req, mdn)	
	req.add_header("accessToken", atoken)
	obj = proc_res(req)
	print obj
	proc_moinlist(obj)

def moimpost(host='https://m2.wagle.me', mdn='01080805909', 
	 atoken='abcde',
	 gathID='12345',
	 wterConts="Hi ~~"):
	url = "%s/v3.0/community/%s/docs/create" % (host, gathID)
	wterConts = wterConts.decode('euc-kr')
	wterConts = wterConts.encode('utf-8')

	req = urllib2.Request(url)
	basic_headers(req, mdn)	
	req.add_header("accessToken", atoken)
	req.add_header("Content-Type", get_multipart_header())

	fields = {}
	fields["wterConts"] = wterConts
	fields["shortUrlYn"] = 'N'
	fields["leadYn"] = 'N'
	fields["gathID"] = gathID
	postdata = build_multipart_posting(fields)
	req.add_data(postdata)
	
	obj = proc_res(req)
	



if __name__ == "__main__":
	import sys
	import urlparse

	HOST = 'https://m2.wagle.me'    # The remote host
	#HOST = 'http://m2.wagle.me:8070'    # The remote host

	# LOGIN ID = wagleAdmin
	login(host=HOST, id='wagleAdmin', passwd='615746')
	
	# LOGIN ID = handola
	#login(host=HOST)
	
	#mydirectmesg(host=HOST, atoken=TOKEN)
	#mytimeline(host=HOST, atoken=TOKEN)
	
	# save file: ID.tweets
	mytimelineAll(host=HOST, atoken=TOKEN)
	
	#show(host=HOST, userseq='12345', atoken=TOKEN)

	#post(host=HOST, atoken=TOKEN, accessType='020', text='이제 태풍이 지나간걸까요?')

	#moimlist(host=HOST, atoken=TOKEN)
	#moimpost(host=HOST, atoken=TOKEN, gathID='368', wterConts='아자 한돌') 
