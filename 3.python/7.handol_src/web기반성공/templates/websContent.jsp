 <%@page contentType="text/html; charset=UTF-8" %>
<%@ taglib uri="http://java.sun.com/jstl/core_rt" prefix="c"%>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>contents</title>
<script type="text/javascript" src="${pageContext.request.contextPath}/scripts/jquery-1.4.2.min.js"></script> 
<script type="text/javascript" src="${pageContext.request.contextPath}/scripts/sha1.js"></script>
<script type="text/javascript" src="${pageContext.request.contextPath}/scripts/jquery.form.js"></script>
<SCRIPT LANGUAGE="JavaScript">
//<!--

 
	function doAction() {  

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
		$('#contentsForm').attr('action', '${pageContext.request.contextPath}/talk2/publicWrite.do').submit();
	}
	
	
	function dologSubmit(){
		$('#contentsForm').attr('action', '${pageContext.request.contextPath}/webs/logout.do').submit();
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
<body>
<form NAME="contentsForm" id="contentsForm" method="POST" enctype="multipart/form-data">
 
 <input type="hidden" name="userID" id="userID" value="${sendData.userID}">
 <input type="hidden" name="accessToken" id="accessToken" value="${sendData.accessToken}">
 <input type="hidden" name="Iswrite" id="Iswrite" value="${sendData.Iswrite}">
 <input type="hidden" name="resultCode" id="resultCode" value="${sendData.resultCode}">
 <input type="hidden" name="upLoadFileCnt" id="upLoadFileCnt">
 <input type="hidden" name="Iswebs" id="Iswebs" value="Y">
 
 
<div name = "contentDiv" id = "contentDiv" >
<table width="800" border="0" cellspacing="0" cellpadding="0">
  <tr>
    <td>&nbsp;</td>
    <td width="397" height="768" background="${pageContext.request.contextPath}/img/webs/phone.gif"><table width="397" border="0" cellspacing="0" cellpadding="0">
      <tr>
        <td height="144" colspan="3">&nbsp;</td>
      </tr>
      <tr>
        <td height="118" colspan="3" align="center" valign="middle"><img src="${pageContext.request.contextPath}/img/webs/title02.gif" width="119" height="75" /></td>
      </tr>
      <tr>
        <td height="25" colspan="3" align="center" valign="middle"><img src="${pageContext.request.contextPath}/img/webs/text03.gif" width="285" height="15" /></td>
        </tr>
      <tr>
        <td height="152" colspan="3" align="center" valign="middle"><textarea name="content" id="content" cols="35" rows="10"><c:if test="${sendData.resultCode eq '-208'}">${sendData.content}</c:if></textarea></td>
       </tr>
      <tr>
        <td width="100%" height="50" colspan="3" align="center" valign="middle"><input type="file" name="data" id="data" onkeydown="return false" style="height:25px;width:300px;ime-mode: disabled"></td>
	  </tr>
	  <tr>
        <td width="100%" colspan="3" align="center" valign="bottom"><a href="javascript:doAction()"><img src="${pageContext.request.contextPath}/img/webs/btn04.gif" width="201" height="43" border=0/></a></td>
      </tr>
      <tr>
        <td height="55" colspan="3" align="center" valign="middle"><a href="javascript:dologSubmit()"><img src="${pageContext.request.contextPath}/img/webs/btn05.gif" width="147" height="43" border=0 /></a></td>
      </tr>
      <tr>
        <td height="164" colspan="3" align="center" valign="middle">&nbsp;</td>
      </tr>
    </table></td>
    <td>&nbsp;</td>
  </tr>
</table>
</div>
</form>
<script language="javascript">
$(document).ready(function() {  
	if($('#resultCode').val() == '0'){
		if($('#Iswrite').val() !='N'){
			alert("저장완료.");
		}
	}
	else if($('#resultCode').val() == '-208'){
		alert("업로드 가능한 파일의 크기는\n 5Mbyte 이하입니다"); 
	}

})
</script>
</body>
</html>
