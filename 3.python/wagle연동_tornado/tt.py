
for i in range(10):
	print reduce(lambda x,y: x+y, range(i+1) )

print "-----"

sq2 = map( lambda x: x*x, range(10) )
print sq2
yy = reduce(lambda x,y: x+y, sq2)
print yy

fil = filter( lambda x: x%3==0, range(10))
print fil

twodim = [[1,2]] * 10
print twodim
xx = map( lambda x: x[1], twodim )
print xx


