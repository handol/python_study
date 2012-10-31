#!/usr/local/bin/python
import MySQLdb

db = MySQLdb.connect(host="localhost", user="root", passwd="ini2002", db="dahee")
db.select_db("bbs")


def do_query(query):
	db.query(query)
	res = db.use_result()
	while 1:
		row = res.fetch_row()
		if row==(): break 
		else: print str(row)

do_query("show tables")

#do_query("select subject from zetyx_board_free")


"""
c=db.cursor()
c.execute("use dahee")
c.execute("show tables")
db.query("show tables")
r=db.store_result()
r.fetch_row()
"""

