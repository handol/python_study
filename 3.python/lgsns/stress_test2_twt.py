import time
import pyodbc

def load_user_list(filename):
	try:
		fp = open(filename)
	except:
		print "cannot read file:", filename
		return []
	
	res = []
	lines = fp.readlines()
	for line in lines:
		flds = line.split()
		if len(flds) > 0:
			res.append(flds[0])
		if len(res) >= 300:
			break
		
	return res
	
def table_query_loop(cursor):
	for i in range(100):
	        query = "select userid, contentID, contentKind, content, regdate from twt_contents where openType=1 and isDel=0 and userID   = 'beautyjian' order by regDate desc limit 0, 20"
	        cursor.execute(query)
	        rows = cursor.fetchall()

def wagle_db(ipaddr, query_form, user_array):
	conn_str = 'DRIVER={MySQL};CHARSET=UTF8;SERVER=%s;PORT=3306;DATABASE=lgu;UID=lgu;PWD=lgu_pwd!' % (ipaddr)
	cnxn = pyodbc.connect(conn_str)
	cursor = cnxn.cursor()

	a = time.time()

	for user in user_array:
		query = query_form % user
	        cursor.execute(query)
	        rows = cursor.fetchall()
		for row in rows:
			pass

	b = time.time()
	
	print query_form	
	print "Start Time : " , a
	print "End Time : " ,  b
	print "During Time : " ,  b-a
	
	cursor.close()
	cnxn.close()
	

#========== main

user_array = load_user_list('twt_user_list.csv')
print len(user_array), "users loaded !"

query_form = "select userid, contentID, contentKind, content, regdate from twt_contents where openType=1 and isDel=0 and userID   = '%s' order by regDate desc limit 0, 20"

#query_form = "select * from twt_address where userID = '%s'"
wagle_db ('211.233.77.7', query_form, user_array)	
