#!/usr/local/bin/python

def main(a):
	print "hello"
	print a
	a.append('cc')
	print a
	return a[0]


#if __name__=="__main__":

a=[]
a.append('aa')
a.append('bb')
b = main(a)
print a
b = 'BB'
print a

#f = open('ttt', 'w')
#print f 'aaa'
#f.write('aaa');
#f.write('aaa');
