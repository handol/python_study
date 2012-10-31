import smtplib

def send_mail(sender, recver, mailtitle, htmlfile):
	f = open(htmlfile, 'r')
	html = f.read(  )
	f.close(  )
	subject = "Today's Newsletter!"
	message = createhtmlmail(subject, html, text)
	server = smtplib.SMTP("localhost")
	server.sendmail('agillesp@i-noSPAMSUCKS.com',
	'agillesp@i-noSPAMSUCKS.com', message)
	server.quit(  )
