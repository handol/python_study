#-*- coding:euc-kr -*-
a="한돌\n"

import   codecs

fp=open("/tmp/hhh", "a+")
fp.write(a)
fp.close()

fp=codecs.open("/tmp/hhh", encoding='euc-kr', mode='a+')
fp.write(unicode(a,"euc-kr"))
fp.close()

a=unicode(a,"euc-kr").encode("utf-8")
fp=open("/tmp/hhh", "a+")
fp.write(a)
fp.close()

fp=codecs.open("/tmp/hhh", encoding='euc-kr', mode='a+')
fp.write(unicode(a,"utf-8"))
fp.close()

a="한돌\n"
b=u"한돌\n"

print b==unicode(a,"euc-kr")

import re

ptn = re.compile("[^a-zA-Z0-9\s]")
print ptn.sub("X", "abAB \t\0\1")


a = u"aa bbbbb ccc ddd"

