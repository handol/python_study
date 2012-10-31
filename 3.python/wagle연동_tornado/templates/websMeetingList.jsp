<%@page contentType="text/html; charset=UTF-8"%>
<%@ taglib uri="http://java.sun.com/jstl/core_rt" prefix="c"%>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>MeetingList</title>
<script type="text/javascript"
	src="${pageContext.request.contextPath}/scripts/jquery-1.4.2.min.js"></script>
<script type="text/javascript"
	src="${pageContext.request.contextPath}/scripts/sha1.js"></script>
<script type="text/javascript">
function doAction(meetingID){
	document.getElementById("meetingID").value=meetingID;
	$('#listForm').attr('action', '${pageContext.request.contextPath}/webs/meetingContentForm.do').submit();
}
</script>
<style type="text/css">
body {
	background-color: #4D2A8B;
}

/* 스크롤박스 & 스크롤바 */
.TDscrollbar {
	SCROLLBAR-FACE-COLOR: #ededed;
	FONT-SIZE: 9pt;
	SCROLLBAR-HIGHLIGHT-COLOR: #fafafa;
	SCROLLBAR-SHADOW-COLOR: #bdbdbd;
	COLOR: black;
	SCROLLBAR-3DLIGHT-COLOR: #ffffff;
	SCROLLBAR-ARROW-COLOR: #89a0bc;
	SCROLLBAR-TRACK-COLOR: #F7FFFF;
	FONT-FAMILY: 굴림;
	SCROLLBAR-DARKSHADOW-COLOR: #ffffff;
}

#scrollbox {
	width: 300;
	height: 435;
	overflow: auto;
	padding: 10px;
	border: 0;
	border-style: solid;
	border-color: black;
}
</style>
</head>
<body>

<form NAME="listForm" id="listForm" method="POST">
 <input type="hidden" name="userID" id="userID" value="${sendData.userID}">
 <input type="hidden" name="accessToken" id="accessToken" value="${sendData.accessToken}">
 <input type="hidden" name="meetingID" id="meetingID">
<table width="800" border="0" cellspacing="0" cellpadding="0">
	<tr>
		<td>&nbsp;</td>
		<td width="397" height="768" background="${pageContext.request.contextPath}/img/webs/phone.gif">
		<table width="397" border="0" cellspacing="0" cellpadding="0">
			<tr>
				<td height="134" colspan="3">&nbsp;</td>
			</tr>
			<tr><td align="center">
				<DIV id="scrollbox" class=TDscrollbar>
				<table width="290" border="1" cellspacing="0" cellpadding="0">
					<c:forEach var="list" items="${sendData.meetingList}">
						<tr>
							<td height="80" width="80" align="center" valign="middle"><img src="${list.imageURL}" width="80" height="80"></td>
							<td height="80" align="left" valign="middle"><a href="javascript:doAction('${list.meetingID}')">${list.title
							}</a></td>
						</tr>
					</c:forEach>
				</table>
				</DIV>
			</td></tr>
			<tr>
				<td height="154" colspan="3">&nbsp;</td>
			</tr>
		</table>
		</td>
		<td>&nbsp;</td>
	</tr>
</table>
</form>
</body>
</html>
