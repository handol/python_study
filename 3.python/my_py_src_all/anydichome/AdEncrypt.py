import pyDes
import base64
import binascii

MY_KEY = "anydic08"  # must be 8-character long
class AdEncrypt:
	def __init__(self):
		self.k = pyDes.des(MY_KEY, pyDes.CBC, "\0\0\0\0\0\0\0\0")
	def	encode(self, trgstr):
		trgstr = AdEncrypt._make8long(trgstr)
		c1 = self.k.encrypt(trgstr)
		c2 = base64.b64encode(c1)
		c2 = binascii.hexlify(c1)
		return c2
		
	def	decode(self, trgstr):
		d1 = base64.b64decode(trgstr)
		d1 = binascii.unhexlify(trgstr)
		d2 = self.k.decrypt(d1)
		return d2.rstrip()

	# convert into a 8-byte long string
	@staticmethod
	def _make8long(trgstr):
		mod = len(trgstr) % 8
		if mod > 0:
			return trgstr + ' '*(8-mod) 
		else:
			return trgstr


if __name__=="__main__":
	import sys

	cr = AdEncrypt()
	c = cr.encode(sys.argv[1])
	print c
	d = cr.decode(c)
	print d
