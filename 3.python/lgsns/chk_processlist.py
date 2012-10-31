import pyodbc

### {MySQL} must be defined  /etc/odbcinst.ini

def show_processlist(cursor):
        query = "show  processlist"
        cursor.execute(query)
        rows = cursor.fetchall()  

        rowcount = cursor.rowcount

        print "process count :  " , rowcount

def chk_wagle_db(ipaddr):
        print "== DB:", ipaddr
        conn_str = 'DRIVER={MySQL};CHARSET=UTF8;SERVER=%s;PORT=3306;DATABASE=lgu;UID=lgu;PWD=lgu_pwd!' % (ipaddr)
        cnxn = pyodbc.connect(conn_str)
        cursor = cnxn.cursor()
        show_processlist(cursor)
        cursor.close()
        cnxn.close()

###wagle###
chk_wagle_db('211.233.77.6')
chk_wagle_db('211.233.77.7')

###placebook###
chk_wagle_db('211.233.77.8')
chk_wagle_db('211.233.77.9')

chk_wagle_db('211.233.77.10')
