#!/usr/bin/env python

name='mogs babo '*3
age = 10
def mogs():
	global age
	# empty
	print name
	age += 20
	print age
	pass


def getflds(fname):
	fd = open(fname, 'r')
	for line in fd:
		flds = line.split()

		try:
			print "%s , %s" % (flds[0], flds[2])
		except:
			#print "-"*30
			pass



if __name__ == "__main__":

	import sys


	if len(sys.argv) < 2:
		print "enter a file name"
		sys.exit(0)
	else:
		getflds(sys.argv[1])
		mogs()
