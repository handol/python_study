<%@page contentType="text/html; charset=UTF-8" %>
<%@ taglib uri="http://java.sun.com/jstl/core_rt" prefix="c"%>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>모임 로그인</title> 
<script type="text/javascript" src="${pageContext.request.contextPath}/scripts/jquery-1.4.2.min.js"></script> 
<script type="text/javascript" src="${pageContext.request.contextPath}/scripts/sha1.js"></script> 
<SCRIPT LANGUAGE="JavaScript">
//<!--
 
	
	function validate(){
		if($('#userID').val().ltrim() == ''){
			alert("아이디를 입력하세요.");
			$('#userID').focus();
			return false;
		}
		if($('#userPWD').val() == ''){
			alert("비밀번호를 입력하세요.");
			$('#userPWD').focus();
			return false;
		}
		return true;
	}
	
	
	function doAjaxAction() { 
		if(validate()){  
		$.ajax({
				url : '${pageContext.request.contextPath}/webs/login.do',
				type : 'POST', 	
				dataType : "json", 
				data : { 
						'userID': $('#userID').val(),
						'userPWD': hex_sha1($('#userPWD').val())
						//'userPWD': $('#userPWD').val()
				   		} ,
				success : function(data) {  
				 
					if(data.resultMsg == 'success'){ 
						$('#accessToken').val(data.accessToken);
						setCookie('userID',$('#userID').val(),1);
						setCookie('accessToken',data.accessToken,1);
						$('#loginForm').attr('action', '${pageContext.request.contextPath}/meeting/myMeeting.do').submit();
					}
					else if(data.resultCode == '1'){
						alert("아이디가 존재하지 않습니다.");
						$('#userID').val('');
						$('#userPWD').val('');
						return;
					}
					else if(data.resultCode == '2'){
						alert("비밀번호가 잘못 입력 되었습니다..");
						$('#userPWD').val('');
						return;
					}	
					else if(data.resultCode == '3'){
						alert("deviceID 미존재.");
						$('#userID').val('');
						$('#userPWD').val('');
						return;
					}	
					else if(data.resultCode == '4'){
						alert("삭제된 아이디입니다.");
						$('#userID').val('');
						$('#userPWD').val('');
						return;
					}  	
				},
				error: function () { 
					alert("NOT SUCCESSFUL");
				}
			});  
		}
	}

 
 
   String.prototype.ltrim = function() {
	   var re = /\s*((\S+\s*)*)/;
	   return this.replace(re, "$1");
   }
 
   String.prototype.rtrim = function() {
	   var re = /((\s*\S+)*)\s*/;
	   return this.replace(re, "$1");
   }
 
   String.prototype.trim = function() {
	   return this.ltrim().rtrim();
   }
 
   function setCookie( cookieName, cookieValue, expireDate )
   {
    var today = new Date();
    today.setDate( today.getDate() + parseInt( expireDate ) );
    document.cookie = cookieName + "=" + escape( cookieValue ) + "; path=/;";
   }

   function init(){
	   
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
<form NAME="loginForm" id="loginForm" method="POST">
<input type="hidden" name="accessToken" id="accessToken">
 <table width="800" border="0" cellspacing="0" cellpadding="0">
  <tr>
    <td>&nbsp;</td>
    <td width="397" height="768" background="${pageContext.request.contextPath}/img/webs/phone.gif"><table width="397" border="0" cellspacing="0" cellpadding="0">
      <tr>
        <td height="155" colspan="2">&nbsp;</td>
      </tr>
      <tr>
        <td height="220" colspan="2" align="center" valign="middle"><img src="${pageContext.request.contextPath}/img/webs/title01.gif" width="237" height="149" /></td>
      </tr>
      <tr>
        <td width="120" height="35" align="right" valign="middle"><img src="${pageContext.request.contextPath}/img/webs/text01.gif" width="29" height="15" /></td>
        <td width="277" align="left" valign="middle" style="padding-left:10px"><input type="text" name="userID" id="userID" />
        </td>
      </tr>
      <tr>
        <td width="120" height="35" align="right" valign="middle"><img src="${pageContext.request.contextPath}/img/webs/text02.gif" width="29" height="15" /></td>
        <td width="277" height="35" align="left" valign="middle" style="padding-left:10px"><input type="password" name="userPWD" id="userPWD" style="width:155px" onkeydown="javascript:if(event.keyCode==13) doAjaxAction()"/>
        </td>
      </tr>
      <tr>
        <td height="140" colspan="2" align="center" valign="middle"><a href="javascript:doAjaxAction()"><img src="${pageContext.request.contextPath}/img/webs/btn01.gif" width="221" height="59" border=0/></a></td>
      </tr>
      <tr>
        <td height="183" colspan="2" align="center" valign="middle">&nbsp;</td>
      </tr>
    </table></td>
    <td>&nbsp;</td>
  </tr>
</table>
</form>
</body>
</html>
