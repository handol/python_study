import time
import pyodbc

def table_query(cursor):
	for i in range(100):
	        query = "select userid, contentID, contentKind, content, regdate from twt_contents where openType=1 and isDel=0 and userID   = 'beautyjian' order by regDate desc limit 0, 20"
	        cursor.execute(query)
	        rows = cursor.fetchall()

def wagle_db(ipaddr):
	a = time.time()
	conn_str = 'DRIVER={MySQL};CHARSET=UTF8;SERVER=%s;PORT=3306;DATABASE=lgu;UID=lgu;PWD=lgu_pwd!' % (ipaddr)
	cnxn = pyodbc.connect(conn_str)
	cursor = cnxn.cursor()

	table_query(cursor)

	b = time.time()
	
	print "Query	: select userid, contentID, contentKind, content, regdate from twt_contents where openType=1 and isDel=0 and userID   = 'beautyjian' order by regDate desc limit 0, 20"
	
	print "Start Time : " , a
	print "End Time : " ,  b
	print "During Time : " ,  b-a
	
	cursor.close()
	cnxn.close()
	
wagle_db ('211.233.77.7')	
