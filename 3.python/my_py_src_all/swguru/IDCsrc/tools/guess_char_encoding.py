### handol@gmail.com  2007-8-13
### testing the library: chardet
### url of chardet: http://chardet.feedparser.org/

import chardet

if __name__ == "__main__":
	import sys
	if len(sys.argv) < 2:
		print "# usage: input_file"
		sys.exit()

	try:
		fp = open(sys.argv[1])
	except:
		print "fail to read the file: ", sys.argv[1]
		sys.exit()


	contents = fp.read()
	fp.close()
	res = chardet.detect(contents)
#print "#", res
	print res['encoding']
