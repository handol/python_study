import pyodbc


### {MySQL} must be defined  /etc/odbcinst.ini 
cnxn = pyodbc.connect('DRIVER={MySQL};CHARSET=UTF8;SERVER=211.233.77.7;PORT=3306;DATABASE=lgu;UID=lgu;PWD=lgu_pwd!')
#print cnxn.getinfo(SQL_SERVER_NAME)
cursor = cnxn.cursor()

query = 'show tables'
cursor.execute(query)
rows = cursor.fetchall()
for row in rows:
    #print row
    pass
cursor.close()



cursor = cnxn.cursor()
	#where userID=%s and timelineID 

twt_query = """ select timelineID, userID, contentID, contentKind, regDate, rtUserID
	from twt_timeline
	where userID='%s'
	order by timelineID desc
	limit 1, 10 """ % ('qwerty1')

print twt_query

cursor.execute(twt_query)
rows = cursor.fetchall()
print "total = ", len(rows)
for row in rows:
    print row
    pass

cursor.close()
cnxn.close()
