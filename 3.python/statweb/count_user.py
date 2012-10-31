import pyodbc
import os
import sys


### {MySQL} must be defined  /etc/odbcinst.ini 


def get_table_rowcount(cursor, tablename):
	query = "select count(*) from %s" % (tablename)
	cursor.execute(query)
	rows = cursor.fetchall()
	cnt = 0
	for row in rows:
	    print row[0]
	    cnt = int(row[0]) 
	    pass
	return cnt

## return list of munbers
def chk_wagle_db(ipaddr):
	print "== DB:", ipaddr
	conn_str = 'DRIVER={MySQL};CHARSET=UTF8;SERVER=%s;PORT=3306;DATABASE=lgu;UID=lgu;PWD=lgu_pwd!' % (ipaddr)
	cnxn = pyodbc.connect(conn_str)
	cursor = cnxn.cursor()
	c_users = get_table_rowcount(cursor, "twt_user")
	#c_followers = get_table_rowcount(cursor, "twt_follower_list")
	c_contents = get_table_rowcount(cursor, "twt_contents")
	c_l_contents = get_table_rowcount(cursor, "twt_lbs_contents")

	cursor.close()
	cnxn.close()
	return c_users, c_contents + c_l_contents

## return list of munbers
def chk_placebook_db(ipaddr):
	print "== DB:", ipaddr
	conn_str = 'DRIVER={MySQL};CHARSET=UTF8;SERVER=%s;PORT=3306;DATABASE=lgu;UID=lgu;PWD=lgu_pwd!' % (ipaddr)
	cnxn = pyodbc.connect(conn_str)
	cursor = cnxn.cursor()
	c_users = get_table_rowcount(cursor, "chk_user")
	c_checkin = get_table_rowcount(cursor, "chk_checkin")

	cursor.close()
	cnxn.close()
	return c_users, c_checkin

htmltemplate = """<html>
<head>
<meta http-equiv="refresh" content="5">
<title>LG SNS Counter</title> 
</head>

<body> 
<div align=center> 
<ul>
<li> <h1>Wagle Users: %s </h1> 
<li> <h1>Wagle Tweets: %s </h1> 
</ul>
<ul>
<li> <h1>Place Users: %s </h1> 
<li> <h1>Place Checkins: %s </h1> 
</ul>
</div>
</body>

</html>
"""

## 211.233.77.6 = wagle 1st db
## 211.233.77.7 = wagle 2nd db

def save_to_file(fname):
	fp = open(fname, "w")
	cnt_res = chk_wagle_db('211.233.77.7')
	cnt_res2 = chk_placebook_db('211.233.77.9')
	html = htmltemplate % (cnt_res[0], cnt_res[1], cnt_res2[0], cnt_res2[1])
	fp.write(html)
	fp.close
	print "Done"

save_to_file("waglecnt.html")
