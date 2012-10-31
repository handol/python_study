import time

import b
class a:
	def __init__(self, s):
		self.data = s
		print s

	def do(self):
		n = 0
		while 1:
			print n
			b.prn(self)
			time.sleep(1)
			n += 1
			if n % 3 == 0:
				reload(b)


aa = a('hi ')
aa.do()
