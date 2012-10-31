#!/usr/bin/env python
# -*- coding: EUC-KR -*-
#
# ���� ��� (�ѱ�) ǥ���� ��� ����
# 1~14
# url = "http://sm.krx.co.kr//common/dictionary/kse_voca_left.jsp?language=Korean&dic_typ=A001&code=%02d" % number

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

def idx(anchors, out):
	
	for url,ref in anchors:	
		#num = int(url[-2:])
		#out.write("%d\n" % num)		
		out.write("%s\n" % url)		
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
		url = "http://sm.krx.co.kr//common/dictionary/kse_voca_left.jsp?language=Korean&dic_typ=A001&code=%02d" % number
		html = fetchurl(url)
		if html != "":
			try:
				h2t = html2txt.html2txt(url)
				h2t.feed(html)
				idx(h2t.anchors, out)
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

