from ftplib import FTP 
import os
import os.path

remoteDIR = '/home/dahee/dev/hlrsvc/HLRSVC/'
localDIR = '/cygdrive/c/2003work/HLRSVC/'

fList = [ 
#		'src/slp/gsm/pagereq.script', \
#		'src/slp/gsm/statusrep.script', \
#		'src/slp/gsm/slp_pagereq.c ', \
#		'src/slp/gsm/slp_svcreq.c ', \
#		'src/slp/gsm/slp_statusrep.c ', \
#		'src/slp/gsm/slp_code_sri_gsm.c ', \
#		'src/slp/gsm/slp_code_sri_gsm.h ', \
		'src/slp/gsm/slp_code_sri_gsm_utils.c ', \
#		'src/slp/gsm/slp_code_sri_gsm_intw.c ', \
#		'src/slp/gsm/slp_gmap_intw.c ', \
#		'src/slp/gsm/slp_util2.c ', \
#		'src/dbserv/hlrdb/sri_gsm_sleeapi.c ', \
#		'src/dbserv/hlrdb/init_dbfunc.c ', \
#		'include/gsm_db.h ', \
#		'include/gsm_dbdef.h ', \
#		'#SIM/actest/sri_gsm.c', \
#		'#SIM/actest/sri_gprs.c', \
		'0'
        ]
        
          
print '---connecting..'
ftp = FTP('192.168.1.16')

print '---logging in..'
ftp.login('dahee', 'gksehf00')
#ftp.login('usrname', 'password')


for f in fList:
  if f[0]=='#': continue
  if f[0]=='0': break
  
  localP = os.path.join(localDIR, f)
  remoteP = os.path.join(remoteDIR, f)
  lDir = os.path.dirname(localP)
  rDir = os.path.dirname(remoteP)
  fname = os.path.basename(f)
  print lDir, rDir, fname
  
  #print open(localP, 'rb').read()
  a = raw_input("upload %s " % fname).strip()
  
  if a != 'y': continue
  
  
  os.chdir(lDir)
  ftp.cwd(rDir)
  try:
    #ftp.retrbinary('RETR %s' % fname, open(localP, 'wb').write)
    ftp.storbinary('STOR %s' % fname, open(localP, 'rb'))
  except:
    print "!!! error: %s " % fname
    raise
    

ftp.quit()

#ftp.storbinary('STOR welcome.msg', open('welcome.msg', 'rb'))
#ftp.storlines('STOR welcome.msg', open('welcome.msg', 'rb'))

#ftp.retrbinary('RETR welcome.msg', open('welcome.msg', 'wb').write)
#ftp.retrlines('LIST', open('list.txt', 'w').write)
#print ftp.dir()
#print ftp.nlst()
#ftp.retrlines('LIST')
#ftp.retrlines('LIST', open('list.txt', 'w').write)
#ftp.quit()




#ftp.delete()
#ftp.rename()
#ftp.mkd()
#ftp.rmd()
