import pyodbc
import os
import sys
import time


### {MySQL} must be defined  /etc/odbcinst.ini 



def mk_comma_numstr(numstr):
	n = len(numstr)
	cnt = 3
	resstr = ""
	for i in range(len(numstr)):
		j = len(numstr) - i
		if (j % 3) == 0 and j != len(numstr):
			resstr += ','
		resstr += numstr[i]
	return resstr

				
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

def save_to_file(fname, html_form_file):
	
	form_f = open(html_form_file)
	htmltemplate = form_f.read()
	form_f.close()

	fp = open(fname, "w")
	cnt_res = chk_wagle_db('211.233.77.7')
	cnt_res2 = chk_placebook_db('211.233.77.9')

	#html = htmltemplate % (cnt_res[0], cnt_res[1], cnt_res2[0], cnt_res2[1])
	numstr1 = mk_comma_numstr( str(cnt_res[0]))
	numstr11 = mk_comma_numstr( str(cnt_res[1]))
	numstr2 = mk_comma_numstr( str(cnt_res2[0]))
	numstr22 = mk_comma_numstr( str(cnt_res2[1]))

	html = htmltemplate % (numstr1, numstr11, numstr2, numstr22)
	fp.write(html)
	fp.close
	print "Done ===>", fname


#print mk_comma_numstr("123")
#print mk_comma_numstr("1234")
#print mk_comma_numstr("123456")
#print mk_comma_numstr("1234567")

if __name__=="__main__":
	if len(sys.argv)==1:
		save_to_file("snscnt.html", "sns_counter_form.html")
	else:
		while 1:
			save_to_file("snscnt.html", "sns_counter_form.html")
			time.sleep(int(sys.argv[1]))
			
