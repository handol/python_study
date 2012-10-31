import math

# http://www.q-engineering.pe.kr/table_probability.htm

# sigma*sigma == variance
# sigma == standard deviation
# mu == mean == average
# http://en.wikipedia.org/wiki/Normal_distribution
# http://en.wikipedia.org/wiki/Greek_alphabet
def normProb(mu, sigma, x):
	print "avg =", mu
	print "dev =", sigma
	print "x =", x
	p = ((x-mu)*(x-mu)) / ( 2 * sigma*sigma)
	base = 1/(sigma * math.sqrt(2*math.pi))
	res = base * math.exp(-p)
	print "res =", res, res+ (1-res)/2
	print


normProb(0.0, 1, 1)
normProb(0.0, 1, 2)
normProb(0.0, 2, 1)
normProb(0.0, 2, 2)
	
def normDist(mu, sigma, x):
	print "avg =", mu
	print "dev =", sigma
	print "x =", x
	z = (x - mu) / sigma

	p = ((x-mu)*(x-mu)) / ( 2 * sigma*sigma)
	base = 1/(sigma * math.sqrt(2*math.pi))
	res = base * math.exp(-p)
	print "res =", res, res+ (1-res)/2
	print


