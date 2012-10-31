<%@ page import="net.sf.json.JSONObject"%>
<%@ page contentType="text/html; charset=UTF-8"%>
<%@ taglib uri="http://java.sun.com/jstl/core_rt" prefix="c"%>

<%
	response.setHeader("Pragma", "No-cache"); 
	response.setDateHeader("Expires", 0); 
	response.setHeader("Cache-Control", "no-Cache");
	
	//String resultCode = request.getParameter("resultCode");
	JSONObject jsonObject =(JSONObject)request.getAttribute("sendData");
	String resultCode = jsonObject.getString("resultCode");
	
	if(resultCode != null && resultCode.equals("0")){
		int meetingListCount =jsonObject.getInt("meetingListCount");
		if(meetingListCount!=0){
			String Iswrite = jsonObject.getString("Iswrite");
			if(Iswrite !="N"){
				RequestDispatcher rd = request.getRequestDispatcher("/test/redirect.jsp");
				rd.forward(request, response);	
			}
		}else{
			RequestDispatcher rd = request.getRequestDispatcher("/test/redirect1.jsp");
			rd.forward(request, response);	
		}
	}
%>

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>모임 글쓰기</title>
<script type="text/javascript"
	src="${pageContext.request.contextPath}/scripts/jquery-1.4.2.min.js"></script>
<script type="text/javascript"
	src="${pageContext.request.contextPath}/scripts/sha1.js"></script>
<script type="text/javascript"
	src="${pageContext.request.contextPath}/scripts/jquery.form.js"></script>
<SCRIPT LANGUAGE="JavaScript">
//<!--
	var oldStr, oldCnt; 
	
	function init(){
		chkMeeting();
	}
 
	function doAction() {  

		if($('#meetingID').val() == ''){
			alert("모임을 선택하세요.");
			return
		}
		
		if($('#content').val() == ''){
			alert("글을 입력하세요.");
			$('#content').focus();
			return
		}  
	 
		if($('#data').val() == ''){
			$('#upLoadFileCnt').val(0);
		} 
		else{
			if(!upload())
				return;
			$('#upLoadFileCnt').val(1);
		}
	 
		doSubmit();
	}
	
	
	function doSubmit(){
		setCookie('meetingID', $('#meetingID').val(), 1);
		$('#contentsForm').attr('action', '${pageContext.request.contextPath}/meeting/writeMeeting.do').submit();
	}
	
	
	function dologSubmit(){
		deleteCookie('userID');
		deleteCookie('accessToken');
		deleteCookie('meetingID');
		$('#contentsForm').attr('action', '${pageContext.request.contextPath}/webs/meetingLogout.do').submit();
	} 
	

	function upload() {
    	var path = document.getElementById("data").value;
    	var typ = new Array("jpeg","jpg","png","gif","bmp");
 
 		var size = 1024*1024*5; 

	    if(!typcheck(path, typ)) { 
	        alert("업로드 가능한 파일은\n확장자가  jpeg,jpg,png,gif,bmp 인 파일입니다");  
	        return false; 
	    } 
  
	    return true; 
	}  
	
	
	// 확장자 체크(path:파일명, typ:체크할 확장자)
	function typcheck(path, typ) { 
	    var lastidx = -1; 
	    lastidx = path.lastIndexOf('.'); 
	    var extension = path.substring(lastidx+1, path.length); 
	  
	    if((lastidx != -1)){
	    	for(i = 0; i < typ.length; i++){
	    		if((extension.toLowerCase() == typ[i])){
	    			return true;
	    		}
	    	}
	    } 
	         
	    return false; 
	}
	
	function checkByte(element,cbyte) { 
	    var onechar; 
	    var tcount = 0; 

	    for (k=0;k<element.value.length;k++) { 
	        onechar = element.value.charAt(k); 

	        if (escape(onechar).length > 4) 
	            tcount += 2; 
	        else if (onechar!='\r') 
	            tcount++; 
	    } 

	    if(tcount>cbyte) { 
	        alert("허용된 글자수가 초과되었습니다.\r\n초과된 부분은 자동으로 삭제됩니다."); 
	        element.value = oldStr; 
	        tcount = oldCnt; 
	    } 
	    oldStr = element.value; 
	    oldCnt = tcount; 
	} 


	 function setCookie( cookieName, cookieValue, expireDate )
	   {
	    var today = new Date();
	    today.setDate( today.getDate() + parseInt( expireDate ) );
	    document.cookie = cookieName + "=" + escape( cookieValue ) + "; path=/;";
	   }
	 
		function getCookie( cookieName ){
		  var search = cookieName + "=";
		  var cookie = document.cookie;
		 
		 // 현재 쿠키가 존재할 경우
		 if( cookie.length > 0 ){
		  // 해당 쿠키명이 존재하는지 검색한 후 존재하면 위치를 리턴.
		  startIndex = cookie.indexOf( cookieName );
		  // 만약 존재한다면
		  if( startIndex != -1 ){
		   // 값을 얻어내기 위해 시작 인덱스 조절
		      startIndex += cookieName.length;

		   // 값을 얻어내기 위해 종료 인덱스 추출
		      endIndex = cookie.indexOf( ";", startIndex );

		      // 만약 종료 인덱스를 못찾게 되면 쿠키 전체길이로 설정
		      if( endIndex == -1) endIndex = cookie.length;

		      // 쿠키값을 추출하여 리턴
		      return unescape( cookie.substring( startIndex + 1, endIndex ) );
		    } else{ // 쿠키 내에 해당 쿠키가 존재하지 않을 경우
		        return false;
		  }
		 } else {   // 쿠키 자체가 없을 경우
		  return false;
		 }
		}

		function deleteCookie( cookieName )
		{
		 var expireDate = new Date();

		 //어제 날짜를 쿠키 소멸 날짜로 설정한다.
		 expireDate.setDate( expireDate.getDate() - 1 );
		 document.cookie = cookieName + "= ; expires=" + expireDate.toGMTString() + "; path=/";
		}
	
		function isCookie(){
			return getCookie('accessToken');
		}
		
		function chkMeeting(){
			var meetingID=getCookie('meetingID');
			for(var i = 0; i < document.getElementById("meetingID").length; i++) {
				if(document.getElementById("meetingID")[i].value == meetingID) {
					document.getElementById("meetingID")[i].selected = "true";
				}
			}
		}
		
//-->
</SCRIPT>


<style type="text/css">
<!--
body {
	background-color: #4D2A8B;
}
-->
</style>
</head>
<body onload="init()">
<form NAME="contentsForm" id="contentsForm" method="POST"
	enctype="multipart/form-data"><input type="hidden" name="userID"
	id="userID"> <input type="hidden" name="accessToken"
	id="accessToken"> <input type="hidden" name="Iswrite"
	id="Iswrite" value="${sendData.Iswrite}"> <input type="hidden"
	name="resultCode" id="resultCode" value="${sendData.resultCode}">
<input type="hidden" name="upLoadFileCnt" id="upLoadFileCnt"> <input
	type="hidden" name="Iswebs" id="Iswebs" value="Y">

<div name="contentDiv" id="contentDiv">
<table width="800" border="0" cellspacing="0" cellpadding="0">
	<tr>
		<td>&nbsp;</td>
		<td width="397" height="768"
			background="${pageContext.request.contextPath}/img/webs/phone.gif">
		<table width="397" border="0" cellspacing="0" cellpadding="0">
			<tr>
				<td height="144" colspan="3">&nbsp;</td>
			</tr>
			<tr>
				<td height="100" colspan="3" align="center" valign="middle"><img
					src="${pageContext.request.contextPath}/img/webs/title02.gif"
					width="119" height="75" /></td>
			</tr>
			<tr>
				<td height="18" colspan="3" align="center" valign="bottom"><select
					name="meetingID" id="meetingID">
					<option value="">모임을 선택하세요.</option>
					<c:forEach var="list" items="${sendData.meetingList}">
						<option value="${list.meetingID}">${list.title}</option>
					</c:forEach>
				</select></td>
			</tr>
			<tr>
				<td height="25" colspan="3" align="center" valign="middle"><img
					src="${pageContext.request.contextPath}/img/webs/text03.gif"
					width="285" height="15" /></td>
			</tr>
			<tr>
				<td height="152" colspan="3" align="center" valign="middle"><textarea
					name="content" id="content" cols="35" rows="10"
					onKeyUp="checkByte(this,'1024')"></textarea></td>
			</tr>
			<tr>
				<td width="100%" height="50" colspan="3" align="center"
					valign="middle"><input type="file" name="data" id="data"
					onkeydown="return false"
					style="height: 25px; width: 300px; ime-mode: disabled"></td>
			</tr>
			<tr>
				<td width="100%" colspan="3" align="center" valign="bottom"><a
					href="javascript:doAction()"><img
					src="${pageContext.request.contextPath}/img/webs/btn04.gif"
					width="201" height="43" border=0 /></a></td>
			</tr>
			<tr>
				<td height="55" colspan="3" align="center" valign="middle"><a
					href="javascript:dologSubmit()"><img
					src="${pageContext.request.contextPath}/img/webs/btn05.gif"
					width="147" height="43" border=0 /></a></td>
			</tr>
			<tr>
				<td height="164" colspan="3" align="center" valign="middle">&nbsp;</td>
			</tr>
		</table>
		</td>
		<td>&nbsp;</td>
	</tr>
</table>
</div>
</form>
<script language="javascript">
$(document).ready(function() {
	if(isCookie()==false){
		location.replace("${pageContext.request.contextPath}/webs/meetingLoginForm.do");
		return;
	}
	$('#userID').val(getCookie('userID'));
	$('#accessToken').val(getCookie('accessToken'));
	if($('#resultCode').val() == '-208'){
		alert("업로드 가능한 파일의 크기는\n 5Mbyte 이하입니다");
		$('#contentsForm').attr('action', '${pageContext.request.contextPath}/meeting/myMeeting.do').submit();
	}
})
</script>
</body>
</html>
