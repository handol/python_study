#!/usr/local/bin/python
# -*- coding: EUC-KR -*-

import random

GOOGLE_AJAX_HEAD = """\
			<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
			<html xmlns="http://www.w3.org/1999/xhtml">
		<head> 
			<meta http-equiv="content-type" content="text/html; charset=euc-kr"/>    
		    <link href="http://www.google.com/uds/css/gsearch.css" type="text/css" rel="stylesheet"/>

	<style type="text/css">
      @import url(http://www.google.com/uds/css/gsearch.css);

      body {
        font-family: "trebuchet ms", verdana, sans-serif;
        font-size: 14px;
      }

    </style>

	<link href="/css/exlist.css" type="text/css" rel="stylesheet"/>

			<script src="http://www.google.com/uds/api?file=uds.js&amp;v=1.0&amp;key=ABQIAAAAuJ3hfnP9diZwZOI8o_i3PxSwhidGAexeFr_Ys8opf9fuPuzevBTiT0isnEvqAs0r1fUMSnGe8Y0NmQ" type="text/javascript"></script>
			
			<script language="Javascript" type="text/javascript">    
			//<![CDATA[    
			google.load("search", "1", {"language" : "en"});


			function OnLoad() {      // Create a search control      
			var searchControl = new GSearchControl();      // Add in a full set of searchers      
			//searchControl.setResultSetSize(GSearch.LARGE_RESULTSET);
			searchControl.setResultSetSize(GSearch.SMALL_RESULTSET);

			imgsrch = new GimageSearch();
			searchControl.addSearcher(imgsrch);
			//imgsrch.setResultSetSize(GSearch.LARGE_RESULTSET);
			imgsrch.setResultSetSize(GSearch.SMALL_RESULTSET);
			searchControl.addSearcher(new GwebSearch());      
			searchControl.addSearcher(new GnewsSearch());
			//searchControl.addSearcher(new GblogSearch());      
			//searchControl.addSearcher(new GvideoSearch());      
			//var localSearch = new GlocalSearch();
			// Set the Local Search center point      
			//localSearch.setCenterPoint("New York, NY");      

			// Tell the searcher to draw itself and tell it where to attach      
			var drawOptions = new GdrawOptions();
			drawOptions.setDrawMode(GSearchControl.DRAW_MODE_TABBED);
			//drawOptions.setDrawMode(GSearchControl.DRAW_MODE_LINEAR);
			searchControl.draw(document.getElementById("searchcontrol"), drawOptions);      

			// Execute an inital search      
			searchControl.execute("stringToSearch");    }    
			
			//GSearch.setOnLoadCallback(OnLoad);  
			google.setOnLoadCallback(OnLoad);  
			//]]>
			</script>

<META HTTP-EQUIV="Keywords" CONTENT="%s">
<TITLE> %s </TITLE>
<!--
<LINK REL="stylesheet" HREF="/def.css" TYPE="text/css">
-->
<script src="/wclick.js" language=javascript></script>
			</head>
"""

HEAD= """\
<HTML>
<HEAD>
<META http-equiv=Content-Type content="text/html; charset=euc-kr">
<META HTTP-EQUIV="Keywords" CONTENT="%s">

<TITLE> %s </TITLE>
<LINK REL="stylesheet" HREF="/def.css" TYPE="text/css">
<LINK href="/favicon.ico" rel="SHORTCUT ICON" type="image/x-icon">
<script src="/wclick.js" language=javascript></script>
</HEAD>
"""

GOOGLE_SUGGEST2 = """\
		<script type="text/javascript"><!--
		google_ad_client = "pub-3002816070890467";
		google_ad_width = 728;
		google_ad_height = 90;
		google_ad_format = "728x90_as";
		google_cpa_choice = "CAEaCDPSFdVHL0WGUC1QElBDUC9QBVA0";
		google_ad_channel = "9690214772";
		google_color_border = "000000";
		google_color_bg = "000000";
		google_color_link = "FFFFFF";
		google_color_text = "CCCCCC";
		google_color_url = "999999";
		//-->
		</script>
		<script type="text/javascript" src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
		</script>
		"""

GOOGLE_SUGGEST2 = """\
		<script type="text/javascript"><!--
		google_ad_client = "pub-3002816070890467";
		google_ad_width = 728;
		google_ad_height = 90;
		google_ad_format = "728x90_as";
		google_cpa_choice = "CAEaCDPSFdVHL0WGUC1QElBDUC9QBVA0";
		google_ad_channel = "9690214772";
		google_color_border = "FFFFFF";
		google_color_bg = "FFFFFF";
		google_color_link = "34809c";
		google_color_text = "000000";
		google_color_url = "008000";
		//-->
		</script>
		<script type="text/javascript" src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
		</script>
		"""



BG_COLOR = "eef5f7"

## anydic_lower CHANNEL
GOOGLE_AD_LOWER = """\
<script type="text/javascript"><!--
google_ad_client = "pub-3002816070890467";
/* 728x90, created 3/23/09 */
google_ad_slot = "0681829992";
google_ad_width = 728;
google_ad_height = 90;
//-->
</script>
<script type="text/javascript"
src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
</script>
<br/>
"""

## anydic_upper CHANNEL
GOOGLE_AD_UPPER = """\
<script type="text/javascript"><!--
google_ad_client = "pub-3002816070890467";
/* 728x90, created 3/23/09 */
google_ad_slot = "0513021871";
google_ad_width = 728;
google_ad_height = 90;
//-->
</script>
<script type="text/javascript"
src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
</script>
<br/>
"""


GOOGLE_ANALYTICS = """\
<script src="http://www.google-analytics.com/urchin.js" type="text/javascript">
</script>
<script type="text/javascript">
_uacct = "UA-1321944-1";
urchinTracker();
</script>
"""

TITLE = "애니딕 "

BODY = """\
<body bgcolor=#ffffff text=#000000 link=#0000cc vlink=#0000cc alink=#ff0000 
	onLoad="" ondblclick="ad_go()">
"""

pkgad1 = """\
<script type="text/javascript"><!--
google_ad_client = "pub-3002816070890467";
google_ad_output = "textlink";
google_ad_format = "ref_text";
google_cpa_choice = "CAAQ7K-kyAIaCHhbgWRwFbrNKJT5uYsB";
google_ad_channel = "";
//--></script>
<script type="text/javascript" src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
</script>
"""

pkgad2 = """\
<script type="text/javascript"><!--
google_ad_client = "pub-3002816070890467";
google_ad_width = 110;
google_ad_height = 32;
google_ad_format = "110x32_as_rimg";
google_cpa_choice = "CAAQ0LnEmwIaCKCSGkPG7dgLKLzHuYsB";
google_ad_channel = "";
//--></script>
<script type="text/javascript" src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
</script>
"""


referal_ad = """
<script type="text/javascript"><!--
google_ad_client = "pub-3002816070890467";
google_ad_width = 468;
google_ad_height = 60;
google_ad_format = "468x60_as_rimg";
google_cpa_choice = "CAAQ9di1_wEaCJZej6mzxZUvKIGN4YcB";
google_ad_channel = "";
//-->
</script>
<script type="text/javascript" src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
</script>
"""

Google_Pkg_Ad = """\
<TD width=200 >
<FONT size=+0>
%s
</FONT>
</TD>
""" % (referal_ad)

#<TD width=200 >

Google_Pkg_Ad = """\
&nbsp; &nbsp;
<FONT size=-1>
<a class="qg"  href="adsense/1.html" target="_new"> <font size=-1> 구글 애드센스</font></a>
</FONT>
""" 


LOGO= """\
<!-- google_ad_section_start -->
<TABLE cellSpacing=0 cellPadding=0 width=728 border=0>
<TBODY>
	<TR> 
	<TD width=200 align="left" noWrap >
	<a href="/"> <IMG alt="애니딕" src="/img/logo8-40.jpg" border=0> </a> 
	</td> 
	<TD noWrap align="left"> 
	&nbsp; &nbsp; <FONT size=+1 color=Black><B>애니딕 생생 영어 예문 사전</B></FONT> 
	</TD>

	<TD align="center" > 
	<!--
	<a href="/engtran/"> 
	<FONT color="black" size=-1> 영어기사번역 </FONT></a>
	-->
	</TD> 

	<TD align="center" valign="middle" > 
	<a href="http://jeena.tistory.com" target="blog">
	<IMG alt="애니딕" src="/img/quest_excl_40.jpg" border=0>
	</a>
	<a href="http://jeena.tistory.com" target="blog">
	<FONT color="black" size=-1> 블로그 </FONT> </a> %s 
	</TD> 

	%s 
	</TR>
</TBODY>
</TABLE>
<!-- google_ad_section_end -->
""" 

CGI = "ad.py"

OLD_FORM_COLOR = "#00b4da"
FORM = """\
<!-- google_ad_section_start -->
<TABLE cellSpacing=0 cellPadding=0 width="100%%" background="/img/bg_search.gif" border=0>
<TBODY>
<TR height=40>
<TD width="620" class=q vAlign=middle noWrap>
    <form name="adform" action="/%s" method="post">
		<b>
       <FONT size=-1 color="white">&nbsp;
        영영/<font color="white">한영</font>/영한/예문/숙어/속담/그림
        </FONT>
		</b>
        &nbsp;&nbsp;
       <input type=hidden name="F" value=3>
        <INPUT size=30 name="W"  maxlength=50 value="%s">
        <input name="" type=image height=21 alt=검색 hspace=5 src="/img/srch2.gif" width=35 align=absMiddle border=0>
 
        &nbsp;&nbsp;
        <A class="q" href="/help.html"> <FONT size=-1 color="yellow">도움말</FONT></A>
</TD>
	<TD nowrap align="left"> &nbsp;&nbsp;<a class="qg" href="/recent.py"><font size=-1 color="yellow"> 실시간 검색어 </font></a>
        &nbsp;
	</td> 

</TR>
</TBODY></TABLE>
<!-- google_ad_section_end -->
"""

 
MOTO = [ "또 하나의 사전", "Dictionary for Anything, Anyone"]

FOOT2 = \
"""
&nbsp; &nbsp;
<a class="qg" href="/comment.py">제안,소감</a>
&nbsp; &nbsp;
<!--
<a class="qg" href="/logos.html">로고 보기</a>
&nbsp; &nbsp;
-->
<a class="qg" href="http://www.dnsever.com" target="dnsever">무료네임서버</a>
"""

FOOT0 =\
"""
<BR/>
<HR size=1>
"""

FOOT1 =\
"""
&copy;2002,2010 &nbsp;  <i> %s </i> &nbsp; <b> &reg; Anydic, Anydict </b>
""" % random.choice(MOTO)

FOOTER = FOOT1 + Google_Pkg_Ad + "<br/>" + FOOT2 + "<br/>"
FOOTER = FOOT0 + """<div class="footer">""" + FOOT1 + "&nbsp; &nbsp;" + FOOT2 + Google_Pkg_Ad + "</div> <br/>"


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
		func_or_str()
	else:
		print func_or_str

	print "</CENTER>"



####### print func

RAND = 0

def adHead(keywords, title):
	print HEAD % (keywords, title)

def googleHead(word, keyword="애니딕 영어 예문 사전", title="애니딕 인터넷  영어 예문 사전"):
	header = GOOGLE_AJAX_HEAD.replace("stringToSearch", word);
	#print header % (keyword, title + ": %s" % word)
	print header % (keyword, title)

def adLogo(keyForAds=''):
	print BODY

	#do_center ( LOGO)
	keyForAds = ""
	print LOGO % ("&nbsp;", keyForAds)
	#print LOGO % (keyForAds, Google_Pkg_Ad)
	#breakline()

def adForm(cginame, searchword):
	print FORM % (cginame, searchword)
	breakline()
	#adGoogleSearch()
	

def adGoogleSearch():
	GSEARCH = """\
<!-- SiteSearch Google -->
<form method="get" action="http://www.google.co.kr/custom" target="google_window">
<table border="0" bgcolor="#ffffff">
<tr><td nowrap="nowrap" valign="top" align="left" height="32">
<a href="http://www.google.com/">
<img src="http://www.google.com/logos/Logo_25wht.gif" border="0" alt="Google" align="middle"></img></a>
</td>
<td nowrap="nowrap">
<input type="hidden" name="domains" value="anydict.com"></input>
<label for="sbi" style="display: none">검색어를 입력하십시오.</label>
<input type="text" name="q" size="32" maxlength="255" value="" id="sbi"></input>
<label for="sbb" style="display: none">검색양식 제출</label>
<input type="submit" name="sa" value="검색" id="sbb"></input>
</td></tr>
<tr>
<td>&nbsp;</td>
<td nowrap="nowrap">
<table>
<tr>
<td>
<input type="radio" name="sitesearch" value="" id="ss0"></input>
<label for="ss0" title="웹 검색"><font size="-1" color="#000000">Web</font></label></td>
<td>
<input type="radio" name="sitesearch" value="anydict.com" checked id="ss1"></input>
<label for="ss1" title="검색 anydict.com"><font size="-1" color="#000000">anydict.com</font></label></td>
</tr>
</table>
<input type="hidden" name="client" value="pub-3002816070890467"></input>
<input type="hidden" name="forid" value="1"></input>
<input type="hidden" name="ie" value="EUC-KR"></input>
<input type="hidden" name="oe" value="EUC-KR"></input>
<input type="hidden" name="cof" value="GALT:#008000;GL:1;DIV:#336699;VLC:663399;AH:center;BGC:FFFFFF;LBGC:FFFFFF;ALC:0000FF;LC:0000FF;T:000000;GFNT:0000FF;GIMP:0000FF;LH:50;LW:174;L:http://anydict.com/img/logo8-50.jpg;S:http://anydict.com;FORID:1"></input>
<input type="hidden" name="hl" value="ko"></input>
</td></tr></table>
</form>
<!-- SiteSearch Google -->
"""
	print GSEARCH
	print "<BR/>"

def adGoogle():
	print GOOGLE_AD_UPPER
	breakline()

def adGoogle2():
	print GOOGLE_AD_LOWER
	breakline()

def adPromote():
	return
	print """<BR/><table width=728><tr><td align="center"><font size=-1>위의 광고 중에 하나를 1주일에 한번 정도만 클릭해 주시면 서비스 운영에 도움이 됩니다 ^^ (자주 클릭하면 효과 없습니다) </td></tr></table>""" 

def adFooter(flag=0):
	#do_center(FOOTER)
	if flag:
		#if random.randint(1,8)==1: adPromote()
		print "<BR/>"
		#adGoogle()
		print FOOTER
	else:
		print "<BR/>"
		#adGoogle()
		print FOOTER
	print GOOGLE_ANALYTICS
	print "</BODY> </HTML>"


if __name__ == "__main__":
	print 'Content-Type: text/html\n'

	adHead("여호텔 예약, 비행기 예매", "This test title")
	adLogo()
	adForm("ad.py","hello")
	adGoogle()
	adFooter()
	
