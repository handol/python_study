from ftplib import FTP 
import sys

print '---connecting..'
ftp = FTP('localhost')

print '---logging in..'
ftp.login('dahee', 'gksehf00')
#ftp.login('usrname', 'password')

print '---getting list'
#ftp.retrlines('LIST')
ftp.retrlines('LIST', open('list.txt', 'w').writelines)
L=[]
ftp.retrlines('LIST', L.append)

print L
sys.exit()
## convert list L to list of lines
lineList=[]
"""
for e in L:
	if (e[0]=='d' and e[1]=='r')
	line
"""
print '---getting dir'
print ftp.dir()

print '---getting nlist'
print ftp.nlst()

print '---downloading welcome.msg'
#ftp.retrbinary('RETR welcome.msg', open('welcome.msg', 'wb').write)

print '---changing dir'
ftp.cwd('script')

print '---getting list'
ftp.retrlines('LIST')

print '---quit'
ftp.quit()

print '---finished' 


