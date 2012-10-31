import time
import os
import socket
import httplib

def get_cmd_result_as_int(cmd):
	res = os.popen(cmd).read()
	res = res.strip()
	if len(res) == 0:
		return 0 
	return int(res)


def check_svr_port(svrip, svrport):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setblocking(0)
	sock.settimeout(1)
	msg = "%s:%d" % (svrip, svrport)
	try:
		sock.connect((svrip, svrport))
		sock.close()
		print "%s\t-- OK" % (msg)
		return 1
	except:
		print "%s\t-- Error" % (msg)
		return 0



############
def check_webpage(svraddr, webpage):
	try:
		#h = httplib.HTTPConnection(uri, timeout=10)
		conn = httplib.HTTPConnection(svraddr)
		conn.request("GET", webpage)
		res = conn.getresponse() 
		print svraddr, webpage, "-->", res.status, res.reason
		return int(res.status)
	except:
		return 0

	

print "=== Current time:", time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
	
#
time_waits = get_cmd_result_as_int('netstat -na | grep "TIME_WAIT" | wc -l')
fin_waits = get_cmd_result_as_int('netstat -na | grep "FIN_" | wc -l')
syn_waits = get_cmd_result_as_int('netstat -na | grep "SYN_" | wc -l')

print (time_waits, fin_waits, syn_waits)


### main web servers
check_svr_port('lgsns7', 80)
check_svr_port('lgsns8', 80)
check_svr_port('lgsns9', 80)
check_svr_port('lgsns10', 80)

### image web servers
check_svr_port('lgsns5', 8080)
check_svr_port('lgsns6', 8080)
check_webpage('211.233.77.14:8080', '/imgSvrOK.txt')
check_webpage('211.233.77.15:8080', '/imgSvrOK.txt')

### db web servers
#check_svr_port('lgsns11', 3306)
#check_svr_port('lgsns12', 3306)
#check_svr_port('lgsns13', 3306)
#check_svr_port('lgsns14', 3306)

### server #1
check_svr_port('lgsns1', 80)
#check_svr_port('lgsns1', 25)
#check_svr_port('lgsns1', 3306)

### hadoop
check_svr_port('lgsns2', 80)
#check_svr_port('lgsns2', 3306)

## other servers
print
