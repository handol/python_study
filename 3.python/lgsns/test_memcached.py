
import memcache
s = memcache.Client(["127.0.0.1:11211"])
#for i in range(10):
#	s.set("name", "david")

mylist = ["aaa", "bbb", "ccc"]

for i in mylist:
	if s.get(i)==None:
		s.set(i, "aaaa")
		print "Set", i
for i in mylist:
	print "Get", s.get(i)

