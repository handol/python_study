#f = open('twt_user_list')
f = open('addr_user_list')
lines = f.readlines()

for line in lines:
	flds = line.split()
	if len(flds)==5:
		print "%s\t%s" % (flds[1],flds[3])
