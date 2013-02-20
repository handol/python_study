#!/usr/bin/env python
import sys, os
#print os.getcwd()
a = "~/dev/hlrsvc/HLRSVC/src/slp/gsm/slp_code_sri_gsm.c"
b = "/home/dahee/CVS/HLRSVC/src/slp/gsm/slp_code_sri_gsm_utils.c"
#res = os.system("diff "+a + " " + b)
#res = os.system("diff "+a + " " + b + " | wc -l")
#res = os.system("diff %(a)s %(b)s | wc -l " % vars())
#print "res1 = " +str(res)

cmd = 'find bin -name "*.py" -print'
cmd = '/bin/ls'
cmd = "diff a b | wc"
cmd = "diff %s %s | wc -l " %(a, b)
print "cmd= ", cmd
line = os.popen(cmd).readline()
lines = os.popen("diff %(a)s %(b)s  " % vars()).readlines()
for line in lines:
	print line
w = line.split()
print "line=%s, w[0]=%s"  %(line, w[0])

if (w[0]=="0") :
	print "zero"
else :
	print "nonzero"

if (os.system("diff a b | wc")==0) :
	print "ok"
else :
	print "no"

sys.exit()
#print res
#print str(res)
