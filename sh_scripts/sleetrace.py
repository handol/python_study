#!/usr/bin/env python
import os
import sys

def get_secvalue(line):
	'''
	TRACE [14:56:53] PC=   0 CID=( 1, 0,12: 0) FROM
	line == "[14:56:53]"
	'''

	hour = int(line[1:3])
	min = int(line[4:6])
	sec = int(line[7:9])
	#print "H:M:S", hour, min, sec
	val = hour*3600 + min*60 + sec
	return val

def proc_map_mesg(f, l, n):
	recv_send=0
	if l.startswith('SEND'):
		recv_send = 2
	elif l.startswith('RECV'):
		recv_send = 1
	else:
		return f, l, n, ''

	pos = l.find('TCAP')
	if pos>=0: 
		compType = l[pos+6:-1]
	else:
		compType = ''
	if l.find('INVOKE') >= 0:
		map_type=0
	elif l.find('RESULT') >= 0:
		map_type=0

	elif l.find('ERROR') >= 0:
		map_type=1
	elif l.find('ANCEL') >= 0:
		map_type=3
	elif l.find('END') >= 0:
		map_type=2
	else:
		map_type=0

	op=0
	opname=''
	while 1:
		l = f.readline()
		n += 1
		if l=='': break
		if l.startswith('TRACE'): break

		if map_type==1:
			pos = l.find('cause')
			if pos >= 0:
				pos2 = l.find('=')
				#op = int(l[pos2+2:pos2+4])
				op = 0
				pos2 = l.find('(')
				pos3 = l.find(')')
				opname = 'Error ' + l[pos2+1:pos3]
			else: continue
		elif map_type==2:
			op = 0
			opname = 'End'

		elif map_type==3:
			op = -1
			opname = 'Cancel'

		else:
			pos = l.find('operation =')
			if pos >= 0:
				pos2 = l.find('=')
				op = int(l[pos2+2:pos2+4])
				pos2 = l.find('(')
				pos3 = l.find(')')
				opname = l[pos2+1:pos3]
			else: continue
	
	#print "OP", op, opname
	if recv_send==1:
		res = "R %3d %-40s" % (op, opname+'  '+ compType)
	else:
		res = "S %3d %-40s" % (op, opname+'  '+ compType)

	return f, l, n, res


def proc_traceline(l):
	tstr=''
	tval=0
	pos = l.find("[")
	if pos >= 0: 
		tstr = l[pos+1:pos+9]
		tval = get_secvalue(l[pos:])

	fromstr = ''
	pos = l.find("FROM=")
	if pos >= 0 and not l[pos+5].isalpha(): 
		pos2 = l[pos+5:].find(' ')
		fromstr = l[pos+5:pos+5+pos2]

	to = ''
	pos = l.find("TO=")
	if pos >= 0 and not l[pos+3].isalpha(): 
		pos2 = l[pos+3:].find(' ')
		to = l[pos+3:pos+3+pos2]
	
	return tstr, tval, fromstr, to


def read_trace(fname, rmi=0):
	try:
		f = open(fname, "r")
	except:
		print "read error : ", fname
		return

	prevln = ''
	p_n = 0
	res=''

	n = 0
	l = ''
	p_tval = 0
	print '# %-4s %-8s  %-38s %s -- %s' % ('Line', 'Time', 'R/S  OpCode OpName', 'FROM', 'TO')
	while 1:
		l = f.readline()
		if l=='': break
		n += 1

		if l.startswith("TRACE"):
			p_n = n
			prevln = l
		else:
			f, l, n, res = proc_map_mesg(f, l, n)
			if res=='': continue
			tstr, tval, fromstr, to = proc_traceline(prevln)
			if tval - p_tval > 15:
				p_tval = tval
				print

			print '%-5d  %s  %s %s -- %s' % (p_n, tstr, res, fromstr, to)



if len(sys.argv) < 2:
	print "%s trace_filename " % (sys.argv[0])
	#print "ex) %s ~/hlrhome/log/.cmdhistory/12/cmd.20031215 " % (sys.argv[0])
	sys.exit(0)

if len(sys.argv) > 2:
	read_trace(sys.argv[1], 1)
else:
	read_trace(sys.argv[1], 0)
