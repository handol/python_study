#!/usr/bin/env python
import os
import sys

def exec_shell(cmnd, prn=1):
	if prn: print os.getcwd(),'#',cmnd
	if prn and LOG: LOG.write(os.getcwd()+' # '+cmnd+"\n")
	res = os.popen(cmnd, 'r').readlines()
	for r in res:
		if prn: print r[:-1]
		if prn and LOG: LOG.write(r)

if __name__== '__main__':
	print os.getcwd()
	for f in os.listdir(os.getcwd()):
		if not f.endswith('.slp'): continue
		if f.find('.1.') >=0 : continue
		print f
		w = f.split('.')
		newf = w[0] + '.1.' + w[1] 
		print f, newf
		exec_shell ("/bin/ln -s %s %s" % (f, newf), prn=0 )

