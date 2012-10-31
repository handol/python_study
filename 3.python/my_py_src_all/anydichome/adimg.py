#!/usr/bin/env python
# -*- coding: EUC-KR -*-

RESPMESG = """Content-Length: %d\r\nConnection: close\r\nContent-Type: image/jpeg\r\n\r\n"""

import cgi
import AdEncrypt

def LoadImage():
	forms = cgi.FieldStorage()
	imgid = forms.getvalue("id")
	if imgid==None:
		return ""
		
	cr = AdEncrypt.AdEncrypt()
	goodimgid = cr.decode(imgid)
	imgfile = "pidicimg/%s.jpg" % (goodimgid)
	
	try:
		fp = open(imgfile, "r")
		imgdata = fp.read()
	except:
		imgdata = ""
	return imgdata
		

def Send(fp, imgdata):
	fp.write(RESPMESG % len(imgdata))
	fp.write(imgdata)
	
	
if __name__=="__main__":
	import sys
	
	imgdata = LoadImage()
	Send(sys.stdout, imgdata)
