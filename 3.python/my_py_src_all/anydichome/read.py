#!/usr/local/bin/python
# -*- coding: EUC-KR -*-

import adtemplate
import adstatic

def prnFile(fname):
	try:
		fd = open(fname, 'r')
	except:
		return

	print fd.read()

if __name__=='__main__':

	print 'Content-Type: text/html\n'

	WORD = adstatic.randWord()
	keywords = "Ư��, ���̵��, ���伥, ������, ���� ���� "

	adtemplate.adHead(keywords, "�ִϵ� ����,�Ұ�, ���̵��, ������ " )
	adtemplate.adLogo()
	adtemplate.adForm("ad.py", WORD)
	adtemplate.adGoogle()

	prnFile("cmnt.html")


	adstatic.adFooter()

