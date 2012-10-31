import pyodbc


### {MySQL} must be defined  /etc/odbcinst.ini 


def get_table_rowcount(cursor, tablename):
	query = "select count(*) from %s" % (tablename)
	cursor.execute(query)
	rows = cursor.fetchall()
	for row in rows:	
	    print tablename , ":",row[0]
	    pass

def chk_wagle_db(ipaddr):
	print "== DB:", ipaddr
	conn_str = 'DRIVER={MySQL};CHARSET=UTF8;SERVER=%s;PORT=3306;DATABASE=lgu;UID=lgu;PWD=lgu_pwd!' % (ipaddr)
	cnxn = pyodbc.connect(conn_str)
	cursor = cnxn.cursor()

	get_table_rowcount(cursor, "twt_PV                 ")
	get_table_rowcount(cursor, "twt_address            ")
	get_table_rowcount(cursor, "twt_address_count      ")
	get_table_rowcount(cursor, "twt_admin_user         ")
	get_table_rowcount(cursor, "twt_alert_info         ")
	get_table_rowcount(cursor, "twt_connecting_state   ")
	get_table_rowcount(cursor, "twt_contents           ")
	get_table_rowcount(cursor, "twt_contents_open_group")
	get_table_rowcount(cursor, "twt_creation_group     ")
	get_table_rowcount(cursor, "twt_favorite           ")
	get_table_rowcount(cursor, "twt_follower_list      ")
	get_table_rowcount(cursor, "twt_following_list     ")
	get_table_rowcount(cursor, "twt_group_member       ")
	get_table_rowcount(cursor, "twt_lbs_contents       ")
	get_table_rowcount(cursor, "twt_login              ")
	get_table_rowcount(cursor, "twt_login_user         ")
	get_table_rowcount(cursor, "twt_memtioninfo        ")
	get_table_rowcount(cursor, "twt_msgcontents        ")
	get_table_rowcount(cursor, "twt_msgroom            ")
	get_table_rowcount(cursor, "twt_qna                ")
	get_table_rowcount(cursor, "twt_rt                 ")
	get_table_rowcount(cursor, "twt_sms_auth           ")
	get_table_rowcount(cursor, "twt_stat_address_count ")
	get_table_rowcount(cursor, "twt_stat_creation_group")
	get_table_rowcount(cursor, "twt_taginfo            ")
	get_table_rowcount(cursor, "twt_timeline           ")
	get_table_rowcount(cursor, "twt_traffic            ")
	get_table_rowcount(cursor, "twt_user               ")
	get_table_rowcount(cursor, "twt_userngroup         ")
	get_table_rowcount(cursor, "twt_usernroom          ")

	cursor.close()
	cnxn.close()


chk_wagle_db('211.233.77.6')
chk_wagle_db('211.233.77.7')
