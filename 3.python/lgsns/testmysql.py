import pyodbc


### {MySQL} must be defined  /etc/odbcinst.ini 
#cnxn = pyodbc.connect('DRIVER={MySQL};CHARSET=UTF8;SOCKET=/var/lib/mysql/mysql.sock;DATABASE=lgu;UID=lgu;PWD=lgu_pwd!')
#cnxn = pyodbc.connect('DRIVER={MySQL};CHARSET=UTF8;SERVER=211.233.77.10;DATABASE=lgu;UID=lgu;PWD=lgu_pwd!')
cnxn = pyodbc.connect('DRIVER={MySQL};CHARSET=UTF8;SERVER=211.233.77.10;PORT=3306;DATABASE=lgu;UID=lgu;PWD=lgu_pwd!')
cursor = cnxn.cursor()

query = 'show tables'
cursor.execute(query)
rows = cursor.fetchall()
for row in rows:
    print row


