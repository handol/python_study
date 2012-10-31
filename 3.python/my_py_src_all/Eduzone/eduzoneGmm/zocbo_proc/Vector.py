#!/usr/bin/env python
########################################################
# 2008.3.12  handol@gmail.com
# 
# For vector implementation in python , 
# refer to http://www.math.okstate.edu/~ullrich/PyPlug/
########################################################

import math

class Vector:
	def __init__(self, vals):
		if isinstance(vals, Vector):
			self.vals = vals.vals[:]
		elif type(vals) == list:
			self.vals = map(float, vals)
		elif type(vals) == int:
			self.vals = [0.0] * vals
		elif type(vals) == float:
			self.vals = [vals]
		elif type(vals) == str:
			if vals.find(',') != -1:
				delimiter = ','
			else:	
				delimiter = None 
			self.vals = map(float, vals.split(delimiter))	
		else:
			print type(vals), vals
			raise "Unknown type in constructor"
		#print "Vector __init__():", id(self.vals), id(vals)
		#print "Vector __init__():", self.vals, vals
	
	def prn(self, msg='', format="%.1f "):
		print msg, ''.join(map(lambda x: format % x, self.vals))

	def str(self, msg='', format="%.1f "):
		return msg + ''.join(map(lambda x: format % x, self.vals))

	def dim(self):
		return len(self.vals)
	
	def __len__(self):
		return len(self.vals)

	def __getitem__(self, idx):
		return self.vals[idx]
	
	## simple vector add
	def __add__(v1, v2):
		v3 = map(lambda x, y: x+y, v1.vals, v2.vals)
		return Vector(v3)

	## vector add  +=
	#def __iadd__(self, v2):
	#	self.vals = map(lambda x, y: x+y, self.vals, v2.vals)
	#	return self 

	## simple vector sub
	def __sub__(v1, v2):
		v3 = map(lambda x, y: x-y, v1.vals, v2.vals)
		#print "vector Sub:", v3
		return Vector(v3)

	## vector sub  -=
	def __isub(self, v2):
		self.vals = map(lambda x, y: x-y, self.vals, v2.vals)
		return self 
		
	## 	 vector * float
	def __mul__(v1, v2):
		if type(v1) != Vector and type(v2)==Vector:
			tmp = v1
			v1 = v2
			v2 = tmp
		v3 = map(lambda x: x*v2, v1.vals)
		#print "vector Sub:", v3
		return Vector(v3)
	
	## 	 vector / float
	def __div__(v1, f):		
		v3 = map(lambda x: x/f, v1.vals)
		#print "vector Sub:", v3
		return Vector(v3)

	## 	 vector / float
	def __idiv__(self, f):		
		self.vals = map(lambda x: x/f, self.vals)
		return self

	## max
	def upper(self, v2):
		self.vals = map(max, self.vals, v2.vals)
		return self
		
	## min
	def lower(self, v2):
		self.vals = map(min, self.vals, v2.vals)
		return self
		
	## the size of Vector == Euclidean Norm (distance)
	def size(self):
		res = sum( map(lambda x: x*x, self.vals) )
		#print a, res
		return math.sqrt(res)

	## get the KSD distance of a given vector
	def ksdsize(self):
		res = sum( map(lambda x: x*x, self.vals) )
		#print a, res
		return math.sqrt(res/len(self.vals))

	## get the normalization of this vector. return a new Vector.
	def getNormVector(self):
		norm = self.size()
		return self / norm


if __name__ == "__main__":
	tarr = [
	Vector("110, 0, 93, -15, 125, 31, 94, -32, 94, -15, 93"),
	Vector("109, -15, 109, -15, 78, 47, 78, -16, 109, -46, 93"),
	Vector("109, -16, 79, 15, 94, 47, 78, -31, 109, -31, 94"),
	Vector("94, 16, 109, -63, 110, 47, 78, -47, 94, 0, 78"),
	Vector("110, 31, 109, -15, 109, 31, 78, -15, 109, -31, 109")
	]

	v = Vector([10, 20, 20, -10, 30])
	t = Vector([1, 2, 3, 4, 3])
	t2 = Vector([2, 3, 5, 5, 5])
	t3 = Vector([3, 3, 4, 5, 1])
	t4 = Vector([3, 4, 4, 6, 3])
	t5 = Vector("110, 0, 93, -15, 125, 31, 94, -32, 94, -15, 93")
	
	t5.prn()
	
	v.prn("v: ")
	a = t + t2	
	a.prn("a: ")
	b = a*2
	b.prn("b: ")
	print b.size(), b.ksdsize()
	b += a
	b.prn("b: ")
	b /= 2
	b.prn("b: ")
	c = b.getNormVector()
	c.prn("c: ")
	

	

