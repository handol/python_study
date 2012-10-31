#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs

class filestore:
	def __init__(self, fname):
		self.fname = fname

	# load the first line
	def load(self):
		try:
			f = codecs.open(self.fname, "r", "utf-8")
			line = f.readline()
			line = line.strip()
			f.close()
			return line
		except:
			return ""

	def load_int(self):
		line = self.load()
		try:
			return int(line)
		except:
			return 0

	# save to file
	def save(self, line):
		line = str(line)
		try:
			f = codecs.open(self.fname, "w", "utf-8")
			f.write("%s\n" % line)
			f.close()
		except:
			return ""
