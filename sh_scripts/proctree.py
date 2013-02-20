#!/usr/bin/env python
import os
import os.path
import sys
#import time
from stat import *


def get_users_in_dir(home_dir):
	""" get user names under '/home'
	"""
	users = []
	for f in os.listdir(home_dir):
		pathname = os.path.join(home_dir, f)
		stinfo = os.stat(pathname)
		mode = stinfo[ST_MODE]
		if  S_ISDIR(mode): users.append(f)
	return users


def get_users_in_passwdfile(fname, min_id):
	"""
	fname is '/etc/passwd'
	"""
	users = []
	try:
		f = open(fname, 'r')
	except:
		print "read fail: ", fname
		return []

	for l in f.readlines():
		w = l.split(':')
		if int(w[2]) > min_id: users.append(w[0])
	return users


def prn_process(w, depth):
	if w[3][0].isalpha():
		print '   '*depth+"[%s] " % w[0] + ' '.join(w[7:])
	else:
		print '   '*depth+"[%s] " % w[0] + ' '.join(w[6:])


def prn_child(pstab, pid, depth):
	for i in range(len(pstab)):
		if pstab[i][0]!=0 and pstab[i][1]==pid: 
			pid = pstab[i][0]
			prn_process(pstab[i], depth)
			pstab[i][0] = 0
			prn_child(pstab, pid, depth+1)


def find_ancestor(pstab, pid):
	while 1:
		i = 0
		for w in pstab:
			if w[0]==pid:
				pid = w[1]
				break
			elif w[0] > pid:
				return i
			i += 1

		if pid != w[1]: return i


def prn_tree(pstab, depth):
	for w in pstab:
		if w[0]==0: continue

		idx = find_ancestor(pstab, w[2])
		if idx >= len(pstab): continue
		prn_process(pstab[idx], depth)

		pid = pstab[idx][0]
		pstab[idx][0] = 0

		prn_child(pstab, pid, depth+1)


def	find_user_process(users):
	ps = os.popen('/usr/bin/ps -ef').readlines()
	pstab = []

	for l in ps:
		## find only user processes, excluding root, or other users
		w = l.split()
		if len(w) < 6: continue
		if users.count(w[0]) == 0: continue
		pstab.append(w[1:])

	pstab.sort()
	prn_tree(pstab, 0)

	

def subtract_list(A, B):
	""" A - B
	"""
	S = A
	for b in B:
		try:
			idx = A.index(b)
		except:
			continue
		else:
			del S[idx]
	return S

def kill_deads(ps):
	ps.sort()

	for i in range( len(ps)):
		print "%-8s [%5d] %s"% (ps[i][0], ps[i][1], ps[i][2])

	print
	for i in range( len(ps)):
		print "%-8s [%5d] %s"% (ps[i][0], ps[i][1], ps[i][2])
		try:
			ans = raw_input("kill process %d [y/n] ? " % ps[i][1])
		except:
			print "\nOkay, you stopped me..."
			return
		else:
			if ans=='y':
				#print "/bin/kill -9 %d" % ps[i][1]
				os.system("/bin/kill -9 %d" % ps[i][1])


SKIP_USER = ['ss7admin', 'altibase', 'webcc']

###################################
if __name__=="__main__":
	
	#users = get_users_in_dir('/home')
	users = get_users_in_passwdfile('/etc/passwd', 101)
	print	"users:", ', '.join( users)
	print
	print	"SKIP_USER:", ', '.join( SKIP_USER)
	print
	users = subtract_list(users, SKIP_USER)

	print	"---> users:", ', '.join( users)
	print
	
	if len(sys.argv) > 1:
		users = [sys.argv[1]]

	find_user_process(users)


