#!/usr/bin/env python
# $Id: sitesync.py,v 1.12 2002/11/05 20:41:35 shaggy Exp $

"""
Synchronize remote ftp server/servers with a local directory by
uploading only files that are modified since last time (according to
a saved timestamp)

Multiple servers with different content are supported

usage sitesync [OPTIONS]
Where OPTIONS is one or more of the following

-l, --list: list files that need to be updated
-a, --add: add a host(server) to be handled
-s, --set-uploaded: set all files to uploaded state
-f, --force: upload non-modified files too
-ff: upload all files, including the ones that normally should be ignored
-h, --help: print this help
-v, --verbose: print verbose messages, currently prints files that do not need uploading
-vv: print ftp debugging info
-vvv: print lots of ftp debugging info

Copyright (c) 2002 by Martin Tsachev. All rights reserved.
mailto:martin@f2o.org
http://martin.f2o.org

Redistribution and use in source and binary forms,
with or without modification, are permitted provided
that the conditions available at
http://www.opensource.org/licenses/bsd-license.html
are met.

"""

import sys, os, getopt, ConfigParser, ftplib, string

config = 0
config_root = os.getenv('HOME') or ''
config_file = config_root + '/.sitesyncrc'
netrc_file = config_root + '/.netrc'
verbose = 0
force = 0


#class File :
#	def __init__(self, file, mtime, action)  :
#		self.file = file
#		self.mtime = mtime
#		self.action = action


class Host :

	def __init__(self, host, config) :
		self.host = host
		self.config = config
		self.root = ''

		self.pasv = self.config.getboolean(host, 'pasv')
		self.remote_dir = self.config.get(host, 'remote_dir')
		self.ignore = eval(self.config.get(host, 'ignore'))
		locals = eval(self.config.get(host, 'local_dir'))
		self.local_dir = list2dir(locals)
		self.mtimes = eval(self.config.get(host, 'mtimes'))
		self.files = eval(self.config.get(host, 'files'))

		if not self.check(locals) :
			return

		new_files = recurse_list(self.local_dir, '', [])
		for i in range(0, len(new_files)) :
			if new_files[i] not in self.files :
				print 'Adding', new_files[i]
				self.files.append(new_files[i])
				self.mtimes.append(0)
		self.config_update()


	def check(self, dir = '') :
		"""Checks if the host definitions is OK."""
		if not self.local_dir and dir :
			print self.host + ':', dir, 'is/are not accessible\n'
			return 0
		elif not self.local_dir :
			return 0
		else :
			return 1

	def list(self) :
		"""Print a list of files that need to be uploaded or deleted from the host."""

		if not self.check() :
			return

		action, upload, delete, ignore = self.get_action()
		if not self.host_info(upload, delete, ignore) :
			return
		for i in range(0, len(self.files)) :
			if action[i] == 'u' :
				print 'U', self.files[i]
			elif action[i] == 'd' :
				print 'D', self.files[i]
			elif verbose :
				print 'N', self.files[i]


	def set_uploaded(self) :
		"""Set all files to an uploaded state."""

		if not self.check() :
			return

		mtimes = []
		for i in range(0, len(self.files)) :
			try :
				mtimes.append(os.path.getmtime(self.local_dir + self.files[i]))
			except OSError :
				mtimes.append(0)
		self.mtimes = mtimes
		self.config_update()


	def upload(self) :
		"""Handle uploading the files."""

		if not self.check() :
			return

		action, upload, delete, ignore = self.get_action()
		if not self.host_info(upload, delete, ignore) :
			return

		if not self.ftp_connect() :
			return

		self.change_dir(self.remote_dir)
		self.root = self.ftp.pwd()

		if verbose :
			self.ftp.set_debuglevel(verbose-1)
		olddir = '.'

		for i in range(0, len(self.files)) :
			file = self.files[i]
			arr = file.split('/')
			filename = arr.pop()
			dir = ''
			while len(arr) :
				dir += arr.pop(0) + '/'

			if action[i] == 'u' :
				if dir != olddir :
					self.change_dir(dir)
					olddir = dir
				print 'Uploading', file
				try :
					self.ftp.storbinary('STOR ' + filename, open(self.local_dir + file, 'r'))
					self.mtimes[i] = os.path.getmtime(self.local_dir + file)
				except :
					print 'Could not upload', file
					self.config_update()

			elif action[i] == 'd' :
				print 'Deleting', file
				self.change_dir(dir)
				try :
					self.ftp.delete(filename)
					self.mtimes[i] = -1
				except :
					print 'Could not delete', file
					self.config_update()

			elif verbose :
				print self.files[i], 'does not need uploading'
		self.ftp.quit()
		self.config_update()


	def ftp_connect(self) :
		"""Connect to a FTP server."""
		from socket import error

		try :
			self.ftp = ftplib.FTP(self.host)
		except error :
			print 'Cannot connect to', self.host
			return 0

		user, passwd = get_login_info(self.host)
		try :
			self.ftp.login(user, passwd)
		except ftplib.error_perm :
			print 'Authentication failed'
			return 0

		if verbose :
			print 'Logged in'
		self.ftp.set_pasv(self.pasv)
		return 1


	def change_dir(self, dir) :
		"""Change to a specified FTP directory, creates it if the diretory doesn't exists."""

		if dir and dir[0] == '/' :
			dir = dir[1:]

		try :
			self.ftp.cwd(self.root + dir)
		except ftplib.error_perm :
			self.ftp.cwd(self.root)
			arr = dir.split('/')
			arr.pop()
			while len(arr) :
				dir = arr.pop(0)
				try :
					self.ftp.cwd(dir)
				except ftplib.error_perm :
					try :
						self.ftp.mkd(dir)
						self.ftp.cwd(dir)
					except ftplib.error_perm :
						print 'Cannot create', dir, 'in', self.ftp.pwd()


	def get_action(self) :
		"""Evaluate what action to take for every file, reorder files for uploading first."""

		action = []
		ord_files = []
		ord_mtimes = []
		for i in range(0, len(self.files)) :
			for j in range(0, len(self.ignore)) :
				if force < 2 and self.files[i].find(self.ignore[j]) >= 0:
					ord_files.append(self.files[i])
					ord_mtimes.append(self.mtimes[i])
					action.append('i')
					break
			else :
				try :
					mtime = os.path.getmtime(self.local_dir + self.files[i])
				except OSError :
					ord_files.append(self.files[i])
					ord_mtimes.append(self.mtimes[i])
					action.append('d')
				else :
					if force or int(self.mtimes[i]) < mtime :
						ord_files.insert(0, self.files[i])
						ord_mtimes.insert(0, self.mtimes[i])
						action.insert(0, 'u')
					else :
						ord_files.append(self.files[i])
						ord_mtimes.append(self.mtimes[i])
						action.append('n')

		self.files = ord_files
		self.mtimes = ord_mtimes
		return action, action.count('u'), action.count('d'), action.count('i')


	def host_info(self, upload, delete, ignore) :
		"""Print the count of files to upload/delete for the host."""

		print '\n', self.host + ':', len(self.files), 'files,',\
		upload, 'for uploading,', delete, 'for deleting,', ignore, 'ignored'

		if upload == 0 and delete == 0 :
			return 0
		else :
			return 1


	def config_update(self) :
		"""Write current configuration to the rc file."""
		config_set_files(self.config, self.host, self.files, self.mtimes)

	#  End of class Host
	# # # # # # # # # #


def get_line(prompt, optional = 0) :
	"""Reads a line of user input."""

	try :
		while 1 :
			line = raw_input(prompt + ': ')
			if line or optional :
				return line
	except EOFError :
		return ''


# always send reldir and files, they are cached between calls otherwise
def recurse_list(basedir, reldir, files) :
	"""Return a list of the files in a directory or its subdirectories."""

	listing = os.listdir(basedir + reldir)
	for file in listing:
		dir = os.path.isdir(basedir + reldir + file)
		if dir :
			recurse_list(basedir, reldir + file + '/', files)
		else :
			files.append(reldir + file)
	return files


def list2dir(list) :
	"""Return the first directory that exists from a list."""

	local_dir = ''
	for dir in list :
		if os.path.isdir(dir) :
			local_dir = dir
			break
	return local_dir


def netrc_addhost(host) :
	"""Add an entry to a netrc file."""
	import getpass

	user = get_line('Username')
	passwd = getpass.getpass()
	host_entry = '\nmachine ' + host + ' login ' + user + ' password ' + passwd + '\n'

	file = open(netrc_file, 'a')
	file.write(host_entry)
	file.close()
	return user, passwd


def get_login_info(host) :
	"""Get login credentials for a host - from netrc or user input."""
	import netrc

	try :
		login_info = netrc.netrc(netrc_file)
	except IOError :
		user, passwd = netrc_addhost(host)
		return user, passwd
	try :
		user, account, passwd = login_info.authenticators(host)
	except TypeError :
		user, passwd = netrc_addhost(host)
	return user, passwd


def config_set_files(config, host, files, mtimes) :
	"""Write the updated files and modification times for the host."""

	i = 0
	for mtime in mtimes :
		if ( int(mtime) == -1 ) :
			mtimes.pop(i)
			files.pop(i)
		i += 1
	for i in range(0, len(files)) :
		mtimes[i] = str(mtimes[i])
	config.set(host, 'mtimes', mtimes)
	config.set(host, 'files', files)
	config.write(open(config_file, 'w'))


def add_host() :
	"""Add a host to the rc file."""

	host = get_line('Hostname')
	get_login_info(host)
	pasv = int(get_line('Passive[0/1]'))
	remote_dir = get_line('Remote directory')
	if remote_dir[-1] != '/':
		remote_dir += '/'

	local = []
	i = 1
	print 'Enter the alternative directories to read files from, end with an empty entry'
	while 1 :
		dir = get_line('Local directory ' + str(i), 1)
		if len(dir) > 0 :
			if dir[-1] != '/':
				dir += '/'
			local.append(dir)
			i += 1
		elif len(local) :
			break
	dir = list2dir(local)
	files = recurse_list(dir, '', [])
	print len(files), 'files found'
	mtimes = []
	for i in range(0, len(files)) :
		mtimes.append(0)

	ignore = get_line('Ignore')

	config = ConfigParser.ConfigParser()
	config.read(config_file)
	try :
		config.add_section(host)
	except ConfigParser.DuplicateSectionError :
		print host, 'is already defined'
		sys.exit(1)
	config.set(host, 'pasv', pasv)
	config.set(host, 'remote_dir', remote_dir)
	config.set(host, 'local_dir', local)
	config.set(host, 'ignore', ignore)
	config_set_files(config, host, files, mtimes)


def iterate_hosts(action) :
	"""Execute the specified action on all hosts."""
	global config

	if action == 'list' :
		action = 'site.list()'
	elif action == 'upload' :
		action = 'site.upload()'
	elif action == 'set-uploaded' :
		action = 'site.set_uploaded()'
	else :
		print 'Error\n'
		return

	config = ConfigParser.ConfigParser()
	config.read(config_file)

	for host in config.sections() :
		site = Host(host, config)
		eval(action)


def usage() :
	print __doc__


def main() :
	global verbose, force

	if not os.path.isfile(config_file) :
		print 'Configuration file', config_file, 'not found'
		print 'Please run with -a to add a host first\n'

	try :
		opts, args = getopt.getopt(sys.argv[1:], 'hvalsf',
		['help', 'verbose', 'add', 'list', 'set-uploaded', 'force'])
	except getopt.GetoptError :
		usage()
		sys.exit(1)

	action = 'usage'
	for o, a in opts :
		if o in ('-h', '--help') :
			action = 'help'
		elif o in ('-v', '--verbose') :
			verbose += 1
		elif o in ('-l', '--list') :
			action = 'list'
		elif o in ('-a', '--add') :
			action = 'add'
		elif o in ('-s', '--set-uploaded') :
			action = 'set-uploaded'
		elif o in ('-f', '--force') :
			force += 1

	if action == 'list' :
		iterate_hosts(action)
	elif action == 'add' :
		add_host()
	elif action == 'set-uploaded' :
		iterate_hosts(action)
	elif action == 'help' :
		usage()
	else :
		iterate_hosts('upload')

main()
