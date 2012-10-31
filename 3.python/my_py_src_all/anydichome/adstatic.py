#!/usr/local/bin/python
# -*- coding: EUC-KR -*-

import random
import adtemplate

WLIST = [
	#"side by side",
	#"raise issue",
	"anticipate",
	"good Samaritan",
	"scrutiny",
	"crab",
	#"step by step",
	"stem cell",
	"take over",
	"get rid of",
	"crystal clear",
	"crystal",
	#"as of",
	"strike up",
	#"pay-as-you-go",
	"Java",
	"��ȭ",
	"����",
	"ĳ����",
	"����",
	"crystal clear"
]


IMGLIST = [
	'<img src="/img/logo_hp.jpg" height=40 border=0 align="absmiddle">',
	'<img src="/img/logo40.JPG" height=40 border=0 align="absmiddle">',
	'<img src="/img/anydict-yahoostyle2.bmp" height=30 border=0 align="absmiddle">',
	'<img src="/img/purpl2red.JPG" height=50 border=0 align="absmiddle">',
	'<img src="/img/c7.jpg" height=40 border=0 align="absmiddle">',
	'<img src="/img/han3_1.JPG" height=40 border=0 align="absmiddle">',
	'<img src="/img/logo9-70.jpg" height=40 border=0 align="absmiddle">',
	'<img src="/img/logo12-70.jpg" height=40 border=0 align="absmiddle">',
	'<img src="/img/logo12-70.jpg" height=40 border=0 align="absmiddle">',
	'<img src="/img/logo12-70.jpg" height=40 border=0 align="absmiddle">',
	'<img src="/img/logo12-70.jpg" height=40 border=0 align="absmiddle">'
]



CON_KEYS = [
"����, �н���, ����, ���, ����, �ʵ� �ϱ�, ���б�, ����ϱ�, SAT, ����, ����, ���� ���� ",
"����, ��ȭ, DVD, ����, ����,  ��ī��, �ʰ�� ���ͳ� ",
"����, ����, ������, �ܵ�, �Ҽ�, ����, ����, ����, �����, ����",
"����, �ʵ� �б�, ��ġ��, ���̹�, �����, ����, ",
"����, ����, ����, ����, ���伥, ������, ���� ",
"��ȭ, ��ȭ, ���, ����, ������, �����, ���� ����, ��������, �Ե�����, ���﷣��",
"��Ʈ�� �߰� ����, TV, �����, ���� û����, ������, DTV, DMB, ���� ��� ",
"TV, �����, ���� û����, ������, DTV, DMB, ���� ��� ",
"MP3, ������, ���� ��ǰ, PSP, X box, ����, ����, �޴�� DPA, �޴���, ��ȭ��, �ִ��� " ]



#SMALL_LOGO = '<a href="/logos.html"> %s </a>' % random.choice(IMGLIST) 
SMALL_LOGO = '<a href="/"><img src="/img/han3_1.JPG" height=40 border=0 align="absmiddle"></a>'


KEYWORDS = """\
<META HTTP-EQUIV="Keywords"
CONTENT="����,�п�,����,���, ��ǻ�� ����, ���� ��� ���� ">

"""


TITLE = "�ִϵ� ���� ���� ����: ��ǻ��, ���ͳ�"



ANNOUNCE = """
<div class="notice">
<b>"think hard"</b> �� �´� ǥ���ϱ��? �����˻��� ���� Ȯ���� ���� �ֽ��ϴ�.
&nbsp;&nbsp;
<a href="/ad.py?F=3&W=think+hard">think hard</a> <br/>
</div>
<DIV class="dahee">
<ul>
<li> "���� ������ ����", ���ͳ� �󿡼� ������ ����ִ� ���� ���� ����.
<li> Webster ���� ����, WordNet ���� �� ���Ǿ� ���� ����.
<li> ���Ǿ�, ���Ǿ�, ����, � �˻� ����. - ���� ������ ���� ������ �˻� ����.
<li> <font color="red"> New </font>
�׸� ���� (2,300 �ܾ�) - �̹���, �׸�, ��Ȳ���� ���� ����� ���� ����~~ 
<li> <font color="red"> New </font>
�ѿ�, �ѱ� �˻�, �Ӵ� ���� ����.
<li> <font color="red"> New </font>
���� �߿� �ܾ ���� Ŭ���ϸ� �ڵ� �˻��� ����.
<!--
<li> ���� ���� �������� <font color="green" size=-1>�̸����� </font>���� ���� ���� ������ �� �� �־��.
-->
</ul>
</DIV>
"""
 
MOTO = [ "�� �ϳ��� ����", "Dictionary for Any"]
FOOTER = """
<BR/> <BR/>
<table width=728><tr><td align="center">
<HR size=1>
<font size=-1>
<font color="black">
&copy;2002,2006 &nbsp; <i> %s </i> &nbsp; <b> Anydic, Anydict </b>
</font>
</font>
<font size=-1>
&nbsp; &nbsp;
<a class="qg" href="/comment.py">����,�Ұ�</a>
&nbsp; &nbsp;
<a class="qg" href="/logos.html">�ΰ� ����</a>
&nbsp; &nbsp;
<a class="qg" href="http://www.dnsever.com" target="dnsever">������Ӽ���</a>
</font>
</td></tr></table>
<br/>
<font color="white">��ǻ�� ����, �Ǹ�, MP3 �÷��̾�, PDA, PS2 </font>
&nbsp; &nbsp;
""" % (random.choice(MOTO))




AD = """
		<script type="text/javascript"><!--
		google_ad_client = "pub-3002816070890467";
		google_ad_width = 728;
		google_ad_height = 90;
		google_ad_format = "728x90_as";
		google_ad_type = "text_image";
		google_ad_channel = "";
		google_language = "ko";
		/*
		google_color_border = "336699";
		*/
		google_color_border = "FFFFFF";
		google_color_bg = "FFFFFF";
		google_color_link = "0000FF";
		google_color_text = "000000";
		google_color_url = "008000";
		//-->
		</script>
		<script type="text/javascript"
		  src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
		  </script>
		  """

AD  = ""

def adFooter():
	if random.randint(1,8)==1:
		adPromote()

	#adtemplate.do_center( FOOTER )
	print FOOTER 

def adAnnounce():
	print """
	<!-- google_ad_section_start -->
	<table><tr><td align='left'><font size=-1> %s </font></td> 
	</tr> <tr> <br/> <td align="center"> &nbsp; %s </td></tr></table>
	<!-- google_ad_section_end -->
	""" % (ANNOUNCE, AD)
	#print ANNOUNCE
	pass


def adRecent():
	print """<table><tr><td align="left" width=73%%>"""
	adAnnounce()

	print """</td></tr></table> """


def adPromote():
	print """<BR/><table width=728><tr><td align="center"><font size=-1>���� ���� �߿� �ϳ��� 1���Ͽ� �ѹ� ������ Ŭ���� �ֽø� ���� ��� ������ �˴ϴ� ^^ (���� Ŭ���ϸ� ȿ�� �����ϴ�) </td></tr></table>""" 


def randWord():
	return random.choice(WLIST)

def randKeywords(word):
	if len(word) > 0:
		r = ord(word[0])
		r %= len(CON_KEYS)
		keywords = CON_KEYS[r]
	else:
		keywords = CON_KEYS[0]
	return keywords


if __name__ == "__main__":
	print 'Content-Type: text/html\n'
	
	
