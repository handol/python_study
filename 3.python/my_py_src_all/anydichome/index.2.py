#!/bin/env python
# -*- coding: EUC-KR -*-

import adtemplate
import adstatic
import recent

if __name__=='__main__':

	print 'Content-Type: text/html\n'

	WORD = adstatic.randWord()
	keywords = "��ǻ�� ���� ���� ����, ����, ��ȭ, DVD, ����, ����,  ��ī��, �ʰ�� ���ͳ�, ���� ���, DMB, �п�, ���� ��� "

	#adtemplate.adHead(keywords, "�ִϵ�: ���ͳ� ���� ���� ���� " )
	adtemplate.googleHead(keywords, "�ִϵ�: ���ͳ� ���� ���� ���� " )
	adtemplate.adLogo(keywords)
	adtemplate.adForm("ad.py", WORD)
	#adtemplate.adGoogle()

	recent.prn_recent()
	print "<BR/>"

	adtemplate.adGoogle()

	adstatic.adAnnounce()

	adtemplate.adFooter(1)

