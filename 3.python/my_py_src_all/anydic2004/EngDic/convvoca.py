### 
#-*- #oding: euc-kr -*-

import sys
import os

NONE=0
HWORD=1
KDEF=2
EDEF=3
EX=4
alpha_A=ord('A')
alpha_z=ord('z')

def find_alpha(str):
	p = 0
	for s in str:
		if alpha_A <= ord(s) <= alpha_z and s.isalpha():
			#print s, ord(s)
			return p
		p += 1
	return -1

def handle_one_block(buff):
	status = KDEF		
	kordef = 1
	engdef = None
	example = None

	num_lines = len(buff)

	line = buff[0]	
	i = 0
	if line[0].isalpha():  ## Enlish
		words = line.split()
		flds =len(words)

		if flds>=1: 
			status = HWORD #  head word
			print
			print line
			i = 1	
	else:
		print "##error in line %d"%n, "English expected"
		print "#", line
		
			
	line = buff[i]
	if line.startswith("우리"):
		i += 1
		pos = line.find(':')
		if pos<0: 
			print "##error in line %d"%n, "NOT found :"
			print "#", line
			return 0
		try:
			if line[pos+1]==' ': pos += 2
			else: pos += 1
		except:
			kordef = 0
			#print "##error in line %d"%n, "Empty KDEF"
			#print "#", line
			#return 0

		pos2 = find_alpha(line[pos:])
		#print "pos2=%d" % pos2, line[pos+pos2:]
		if pos2 >= 0:
			status = EDEF
			pos3 = pos+ pos2 -1
			if line[pos3]==' ': 
				pos3 -= 1
			if line[pos3]==':' or line[pos3]==';':
				pos3 -= 1
		
			print KDEF, line[pos:pos3]
			engdef = line[pos+pos2:]
			#print EDEF, line[pos2:]
		else:
			if kordef:
				print KDEF, line[pos:]
	else:
		#print "##error in line %d"%n, "KDEF NOT found :"
		#print "#", line
		pass

	if i >= num_lines:
		#print "## Not Full process:: i=%d, len(buff)=%d" % (i, num_lines)
		#print "#", line
		return 0

	line = buff[i]
	if line.startswith("영어"):
		status = EDEF		
		pos = line.find(':')
		if pos<0:
			#print "##error in line %d"%n, "NOT found :"
			#print "#", line
			return 0
		try:
			if line[pos+1]==' ': pos += 2
			else: pos += 1
			#print EDEF, line[pos:]
			if engdef:
				engdef += ' '+ line[pos:]
			else:
				engdef = line[pos:]
			if i+1 < num_lines and buff[i+1][0].isalpha():
				i += 1
				engdef += ' '+ buff[i]
				
			if engdef:
				print EDEF, engdef

		except:
			#print "##error in line %d"%n, "Empty EDEF"
			#print "#", line
			pass
		i += 1
	else:
		if engdef:
			print EDEF, engdef
			pass
		else:
			#print "##error in line %d"%n, "EDEF NOT found :"
			#print "#", line
			pass
	
	
	if i >= num_lines:
		#print "## Not Full process:: i=%d, len(buff)=%d" % (i, num_lines)
		#print "#", line
		return 0

	line = buff[i]
	if line.startswith("예문"):
		status = EX		
		example = None
		pos = line.find(':')
		if pos<0:
			#print "##error in line %d"%n, "NOT found :"
			#print "#", line
			return 0
		try:
			if line[pos+1]==' ': pos += 2
			else: pos += 1
			example = line[pos:]

			while 1:
				i += 1
				if i>= num_lines: break

				line = buff[i]
				example += ' '+line
				#if line[-1]!='.' and line[-1]!='?':

			print EX, example

		except:
			#print "##error in line %d"%n, "Empty EX"
			#print "#", line
			return 0
	else:
		#print "### strange kor"
		pass

	if i != num_lines:
		print "## Not Full process:: i=%d, len(buff)=%d" % (i, num_lines)
	return 1

###
def prn_lines(b):
	for line in b:
		print line
	print

##### main
#f = open("/home/anydict/work_OLD/EngDic/KILIVOCA33000.txt")
f = open("/home/anydict/work/EngDic/KILIVOCA33000.txt")

n=0
status=NONE
buffer=[]
lines=0
cnt = 0
for line in f:
	n += 1
	if n>100000: break

	line = line.strip()

	if not line: 
		status = NONE
		handle_one_block(buffer)
		if len(buffer):
			#prn_lines( buffer )
			cnt += 1
			buffer=[]
		continue

	if line[0]=='#': continue
	buffer.append(line)
	#print line

print "####", cnt, "words"
