import sgmlop
import urllib

class anchor_parser:
	# sgmlop parser target
	def __init__(self):
		self.anchors = []
	def finish_starttag(self, tag, attrs):
		if tag == "a":
			for k, v in attrs:
				if k == "href":
					self.anchors.append(v)

def sgmlop_parse(target, data):
	# helper to feed events into a target
	parser = sgmlop.SGMLParser()
	parser.register(target)
	parser.feed(data)
	parser.close() # we're done
	return target

def getpage(page):
	# helper to fetch an entire web page
	if page.startswith("http://"):
		return urllib.urlopen(page).read()
	else:
		return urllib.urlopen("http://"+page).read()

def getanchors(page):
	parser = sgmlop_parse(anchor_parser(), getpage(page))
	print "parser.anchors =", id(parser.anchors)
	return parser.anchors

def help():
	print "-u url"
	print "-f file"
	sys.exit(0)

if __name__ == "__main__":
	import sys
	if len(sys.argv) >= 3 :
		if sys.argv[1]=='-f':
			parser = sgmlop_parse(anchor_parser(), open(sys.argv[2]).read() )	
		elif sys.argv[1]=='-u':
			parser = sgmlop_parse(anchor_parser(), getpage(sys.argv[2]) )	
		else:
			help()
	else:
		help()

for l in parser.anchors:
	print "\t", l
