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

def printField(filename, separator=' '):
	'result �� �������� Ư�� field�� ����Ʈ�Ѵ�'

	try:
		fp = open(filename, 'r')

	except:
		print 'No exist file'
		sys.exit(0)

	for line in fp:
#		line = line[ : -1 ] ####
		if separator == ' ':
			splitedline = line.split()
		else:
			splitedline = line.split(separator)

		output = ""

		#print 'splitline:', splitedline

		tmp = len(result)

		if len(splitedline) < result[ tmp - 1 ] and result[ tmp - 1 ] > 0:
			print 'Field Number Overflowed:',
			print line
			continue

		for num in result:

			# join is faste is faster

			if num < 0:
				output = output + ' ' + splitedline[ num ]
			else:
				output = output + ' ' + splitedline[ num - 1 ]

		print output


	fp.close()

if __name__ == '__main__':


	if len(sys.argv) == 3:
		dealArg(sys.argv[2])
		printField(sys.argv[1])

	elif len(sys.argv) == 4:
		dealArg(sys.argv[2])
		printField(sys.argv[1], sys.argv[3])

	else:	
		print 'Usuage: python prnFields.py input_file list_of_fields [separator]'
		sys.exit(0)



