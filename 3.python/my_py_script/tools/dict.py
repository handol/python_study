class Handol(dict):
	def __init__(self, initval="Stay Foolish"):
		self.val = initval

	#def add(self, v):
	#	self.val += v

	def add(self, k, v):
		self[k] = v

	def prn(self):
		print self.val
		print "-" * 50
		for k,v in self.iteritems():
			print k, v


h = Handol("Stay Hungry")
h.prn()

hh = Handol()
hh.prn()

#hh.add(" by Steve Jobs")
#hh.prn()

hh.add("valentine", 30)
hh.add("wine", 10)
hh.prn()

