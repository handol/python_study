
def ff(a):
	h = [1,2,4]
	h.append(a)
	print "\ta=",a, "h=", h
	print "\tid(a)=",id(a), "id(h)=", id(h)
	return h

def mystr(ss):
	ms="dahee"
	print "id(ss)=%d, id(ms)=%d, %s" %(id(ss), id(ms), ms)
	ms+=ss
	print "id(ss)=%d, id(ms)=%d, %s" %(id(ss), id(ms), ms)
	return ms

aa=10
bb=20
print "id(aa)=%d, id(bb)=%d" %(id(aa), id(bb))
print

hh = ff
print "id(ff)=%d, id(hh)=%d" %(id(ff), id(hh))
print

hh = ff(aa)
print "id(ff)=%d, id(hh)=%d" %(id(ff), id(hh))
print

print "id(hh)=%d, id(ff(bb))=%d"  %( id(hh), id(ff(bb)))
print

print "---------------"
print "id(mystr(' love'))=%d" %( id (mystr(' love')) )
