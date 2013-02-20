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


def has_child(pstab, pid):
	# check if 'pid' has any child
	for w in pstab:
		if w[2]==pid and  w[5]!='?' and w[6]!='?': return 1
		#if w[2]==pid: return 1
	return 0

def has_parent(pstab, ppid):
	# check if 'ppid' is found 
	for w in pstab:
		if w[1]==ppid and  w[5]!='?' and w[6]!='?': return 1
		#if w[1]==ppid: return 1
	return 0

def process_hjerarchy(pstab):
	tree = []
	for w in pstab:
		tree.append([ w[1], w[2] ])
	tree.sort()

def find_ancestor(tree, pid):
	while 1:
		for t in tree:
			if t[0]==pid:
				pid = t[1]
				break
			elif t[0] > pid:
				return pid

		if pid != t[1]: return pid

def	find_dead_user_process(users):
	ps = os.popen('/usr/bin/ps -ef').readlines()
	pstab = []

	for l in ps:
		## find only user processes, excluding root, or other users
		w = l.split()
		if len(w) < 6: continue
		if users.count(w[0]) == 0: continue
		pstab.append(w)


	deadps=[]

	for w in pstab:
		## find dead process with no child
		if has_child(pstab, w[1]): continue
		if has_parent(pstab, w[2]): continue
		if w[2]!='1' and (w[5]!='?' and w[6]!='?'):
			continue

		deadps.append( [w[0], int(w[1]), ' '.join(w[7:]) ] )
	
	return deadps


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

	ps = find_dead_user_process(users)

	print "---> Found %d dead processes of users\n" % len(ps)

	kill_deads(ps)

