#!/usr/bin/env python
# -*- coding: EUC-KR -*-
#
import html2txt
from urllib import urlopen


URL = "http://sm.krx.co.kr/common/dictionary/kse_voca_body.jsp?dic_seq_no=18"

URL_RANGE = "1~13098"

SAMPLE = """\
KRX���ǿ�����
�ɼǺ� ��ä
(
Bond with imbedded option
)
�ɼǺλ�ä(BO)�� ä�� ����� ���õǴ� ���� ������ �����Ǹ� ���� ���̶� ����ȸ��� ��ä���ڿ��� �ŵ�û��(call option)��, ��ä���ڴ� ����ȸ�翡 ��ȯû��(put option)�� �� �� �ִ� �Ǹ��� �ο��� ���ο� ä���̴�.

"""

def save():
	pass

def process(txt, out):
	lines = txt.split('\n')

	#for l in lines:
	#	print l

	head = lines[1].strip()
	second = lines[3].strip()
	expl = ' '.join( lines[5:] )
	expl = expl.strip()

	if head == '': return

	print head

	out.write("@@0 %s\n" % head)
	if second != '': 
		out.write("@@1 %s\n" % second)
	if expl != '': 
		out.write("$$ %s\n" % expl)
	out.write('\n')
	
	pass


def fetchurl(url):
	try:
		doc = urlopen(url).read()
		return doc
	except:
		print "fetch failed for ", url
		return ""

def main(fromnum, tonum, out):
	for number in range(fromnum, tonum+1):
		print number
		url = "http://sm.krx.co.kr/common/dictionary/kse_voca_body.jsp?dic_seq_no=%s" % number
		html = fetchurl(url)
		if html != "":
			try:
				h2t = html2txt.html2txt(url)
				h2t.feed(html)
				process(h2t.data, out)
			except:
				print "fail for number : %d" % number
		

if __name__ == "__main__":
	import sys
	if len(sys.argv) < 4:
		print "usage: %s from to outfile" % sys.argv[0]
		sys.exit(0)


	try:
		out = open(sys.argv[3], "w+")
		main (int(sys.argv[1]), int(sys.argv[2]), out)	
	except:
		print "cannot write outfile", sys.argv[3]

