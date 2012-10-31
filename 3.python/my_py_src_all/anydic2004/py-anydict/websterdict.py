#!/usr/bin/env python
# -*- coding: EUC-KR -*-

def make_tab(expl):
	p1 = expl.find('<I>')
	p2 = expl.find('</I>')
	if p1==-1: return '',''
	if p2==-1: return '',''

	poomsa = expl[p1+3:p2]
	poomsa = poomsa.replace('.', '')
	poomsa = poomsa.replace('v t', 'vt')
	poomsa = poomsa.replace('v i', 'vi')
	poomsa = poomsa.replace('p p', 'pp')
	explnew = expl[p2+6:]	

	if poomsa != '':
		res = """<tr><td width=20 class="pm" valign="top">%s</td>\n<td class="xp" valign="top">%s</td></tr>""" % (poomsa, explnew)
	else:
		res = """<tr><td></td>\n<td class="xp" valign="top">%s</td></tr>""" % (explnew)
	return res


def proc_webster(dictfile, out=None):
	cnt = 0

	try:
		fd = open(dictfile)
	except:
		print "read fail:", dictfile
		return
	
	html = fd.read()

	ptr = 0
	prev = ''
	while 1:
		p1 = html.find('<P>', ptr)
		if p1==-1: break
		p2 = html.find('</P>', p1)
		if p2==-1: break

		p3 = html.find('<B>',ptr)
		if p3==-1: break
		p4 = html.find('</B>',ptr)

		ptr = p4+4

		w = html[p3+3:p4]
		if html[p4+4].isspace():
			expl = html[p4+5:p2]
		else:
			expl = html[p4+4:p2]
	
		if out != None: 
			if w != prev:
				if prev != '': out.write('</TABLE>\n\n')
				out.write(w)
				out.write('\n<TABLE>')
				prev = w
			out.write( make_tab(expl) )
			out.write('\n')

		cnt += 1
	
	print "Total:", cnt
	return cnt

def proc_all():
	all = range(ord('a'), ord('z')+1)
	all = map(chr, all) + ['new']
	total = 0
	for c in all:
		infile = '/data1/AD/data/v003/wb1913_%s.html' % c
		outfile = '/data1/AD/data/webster/%s.html' % c
		print infile, outfile
		try:
			out = open(outfile, "w")
		except:
			print "cannot write:", outfile
			continue
			
		total += proc_webster(infile, out)
		out.close()

	print "### total = %d" % total

if __name__ == "__main__":
	import time
	import sys

	t = time.time()

	out = None
	if len(sys.argv) > 1 and sys.argv[1]=="all":
		proc_all()

	elif len(sys.argv) > 1:
		try:
			out = open(sys.argv[1], "w")
		except:
			print "cannot write:", sys.argv[1]
	
		proc_webster('/data1/AD/data/v003/wb1913_a.html', out)

	print "WordNet %.3f" % (time.time()-t)


