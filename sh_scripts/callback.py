

def do_call(func):
	print "in do_call(): ", id(func)
	if func: 
		func
		func('cccccc')
	None


def aa(a):
	a += ' hoho'
	print a
def bb(a):
	a += ' hoho'
	print a


print "in __main__: ", id(aa)
do_call(aa)
do_call(aa('he'))
do_call(bb('bebe'))
do_call(None)

print aa
print bb
None
