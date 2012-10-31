
def test_split(str, delimit):
	flds = str.split(delimit)
	print str, "--->", len(flds)
	
	flds2 = filter(lambda x: len(x), flds)
	flds2 = filter(len, flds)
	for i in range(len(flds)):
		print "[%d] %s" % (i, flds[i])
	for i in range(len(flds2)):
		print "[%d] %s" % (i, flds2[i])
		
	
def getNumber(str):
	m = re.match("\D+(\d+)\D+", str)
	if m:
		#print m.group(1)
		return int(m.group(1))
	else: 
		return 0
#print getNumber("fdaf10fds")
#print getNumber("200")
	

def get_table_rowcount(cursor, tablename):
	query = "select count(*) from %s" % (tablename)
	cursor.execute(query)
	rows = cursor.fetchall()
	try:
		return int(row[0])
	except:
		return 0
