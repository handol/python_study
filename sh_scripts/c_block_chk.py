#!/usr/bin/env python
import os
import sys

BLOCK = 0
PARA = 0

def check_line(line, lineno):
	global BLOCK, PARA

	for c in line:
		if c=='{': 
			BLOCK += 1
			if PARA != 0:
				print "line %s: (, ) NOT match" % lineno
		elif c=='}':
			BLOCK -= 1
			if BLOCK < 0:
				print "line %s: {,} NOT match : BLOCK=%d" % (lineno, BLOCK)
			if PARA != 0:
				print "line %s: (, ) NOT match" % lineno

		elif c=='(':
			PARA += 1
		elif c==')':
			PARA -= 1
			if PARA < 0:
				print "line %s: (,) NOT match : PARA=%d" % (lineno, PARA)

def skip_comment(fd, line, lineno):
	pos = line.find("/*")
	if pos < 0: 
		pos = line.find("//")
		if pos < 0: 
			cmnt = 0
			check_line(line, lineno)
			return fd, line, lineno
		else:
			cmnt = 1
			check_line(line[:pos], lineno)
			return fd, line, lineno
	else:
		cmnt = 2
		check_line(line[:pos], lineno)

	while 1:
		pos = line.find("*/")
		if pos >= 0:
			check_line(line[pos+2:], lineno)
			return fd, line[pos+2:], lineno

		line = fd.readline()
		if line==None or line=='': 
			return fd, line, lineno
		lineno += 1





def	check_block(fname, linenum=0):
	try:
		fd = open(fname, 'r')
	except:
		return -1

	n = 0
	currBlock = -1
	while 1:
		line = fd.readline()
		if line==None or line=='': 
			break
		n += 1
		fd, line, n = skip_comment(fd, line, n)

		if linenum!=0:
			if n<linenum: 
				continue
			elif n==linenum:
				currBlock = BLOCK-1
			elif currBlock==BLOCK:
				print "line %d: found match" % n
				linenum=0


	fd.close()


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "%s file [linenum]" % (sys.argv[0])
		sys.exit(0)

	if len(sys.argv) == 3:
		check_block(sys.argv[1], int(sys.argv[2]))
	else:
		check_block(sys.argv[1])

