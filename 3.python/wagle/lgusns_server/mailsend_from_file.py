#####
# http://www.tutorialspoint.com/python/python_sending_email.htm

import smtplib

sender = 'wagle.help@gmail.com'
receivers = ['kimkh09@gmail.com', 'doimoi00@gmail.com', 'handol@gmail.com', 'metalinxx@gmail.com']
receivers = ['handol@gmail.com']


###########
def send_mail(svraddr, sender, receiver, message):
	try:
	   smtpObj = smtplib.SMTP(svraddr)
	   smtpObj.sendmail(sender, receiver, message)         
	   print "Successfully sent email"
	   smtpObj.quit() 
	except SMTPException:
	   print "Error: unable to send email"
	   smtpObj.quit() 
	

###########
def build_msg(sender, recver, subject, htmlmesg):
	message = """From: <%s>
To: <%s>
MIME-Version: 1.0
Content-type: text/html
Subject: %s

This is an e-mail message to be sent in HTML format

""" % (sender, recver, subject)

	message += htmlmesg
	
	return message	



###
def get_recv_list(filename):
	recv_list = ''
	try:
		recv_list = open(filename).read()
		print recv_list
	except:
		pass

	real_list = map(recv_list.split('\n'), trim)

	

#######################
sender = "wagle.help@gmail.com"
title = "This is handol's mail test #2"
htmlmsg = """<br/> <b>This is HTML message.</b>
<h1>This is headline.</h1>
"""

### read html from file
try:
	htmlmsg = open("anydic.html").read()
	print htmlmsg
except:
	pass

for recver in receivers:
	print "======", recver
	mailmesg = build_msg(sender, recver, title, htmlmsg)  
	#print mailmesg
	print
	#send_mail('211.233.77.10', sender, recver, mailmesg)
