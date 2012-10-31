import pyodbc


### {MySQL} must be defined  /etc/odbcinst.ini 


def get_table_rowcount(cursor, tablename):
	query = "select count(*) from %s" % (tablename)
	cursor.execute(query)
	rows = cursor.fetchall()
	for row in rows:
	    print row[0]
	    pass

def chk_wagle_db(ipaddr):
	print "== DB:", ipaddr
	conn_str = 'DRIVER={MySQL};CHARSET=UTF8;SERVER=%s;PORT=3306;DATABASE=lgu;UID=lgu;PWD=lgu_pwd!' % (ipaddr)
	cnxn = pyodbc.connect(conn_str)
	cursor = cnxn.cursor()
	get_table_rowcount(cursor, "chk_user")
#	get_table_rowcount(cursor, "twt_follower_list")
#	get_table_rowcount(cursor, "twt_contents")
#	get_table_rowcount(cursor, "twt_timeline")

	cursor.close()
	cnxn.close()


chk_wagle_db('211.233.77.8')
chk_wagle_db('211.233.77.9')
