#!/usr/bin/python
# -*- coding: EUC-KR -*-
# anydic2004 mysql database를 load하는 모듈.
# 2008/3/10

import MySQLdb


"""
create view goodHosts as select host_id, count(*) as numDocs from docs where no_sentenc >= 10  group by host_id ;
select  count(*),  sum(numDocs )  from  goodHosts ;

==> 2957, 36821


select  goodHosts .*, hosts.hostname  from  goodHosts , hosts where  goodHosts .host_id = hosts.host_id  and numDocs >= 20;
==>  208 |         17942 | ===  20문서 이상

select count(*) from docs INNER JOIN goodHosts on   docs.host_id = goodHosts.host_id where no_sentenc >=10 and goodHosts.numDocs >= 20;
==> 17942

"""

class AdDb:
	def __init__(self, host, user, passwd, db, debug=0):
		self.host = host
		self.user = user
		self.passwd = passwd
		self.db = db

		self.conn = MySQLdb.connect (host, user, passwd, db)
		self.cursor = self.conn.cursor() # cursor is reusable during the connection.
		self.lastseqnum = 0

	def __del__(self):
		self.conn.close()


	def test(self):
		cursor = self.conn.cursor()  # get a new cursor from the conn.
		cursor.execute ("SELECT VERSION()")
		row = cursor.fetchone ()
		print "server version:", row[0]
		cursor.close ()

	def	prnRow(self, rows):
		#print "====== %d rows ====" % (int(cursor.rowcount))
		print "====== %d rows ====" % (len(rows))

		# iterate through resultset
		for row in rows:
			for x in row:
				print type(x)
				print x

	## load Hosts table
	def loadGoodHosts(self, hostTab, minDocs=20, debug=0):
		sql = "SELECT goodHosts.*, hosts.hostname from goodHosts , hosts where goodHosts .host_id = hosts.host_id  and numDocs >= %d" % (minDocs)
		
		if debug: print sql
		cursor = self.conn.cursor ()
		cursor.execute(sql)
		rows = cursor.fetchall ()
		for r in rows:
			hostTab.add(r[0], r[1], r[2])
		cursor.close ()

	## load Hosts table
	def loadGoodDocs(self, docTab, minStcs=10, minDocs=20, debug=0):
		where = "WHERE no_sentenc >= %d AND length(title) > 1 AND goodHosts.numDocs >= %d" % (minStcs, minDocs)
		sql = "SELECT doc_id, docs.host_id, url_path, title, file_path, doc_level, no_sentenc from docs INNER JOIN goodHosts ON docs.host_id = goodHosts.host_id "
		sql += where
		if debug: print sql
		
		cursor = self.conn.cursor ()
		cursor.execute(sql)
		rows = cursor.fetchall ()
		for r in rows:
			docTab.add(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
		cursor.close ()

	## load Word List table
	def	loadWordList(self, wordListTab):
		"""
		There many misspelled words in table "word_list"
		Only up to word_id 89003 ('Zyrian') are good words.
		"""
		sql = "SELECT word, word_id, org_word FROM word_list WHERE word_id <= 89003"
		cursor = self.conn.cursor ()
		cursor.execute(sql)
		rows = cursor.fetchall ()
		for r in rows:
			wordListTab.add(r[0], r[1], r[2])
		cursor.close ()

	## load Idiom List table
	def	loadIdiomList(self, idiomListTab):
		"""
		'Zygophyllum fabago'  is the last good idiom ==> 63506
		"""
		sql = "SELECT idiom, idiom_id FROM idiom_list WHERE idiom_id <= 63506"
		cursor = self.conn.cursor ()
		cursor.execute(sql)
		rows = cursor.fetchall ()
		for r in rows:
			idiomListTab.add(r[0], r[1])
		cursor.close ()


	## load Word Examples table
	def	loadWordEx(self, wordExTab, alphabet):
		sql = "SELECT w_id, doc_id, s_pos, s_len, pos1, len1, level FROM wExam_%c" % (alphabet)
		cursor = self.conn.cursor ()
		cursor.execute(sql)
		rows = cursor.fetchall ()
		for r in rows:
			wordExTab.add(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
		cursor.close ()

	## load Idiom Examples table
	def	loadIdiomEx(self, idiomExTab, alphabet):
		sql = "SELECT i_id, doc_id, s_pos, s_len, pos1, len1, level FROM iExam_%c" % (alphabet)
		cursor = self.conn.cursor ()
		cursor.execute(sql)
		rows = cursor.fetchall ()
		for r in rows:
			idiomExTab.add(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
		cursor.close ()


		


## for Easy Connection
def login():
	db = AdDb("localhost", "BeOnE", "FromRemoteBeOnE", "ad2004")
	return db

if __name__ == "__main__":
	db = AdDb("localhost", "BeOnE", "FromRemoteBeOnE", "ad2004")
	db.test()


