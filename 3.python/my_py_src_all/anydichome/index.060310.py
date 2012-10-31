#!/usr/local/bin/python
# -*- coding: EUC-KR -*-

import random

WLIST = [
	"side by side",
	"anticipate",
	"scrutiny",
	"crab",
	"step by step",
	"stem cell",
	"take over",
	"get rid of",
	"crystal clear",
	"crystal",
	"as of",
	"strike up",
	"pay-as-you-go",
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



DEF_WORD = random.choice(WLIST)

#SMALL_LOGO = '<a href="/logos.html"> %s </a>' % random.choice(IMGLIST) 
SMALL_LOGO = '<a href="/"><img src="/img/han3_1.JPG" height=40 border=0 align="absmiddle"></a>'


KEYWORDS = """\
<META HTTP-EQUIV="Keywords"
CONTENT="����,�п�,����,���, ��ǻ�� ����, ���� ��� ���� ">

"""

STYLE = """\
<style><!--
	body,td,a,p,.h{font-family:����,����,arial,sans-serif;line-height=110%;}
	.ko{font-size: 9pt;}
	.h{font-size: 20px;} .h{color:} .q{text-decoration:none; color:#0000cc;}
	.g{text-decoration:none; color:#0000cc;}
//-->
</style>
"""

SCRIPT = """\
<SCRIPT LANGUAGE="JavaScript"> 
	<!--
	function fo() { 
		document.adform.W.select(); 
		document.adform.W.focus(); 
	}
	-->
</script> 
<script src="/wclick.js" language=javascript></script>
"""

GOOGLE_AD = """\
<script type="text/javascript"><!--
google_ad_client = "pub-3002816070890467";
google_ad_width = 728;
google_ad_height = 90;
google_ad_format = "728x90_as";
google_ad_type = "text_image";
google_ad_channel ="";
google_color_border = "DFF2FD";
google_color_bg = "DFF2FD";
google_color_link = "03364C3";
google_color_url = "008000";
google_color_text = "000000";
//--></script>
<script type="text/javascript"
  src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
</script>
"""

TITLE = "�ִϵ� ���� ���� ����: ��ǻ��, ���ͳ�"

BODY = """\
<body bgcolor=#ffffff text=#000000 link=#0000cc vlink=#0000cc alink=#ff0000 
	onLoad="fo()" ondblclick="ad_go()">
"""

LOGOPART = """\
<TABLE cellSpacing=0 cellPadding=0 width="728" border=0>
<TBODY>
	<TR> 
	<TD noWrap align="left" width=20%> 
	<a href="/logos.html">
		<IMG alt="�ִϵ�" src="/img/logo8-60.jpg" border=0>
	</a> 
	</TD>
	<TD align="left" noWrap > &nbsp; &nbsp; 
		<FONT color=green><B>�ִϵ� ���� ���������</B></FONT> 
	</td> 
	<td> 
<font color="white" size=-2>�˻�, ���� ����, ����, �ʰ�� ���ͳ�, ADSL, ����, ��ǻ�� ����, MP3, PDA, PS2 </font>
	</td> 
	</TR>
</TBODY>
</TABLE>
"""


AD_FORM = """\
<TABLE cellSpacing=0 cellPadding=0 width="728" bgColor=#00b4da border=0>
<TBODY>
<TR height=40>
<TD class=q vAlign=middle noWrap>
    <form name="adform" action="/anyd.py" method="get">
       <FONT color=#ffffff>&nbsp;
        ����/<font color="yellow">�ѿ�</font>/����/����/����/�Ӵ�/�׸�
        </FONT>
        &nbsp;&nbsp;
       <input type=hidden name="F" value=3>
        <INPUT size=30 name="W"  maxlength=50 value="%s">
        <input name="" type=image height=21 alt=�˻� hspace=5 src="/img/srch2.gif" width=35 align=absMiddle border=0>
 
        &nbsp;&nbsp;&nbsp;
        <A class="q" href="/help.html"> <FONT size=-1 color=#ffffff>����</FONT></A>
</TD>
</TR>
</TBODY></TABLE>
""" % DEF_WORD

ANNOUNCE = """
<ul>
<li> "���� ������ ����" &nbsp; ���ͳ� �󿡼� ������ ����ִ� ���� ���� ����.
<li> ����, ���Ǿ�, ���Ǿ�, ����, � �˻� ����. - ���� ������ ���� ������ �˻� ����.
<li> <font color="red"> New </font>
�׸� ���� (2,300 �ܾ�) - �̹���, �׸�, ��Ȳ���� ���� ����� ���� ����~~ 
<li> <font color="red"> New </font>
�ѿ�, �ѱ� �˻�, �Ӵ� ���� ����.
<li> <font color="red"> New </font>
���� �߿� �ܾ ���� Ŭ���ϸ� �ڵ� �˻��� ����.
<li> ���� ���� �������� <font color="green" size=-1>�̸����� </font>���� ���� ���� ������ �� �� �־��.
</ul>
"""
 
FOOTER = """
<font size=-1>&copy;2002,2006 
&nbsp; 
<font color="green"><b> Anydic, Anydict </b> </font>
&nbsp; &nbsp;
<!--
%s
-->
&nbsp; &nbsp;
<!--
<font color="green"><b>Dictionary on Anything, for Anyone.</b></font>
-->
</font>
<font size=-1>
<a class="q" href="/comment.html">����,�Ұ�</a>
&nbsp; &nbsp;
<a class="q" href="http://www.dnsever.com" target="dnsever">������Ӽ���</a>
</font>
<br/>
<font color="white">��ǻ�� ����, �Ǹ�, MP3 �÷��̾�, PDA, PS2 </font>
""" % (SMALL_LOGO)


#### util funcs

def breakline(lines=1):
	print "<BR/> " * lines 

def drawline():
	print "<HR size=1>"

def do_center(func_or_str, align=''):
	if align != '':
		print '<CENTER align="%s">' % align
	else:
		print "<CENTER>"

	if callable(func_or_str):
		func()
	else:
		print func_or_str

	print "</CENTER>"



####### print func

def prn_head():
	print "<html> <head>"
	print '<meta http-equiv=Content-Type content="text/html; charset=euc-kr">'

	print "<title> %s </title>" % TITLE
	print KEYWORDS
	print STYLE
	print SCRIPT
	print "</head>"
	print


def comp_naver():
	COMP_NAVER = """
"stay put" �� ���� ?  "stay put"
"""
	print """<table><tr><td align="left"><font size=-1> %s </font></td></tr></table>""" % COMP_NAVER



def ann_format():
	#do_center("<table><tr><td align='left'><font size=-1> %s </font></td></tr></table>" % ANNOUNCE)
	print """<table><tr><td align="left"><font size=-1> %s </font></td></tr></table>""" % ANNOUNCE

def promote_click():
	if random.randint(1,8)==3:
		do_center( """<font size=-1>���� ���� �߿� �ϳ��� 1���Ͽ� �ѹ� ������ Ŭ���� �ֽø� ���� ��� ������ �˴ϴ� ^^ (���� Ŭ���ϸ� ȿ�� �����ϴ�)""" )
		breakline(1)	

def do_all():
	prn_head()
	
	print BODY
	do_center ( LOGOPART )
	#print LOGOPART
	breakline()

	do_center ( AD_FORM )
	
	breakline(1)
	do_center(GOOGLE_AD)
	breakline(1)

	print """<center> <table><tr><td align="left" width=73%%>"""
	ann_format()
	print """</td>\n<td width=2%%>&nbsp;</td><td align="right" width=25%%>"""
	print """<center> \
<a href="/recent.py"> <font size=-1 color='green'> �ֱ� �˻��� ���� </font></a><br/><br/>\
<!--
<a href="/logos.html"> <font size=-1 color='green'> �ΰ� �ĺ� ���� </font></a><br/>\
-->
</center>"""
	#recent_words()
	print "</td></tr></table> </center>"

	breakline()
	drawline()
	breakline()

	promote_click()

	do_center(FOOTER)

	print "</BODY></HTML>"


## return true if  the word is English or full Korean word
def ishangul(word):
	if ord(word[0]) < 128: return 1

	i = 0
	while i <len(word) and ord(word[i]) > 128 :
		val = (ord(word[i]) << 8) + ord(word[i+1])

		if val >= 0xB0A1 and val <= 0xC8FE:
			i += 2
		else:
			break

	if i == len(word): return 1
	else: return 0

def recent_words():
	try:
		fd = open("/tmp/adword.log", "r")
	except:
		return

	wlist = []
	fd.seek(-170, 2)
	fd.readline()
	while 1:
		word = fd.readline().strip()
		if word == '': break
		if ishangul(word)==0: continue
		if wlist == [] or word != wlist[-1]:
			wlist.append(word)

	wlist.sort()

	print "<table>"
	prev = ''
	n = 0
	for word in wlist:
		if word != prev:
			if n % 2 == 0: print "<tr>"
			print """<td><font size=-1><a class="q" href="/anyd.py?F=3&W=%s">%s</a></font></td>""" % (word.replace(' ','+'), word)
			if n % 2 == 0: print "<td>&nbsp;</td>"
			if n % 2 == 1: print "</tr>"
			prev = word
			n += 1
	if n % 2 == 0:
			print "<td>&nbsp;</td></tr>"
	print "</table></font>"


if __name__ == "__main__":
	print 'Content-Type: text/html\n'
	do_all()
	
	
