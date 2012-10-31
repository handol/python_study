
import MySQLdb


def	checkDbVersion(dbconn):
	cursor = dbconn.cursor ()
	cursor.execute ("SELECT VERSION()")
	row = cursor.fetchone ()
	print "server version:", row[0]
	cursor.close ()


#!/usr/bin/python

def	loadTable(host, user, passwd, db, debug=0):

	conn = MySQLdb.connect (host, user, passwd, db)

	cursor = conn.cursor ()
	cursor.execute ("SELECT id, en01, en02, en03, en04, en05 from usr")
	rows = cursor.fetchall ()

	if debug: print "====== %d rows ====" % (int(cursor.rowcount))

	# iterate through resultset
	D = {}
	for row in rows:
		id = row[0]
		vectors = []
		for x in row[1:]:
			#print x
			#print type(x)
			xx = x.split()
			xx = map(int, xx)
			vectors.append(xx)
			#print xx
			#print type(xx)
		D[id] = vectors

	cursor.close ()
	conn.close ()
	return D



if __name__ == "__main__":

	resD = loadTable('localhost', 'root', 'wpxk00', 'rhythmpass_web')
	handol = resD['handol']
	for v in handol:
		print v
