#!/usr/bin/env python
# -*- coding: EUC-KR -*-

HSUFFIX_ORG = [
"��", "��", "��", "��",
"��", "��", 
"��",
"������",
"�ϴ�", "�ִ�", "�ִ�", "����", "����", "����", "��Ű��",
"�����",
"�ϰ�", "��", "�Ͽ�", "�ٿ�",
"����", "��", "����" 
]

def inverse(str):
	tmplist = list(str)
	tmplist.reverse()
	return ''.join(tmplist)

HSUFFIX = map(inverse, HSUFFIX_ORG)
HSUFFIX.sort()



def prnList(ws):
	for w in ws:
		print w


#prnList(HSUFFIX)

## ��Ʈ������ �ѱ� �ܾ �����Ͽ� ������� ����.
def filterHanWords(line):

	hwords = []
	i = 0
	while i < len(line):
		start = i
		hlen = 0
		while i <len(line) and ord(line[i]) > 128 :
			val = (ord(line[i]) << 8) + ord(line[i+1])
			i += 2

			if val >= 0xB0A1 and val <= 0xC8FE:
				hlen += 2

		if hlen > 0:
			hwords.append(line[start:start+hlen])

		i += 1

	return hwords

## �ѱ� stemmer:��� 
## ����, ��� ������ ��� ã��
## HSUFFIX �� �����ϰ�, ���ڿ��� inverse �Ͽ� �ӵ� ���� ����.
def stemHanWord(word, debug=0):
	
	invword = inverse(word) ## ���ڿ��� ������
	stems = [word]
	if len(word) < 6:
		return stems

	for s in HSUFFIX:
		if invword.startswith(s):
			stemlen = len(word) - len(s)
			if stemlen > 2:
				stems.append(word[:stemlen])
				break
		else:
			if cmp(invword, s) < 0: ## this means 'not found'
				break 

	if debug: prnList(stems)
	return stems


# ���վ� ó��
#SPLIT = [
#(8, [ (4,4), (6,2), (2, 6)]),
#(10, [(4,6),(6,4),(4,4,2), (2,4,4)]),
#(12, [(4,4,4), (6,6), (4, 8), (8,4)]),
#(14, [(4,4,4,2), (4, 4 ,6), (4,6,4), (6,4,4)])
#]

SPLIT = [
(8, [ (4,4), (6,2)]),
(10, [(4,6),(6,4),(4,4,2)]),
(12, [(4,4,4), (6,6), (4, 8), (8,4)]),
(14, [(4,4,4,2), (4, 4 ,6), (4,6,4), (6,4,4)])
]

LENG = [s[0] for s in SPLIT]


def splitbylen(str, lens):
	res = []
	total = 0
	for l in lens:
		res.append( str[total:total+l] )
		total += l
	return res	

def stem_complex(word, debug=0):
	if not len(word) in LENG:
		return []

	lenslist = None
	for s in SPLIT:
		if s[0] == len(word):
			lenslist = s[1]
	
	if lenslist == None:
		return []

	stems = []
	for lens in lenslist:
		if lens > 2:
			stems += splitbylen(word, lens)
			
	if debug:
		print word
		for w in stems:
			print " ",w
		print

	return stems


## ���ڿ� �߿� ù �ѱ� ������ ��ġ�� ��ȯ. 
## return -1 if not found

def findhanchar(str, start=0):
	n = start
	while n < len(str):
		if ord(str[n]) > 128: return n
		n += 1
	return -1


if __name__ == "__main__":
	print LENG	

	stemHanWord("��������", 1)
	stemHanWord("�����", 1)

	stem_complex("��ġ��ݼ���", 1)

	stem_complex("��ġ���", 1)

	stem_complex("��������", 1)

