#!/bin/env python
# -*- coding: EUC-KR -*-

import adtemplate
import adstatic

if __name__=='__main__':

	print 'Content-Type: text/html\n'

	WORD = adstatic.randWord()
	keywords = "����, ��ȭ, DVD, ����, ����,  ��ī��, �ʰ�� ���ͳ�, ���� ���, DMB, �п�, ���� ��� "

	adtemplate.adHead(keywords, "�ִϵ�: ��ǻ, ���ͳ� " )
	adtemplate.adLogo()
	adtemplate.adForm("ad.py", WORD)
	adtemplate.adGoogle()


	adstatic.adRecent()

	adstatic.adFooter()

