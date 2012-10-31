#!/usr/bin/python

import MySQLdb

class KsdDb:
	def __init__(self, host, user, passwd, db, debug=0):
		self.host = host
		self.user = user
		self.passwd = passwd
		self.db = db

		self.conn = MySQLdb.connect (host, user, passwd, db)
		self.cursor = self.conn.cursor() # cursor is reusable during the connection.

	def __del__(self):
		self.conn.close()

	def close(self):
		self.conn.close()

	def test(self):
		cursor = self.conn.cursor ()
		cursor.execute ("SELECT VERSION()")
		row = cursor.fetchone ()
		print "server version:", row[0]
		cursor.close ()

	## load 'ksdlog' table
	def load(self, datamodel, WHERE=None):
		cursor = self.conn.cursor ()
		sql = "SELECT uid, seqnum, ipaddr, logtime, ksdvec, ksdvalue, alertvalue from ksdlog"
		if WHERE != None:
			sql = "%s WHERE %s" % (sql, WHERE)

		cursor.execute(sql)
		rows = cursor.fetchall()
		cursor.close ()

		for r in rows:
			datamodel.add(tuple(r))
		return len(rows)


	## check if ksdvalue of 'uid' table is zero
	def getCenter(self, uid):
		cursor = self.conn.cursor ()
		sql = "SELECT ksdcenter, ksdvalue FROM uid where uid=%d" % (uid)
		cursor.execute(sql)
		val = cursor.fetchone ()
		if int(cursor.rowcount) == 0:
			return [], 0.0
		cursor.close()

		try:
			center = map(float, val[0].split())
			radius = float(val[1])
		except:
			return [], 0.0
			
		return center, radius
	

	## update 'ksdlog' table
	def updateScore(self, uid, seqnum, ksdvalue, alertvalue, debug=0):
		cursor = self.conn.cursor ()
		sql = "UPDATE ksdlog SET ksdvalue=%.1f, alertvalue=%.1f WHERE uid=%d and seqnum=%d" % (ksdvalue, alertvalue, uid, seqnum)
		if debug: print sql
		cursor.execute(sql)

	## update 'uid' table
	def updateSharing(self, uid, sharing, debug=0):
		cursor = self.conn.cursor ()
		sql = "UPDATE uid SET sharing=%d where uid=%d" % (sharing, uid)
		if debug: print sql
		cursor.execute(sql)
		cursor.close()

	## update 'uid' table
	def updateConsistency(self, uid, consistency, debug=0):
		cursor = self.conn.cursor ()
		sql = "UPDATE uid SET consistency=%d where uid=%d" % (consistency, uid)
		if debug: print sql
		cursor.execute(sql)
		cursor.close()

	## update 'uid' table
	def updateCenter(self, uid, center, radius, debug=0):
		kc = ' '.join(map(lambda x: "%.1f" % x, center))
		cursor = self.conn.cursor ()
		sql = "UPDATE uid SET ksdcenter='%s', ksdvalue=%.1f WHERE uid=%d" % (kc, radius, uid)
		if debug: print sql
		cursor.execute(sql)
		cursor.close()

	## INSERT uid
	def insertUid(self, id, dim, debug=0):
		cursor = self.conn.cursor ()
		sql = "INSERT uid (uid, id, ksdvecdim) VALUES (0, '%s', %d)" % (id, dim)
		if debug: print sql
		cursor.execute(sql)
		cursor.close()

	##  get uid from id
	# input "mobile_xxx", output: uid=123
	def	getUid(self, id):
		cursor = self.conn.cursor ()
		sql = "SELECT uid from uid WHERE id='%s'" % (id)
		cursor.execute(sql)
		val = cursor.fetchone ()
		if int(cursor.rowcount) == 0:
			return 0
		cursor.close()
		return val[0]
	

	## INSERT ksdlog
	def insertKsdlog(self, uid, ipaddr, logtime, ksdvec, debug=0):
		cursor = self.conn.cursor ()
		sql = "INSERT ksdlog (uid, seqnum, ipaddr, logtime, ksdvec) VALUES \
				(%d, 0, '%s', NOW() - INTERVAL %d MINUTE, '%s')" % \
			 (uid, ipaddr, logtime, ksdvec)
		if debug: print sql
		cursor.execute(sql)
		cursor.close()
	
		


## for Easy Connection
def login():
	db = KsdDb("localhost", "BeOnE", "FromRemoteBeOnE", "chamdemo")
	return db
	

if __name__ == "__main__":
	db = KsdDb("localhost", "BeOnE", "FromRemoteBeOnE", "chamdemo")
	db.test()

	db.load(6)
	print db.isModelMade(6)
	center, csize = db.getCenter(5)
	print "=== center", center, csize
