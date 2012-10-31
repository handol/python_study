#!/bin/env python
# -*- coding: EUC-KR -*-

import adtemplate
import adstatic
import recent

if __name__=='__main__':

	print 'Content-Type: text/html\n'

	WORD = adstatic.randWord()
	keywords = "컴퓨터 조립 서버 구축, 번역, 영화, DVD, 서버, 광랜,  랜카드, 초고속 인터넷, 위성 방송, DMB, 학원, 수능 방송 "

	adtemplate.adHead(keywords, "애니딕: 인터넷 영어 예문 사전 " )
	#adtemplate.googleHead(keywords, "애니딕: 인터넷 영어 예문 사전 " )
	adtemplate.adLogo(keywords)
	adtemplate.adForm("ad.py", WORD)
	#adtemplate.adGoogle()

#	print """
#	<center>
#
#	<object type='application/x-shockwave-flash' width='502px' height='399px' align='middle' classid='clsid:d27cdb6e-ae6d-11cf-96b8-444553540000' codebase='http://fpdownload.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=8,0,0,0'><param name='movie' value='http://flvs.daum.net/flvPlayer.swf?vid=jEvH4s08HaQ$' /><param name='allowScriptAccess' value='always' /><param name='allowFullScreen' value='true' /><param name='bgcolor' value='#000000' /><embed src='http://flvs.daum.net/flvPlayer.swf?vid=jEvH4s08HaQ$' width='502px' height='399px' allowScriptAccess='always' type='application/x-shockwave-flash' allowFullScreen='true' bgcolor='#000000' ></embed></object>
#</center>
#
#	</br>
#	"""

	ttt = """
    <a href="http://condolence.media.daum.net/gaia/do/service/read?bbsId=Notice&articleId=1">
	<img src="pres_noh.jpg" /></a>
    <a href="http://www.seoprise.com/board/view.php?table=seoprise_12&uid=32437">
	<img src="pres_noh_yousimin.jpg" /></a>
</center>
	"""


	adstatic.adAnnounce()

	adtemplate.adGoogle()

	recent.prn_recent()
	print "<BR/>"

	#print "<br/><center><font size=-1 color='green'> <b> 세계 각국의 애니딕 방문자 맵 </b></font></center><br/>"

	VISIT_MAP =  """
<center>
<embed src="http://maps.amung.us/flash/flashsrv.php?k=3tyeacv6&type=emb.swf" quality="high" pluginspage="http://www.macromedia.com/go/getflashplayer" allowScriptAccess="always" allowNetworking="all" type="application/x-shockwave-flash" flashvars="wausitehash=3tyeacv6&map=neosat&pin=default-yellow&link=yes" width="420" height="230" /> 
<br/>
&nbsp; &nbsp;
<a href="http://whos.amung.us/show/jszqcugj"><img src="http://whos.amung.us/widget/jszqcugj.png" alt="page counter" width="81" height="29" border="0" /></a> 
</center>
	"""

	#print VISIT_MAP

	adtemplate.adFooter(1)

