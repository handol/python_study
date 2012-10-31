import httplib

def check_webpage(svraddr, webpage):
	try:
		#h = httplib.HTTPConnection(uri, timeout=10)
		conn = httplib.HTTPConnection(svraddr)
		conn.request("GET", webpage)
		res = conn.getresponse() 
		print webpage, "-->", res.status, res.reason
		return int(res.status)
	except:
		raise
		return 0

	

#check_webpage("http://211.233.77.14:8080/")
check_webpage('211.233.77.14:8080', '/')
check_webpage('211.233.77.14:8080', '/aa.txt')
check_webpage('211.233.77.14:8080', '/imgSvrOK.txt')
