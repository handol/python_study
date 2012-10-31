import hashlib
passwd='handol'
sha = hashlib.sha1()
sha.update(passwd)
passwdenc = sha.hexdigest()
print passwd
print passwdenc

#import codecs
#inf = codecs.open("handola.tweets.2011-08-22", "r", "utf-8")
#for line in inf.xreadlines():
#	if line.find("Birzzle") != -1:
#		print line
