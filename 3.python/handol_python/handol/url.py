import urllib
import urllib2

def check_webpage(uri):
	try:
		h = urllib.urlopen(uri)
		print h.info()
		#print h.getcode()
	except:
		return 0

def check_webpage2(uri):
	try:
		h = urllib2.urlopen(uri)
		print h.info()
		#print h.getcode()
	except:
		#print urllib2.HTTPError.code
		return 0
	
	

check_webpage("http://211.233.77.14:8080/")
check_webpage("http://211.233.77.14:8080/imgSvrOK.txt")
check_webpage("http://211.233.77.14:8080/aa")
