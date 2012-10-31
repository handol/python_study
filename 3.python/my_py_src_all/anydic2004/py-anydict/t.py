

A={}
A['handol']="aaa"
A['jeein']="bbb"
for k,v in A.iteritems():
	v = 50
for k,v in A.iteritems():
	print k,v


a = 20
b = 10
A={}
A['handol']=a
A['jeein']=b
for k,v in A.iteritems():
	v = 50
for k,v in A.iteritems():
	print k,v

A={}
A['handol']=[20]
A['jeein']=[10]

for k,v in A.iteritems():
	v.append( 50 )
for k,v in A.iteritems():
	print k,v

class T:
	def __init__(self, d):
		self.d = d
		d['handol'] = 10

d = {}
t = T(d)
print t.d

def	aaa(para='aaa', p2=10, p3=20.0):
	print "para=",para
	print vars()

import threading
thr = threading.Thread(target=aaa, kwargs={'para':"bbb", 'p2':100})
thr.start()


a = [[1]]
b = reduce(lambda x,y: x+y, a)
print b
print "res of reduce()", type(b)

a = ['handol', 'xx']
b = map(str, a)
print b
print type(a)

a = ['xx']
b = map(str, a)
print b
print type(a)

class AA:
	def __init__(self, age):
		self.age=age
		print "age=", self.age

map(AA, range(3))


a = [[3],[2],[1]]
b = a
print id(a),id(b)
for i in range(len(a)):
	print "a=%d b=%d" % (id(a[i]), id(b[i]))

b = a[:]
print id(a),id(b)
for i in range(len(a)):
	print "a=%d b=%d" % (id(a[i]), id(b[i]))

b = map(lambda x: (x,0), a)
print id(a),id(b)
for i in range(len(a)):
	print "a=%d b=%d" % (id(a[i]), id(b[i][0]))


a="handol"
b="rosepark"

c=[a,b]
for i in range(len(c)):
	#del c[i]  ### error
	pass
print a

a = [(1,2), (3,4)]
for x,y in a:
	print x,y


b="handol"
c="xxx"
a=[b,c]
del a 
print b, c


def f():
	return 3,4

def ff(a, b):
	print a, "--", b

#ff(f())  ## error
a,b = f()
ff(a,b)


import codecs

import random
a=[10,5,20,15,3,9,1,12]
b=[(a[i],a[i]*2)  for i in range(len(a)) if a[i]%2 == 0]
print b

