import feedparser

def dict_print(d):
	for (k,v) in d.iteritems():
		print "%s\t%s" % (k, v )


def test_parser(url="http://feedparser.org/docs/examples/atom10.xml"):
	d = feedparser.parse(url)
	#print d
	#dict_print(d['feed'])
	dict_print(d.feed)
	print "Title: ", d.feed.title
	print "Link : ", d.feed.link
	#print "Lang : ", d.feed.language
	#print "Encoding : ", d.feed.encoding
	i=0
	for e in d.entries:
		i += 1
		#dict_print(e)
		print "%2d\t%s" % (i, e.title)
		#print e.category
		#print " , ".join(e.category)



if __name__=="__main__":
	import sys
	if len(sys.argv) > 1:
		test_parser(sys.argv[1])
	else:
		test_parser()
