#!/bin/env python
# -*- coding: EUC-KR -*-

import adtemplate
import adstatic
import recent

if __name__=='__main__':

	print 'Content-Type: text/html\n'

	WORD = adstatic.randWord()
	keywords = "컴퓨터 조립 서버 구축, 번역, 영화, DVD, 서버, 광랜,  랜카드, 초고속 인터넷, 위성 방송, DMB, 학원, 수능 방송 "

	#adtemplate.adHead(keywords, "애니딕: 인터넷 영어 예문 사전 " )
	adtemplate.googleHead(keywords, "애니딕: 인터넷 영어 예문 사전 " )
	adtemplate.adLogo(keywords)
	adtemplate.adForm("ad.py", WORD)
	#adtemplate.adGoogle()

	recent.prn_recent()
	print "<BR/>"

	adtemplate.adGoogle()

	adstatic.adAnnounce()

	adtemplate.adFooter(1)

