#!/usr/bin/env python
# -*- coding: EUC-KR -*-
# http://diveintopython.org/xml_processing/unicode.html -- python�� unicode, encoding
import sys
import os

HanFirstSound = [
	" ", " ", "��", "��", "��", "��", "��", "��", "��", 
	"��", "��", "��", "��", " ", "��", "��", "��", "��", "��", "��", "��",
	" "," "," "," "," "," "," "," "," "," "," " ]

HanMiddleSound = [
	" "," "," ", "��", "��", "��", "��", "��", 
	" ", " ", "��", "��", "��", "��", "��", "��", 
	" ", " ", "��", "��","��", "��", "��", "��", 
	" ", " ", "��", "��", "��", "��",
       	" ", " " ]

HanLastSound = [
	" ", " ", "��", "��", "��", "��", "��", "��", "��", "��", 
	"��", "��", "��", "��", "��", "��", "��",
	"��", " ", "��", "��", "��", "��", "��", "��", "��",
	"��", "��", "��", "��", " ", " " ]

def johab_jaso(johabcode):
	f = (johabcode & 0x7C00) >> 10
	m = (johabcode & 0x03E0) >> 5
	l = (johabcode & 0x001F)
	return (f,m,l)

def johapcode_file(file):
	fd = open(file)
	c1 = 0xB0
	c2 = 0xA1
	for line in fd.readlines():
		if len(line) < 2: continue

		#print "%d" % ord(line[-1])
		#hexstr = map(hex, map(ord, line[:2]) )
		#print hexstr
		#print " ".join(hexstr)
		uint2 = (ord(line[0]) << 8) + ord(line[1])
		jaso = johab_jaso(uint2)
		print "%c%c %04X" % (c1, c2, uint2), "%02d %02d %02d" % jaso, \
			HanFirstSound[jaso[0]], HanMiddleSound[jaso[1]], HanLastSound[jaso[2]]

		#print "%04X" % (uint2), "%02d %02d %02d" % johab_jaso(uint2)
		c2 = c2 + 1
		if c2 > 0xFE:
			c2 = 0xA1
			c1 = c1 + 1
		
if __name__=='__main__':
	if len(sys.argv) > 1:
		johapcode_file(sys.argv[1])