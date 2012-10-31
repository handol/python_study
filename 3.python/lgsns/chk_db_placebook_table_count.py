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

	get_table_rowcount(cursor, "chk_PV                     ")
	get_table_rowcount(cursor, "chk_admin_user             ")
	get_table_rowcount(cursor, "chk_badge_acceptance       ")
	get_table_rowcount(cursor, "chk_badge_count            ")
	get_table_rowcount(cursor, "chk_badge_count_class      ")
	get_table_rowcount(cursor, "chk_badge_info             ")
	get_table_rowcount(cursor, "chk_checkin                ")
	get_table_rowcount(cursor, "chk_code                   ")
	get_table_rowcount(cursor, "chk_configuration          ")
	get_table_rowcount(cursor, "chk_ctgy_large_code        ")
	get_table_rowcount(cursor, "chk_ctgy_middle_code       ")
	get_table_rowcount(cursor, "chk_ctgy_small_code        ")
	get_table_rowcount(cursor, "chk_disabled_word          ")
	get_table_rowcount(cursor, "chk_favorite               ")
	get_table_rowcount(cursor, "chk_friends                ")
	get_table_rowcount(cursor, "chk_friends_agreement      ")
	get_table_rowcount(cursor, "chk_group                  ")
	get_table_rowcount(cursor, "chk_group_state            ")
	get_table_rowcount(cursor, "chk_keyword                ")
	get_table_rowcount(cursor, "chk_lifelog                ")
	get_table_rowcount(cursor, "chk_lifelog_bk             ")
	get_table_rowcount(cursor, "chk_lifelog_bk2            ")
	get_table_rowcount(cursor, "chk_lifelog_contents       ")
	get_table_rowcount(cursor, "chk_lifelog_contents_report")
	get_table_rowcount(cursor, "chk_lifelog_reply          ")
	get_table_rowcount(cursor, "chk_lifelog_reply_warning  ")
	get_table_rowcount(cursor, "chk_lifelog_report         ")
	get_table_rowcount(cursor, "chk_login                  ")
	get_table_rowcount(cursor, "chk_login_user             ")
	get_table_rowcount(cursor, "chk_medal                  ")
	get_table_rowcount(cursor, "chk_msgbox                 ")
	get_table_rowcount(cursor, "chk_notice                 ")
	get_table_rowcount(cursor, "chk_place                  ")
	get_table_rowcount(cursor, "chk_place_contents         ")
	get_table_rowcount(cursor, "chk_place_contents_report  ")
	get_table_rowcount(cursor, "chk_place_ctgy             ")
	get_table_rowcount(cursor, "chk_place_point            ")
	get_table_rowcount(cursor, "chk_place_report           ")
	get_table_rowcount(cursor, "chk_place_theme_ctgy_info  ")
	get_table_rowcount(cursor, "chk_place_total_point      ")
	get_table_rowcount(cursor, "chk_point                  ")
	get_table_rowcount(cursor, "chk_program                ")
	get_table_rowcount(cursor, "chk_sms_auth               ")
	get_table_rowcount(cursor, "chk_sns_info               ")
	get_table_rowcount(cursor, "chk_theme_ctgy_code        ")
	get_table_rowcount(cursor, "chk_user                   ")
	get_table_rowcount(cursor, "chk_user_rank              ")
	get_table_rowcount(cursor, "chk_version                ")
	get_table_rowcount(cursor, "chk_wow_medal              ")
	get_table_rowcount(cursor, "chk_wow_notice             ")
	get_table_rowcount(cursor, "chk_wow_place              ")
	get_table_rowcount(cursor, "tmp_data                   ")

	cursor.close()
	cnxn.close()


chk_wagle_db('211.233.77.8')
chk_wagle_db('211.233.77.9')
