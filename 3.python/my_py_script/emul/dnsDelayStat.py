#!/usr/bin/env python
## -*- coding: EUC-KR -*-

# '�ʵ� ��±�'
# 2006. 11.21


import sys

result = []

def dealArg(field):
	'argv�� ó���Ͽ� field number �� return ���ش�.'


	#if field.find(',') != -1:

	newf = field.split(',')
	length = len(newf)

	for seq in newf:
		if seq.find('-') != -1 and seq.find('-') != 0:	# ���� 5-8 �� �ִٸ� 
								# -5, -8 �� �ƴ϶�.
			result.extend(range(int(seq[ 0 ]), int(seq[ 2 ]) + 1))

		else:
			result.append(int(seq))

			
	#result.sort()	
	return result

def openFile(fname):
	if fname=="-":
		return sys.stdin
	else:
		try:
			fp = open(fname, 'r')
			return fp
		except:
			print 'cannot open file:', fname 
			raise
			return None 

def printDns(filename, separator=' '):
	'result �� �������� Ư�� field�� ����Ʈ�Ѵ�'

	fp = openFile(filename)

	if fp==None:
		sys.exit(0)

	for line in fp:
		if line.find("DNS DELAY") !=-1:
			flds = line.split()
			print "%s , %s" % (flds[6], flds[4])


	fp.close()

if __name__ == '__main__':


	if len(sys.argv) == 2:
		printDns(sys.argv[1])

	else:	
		print 'Usuage: input_file'
		sys.exit(0)



