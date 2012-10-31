#!/usr/bin/env python
import ksdMySQL
import rhythmMath
import svg
import math
import cgi

CGIURL = "ksdIntro/demo.py"

def prnListHTML(data):
	print "<UL>"
	for d in data:
		print """<li><a href="/%s?user=%s"> %s </a></li>""" % (CGIURL, d, d)
	print "</UL>"


def prnOneRow(fields):
	print "<tr>"
	color = 0
	for f in fields:
		if color==0:
			cname = "#CDEAEC"
		else:
			cname = "#F8EEE1"
		color = (color+1) % 2

		print "\t<td bgcolor=%s> %s </td>" % (cname, f)
	print "</tr>"

def prnUserList():
	allData = ksdMySQL.loadTable('localhost', 'root', 'wpxk00', 'rhythmpass_web')
	prnListHTML(allData.keys())

def prnUserSelect(users, user=''):
	print """<form action="/%s" method="get">""" % (CGIURL)
	print """<select name="user">"""

	for u in users:
		if u==user:
				print """<option selected="selected" value="%s">%s</option>""" % (u, u)
	
		else:
				print """<option value="%s">%s</option>""" % (u, u)

	print """</select>"""
	print """<input type="submit" value="Submit" />"""
	print """</form>"""

def getKSDinfo(user, vectors):
	
	model = rhythmMath.ksdModel(vectors)
	ratios = model.getRatios()
	rr = rhythmMath.myList(ratios)

	res = []
	#res.append(user)
	res.append("""<a href="/%s?user=%s"> %s </a>""" % (CGIURL, user, user))
	res.append("%.1f" % model.avgDistToCenter)
	res.append( rhythmMath.vecToStr(ratios) )
	res.append("%.1f" % rr.deviation)
	res.append("%.1f" % model.centerSize)
	res.append( rhythmMath.vecToStr(model.centerVec) )
	return res

##
def prnUserAll():
	columnTitle = ["User", "Avg. Dist. to P", "Di. i=1~5", "Devi. of Di", "|P|", "P"       ]
	allData = ksdMySQL.loadTable('localhost', 'root', 'wpxk00', 'rhythmpass_web')
	print """<table>"""
	prnOneRow(columnTitle)
	for user, vectors in allData.iteritems():
		res = getKSDinfo(user, vectors)
		prnOneRow(res)
	print """</table>"""
		


def getRatiosToAvg(user, debug=0):
	allData = ksdMySQL.loadTable('localhost', 'root', 'wpxk00', 'rhythmpass_web')
	vectors = allData[user]
	prnUserSelect(allData.keys(), user)

	if len(vectors) < 1:
		print "NO data for", user
		return

	model = rhythmMath.ksdModel(vectors)
	ratios = model.getRatios()
	return ratios, model.avgDistToCenter

	
def getCoordinations(ratios, radius):
	points = []
	angleStep = 360 / len(ratios)
	angle = angleStep/2
	for ratio in ratios:
			angleRad = math.radians(angle)
			x = math.cos(angleRad) * radius * ratio
			y = math.sin(angleRad) * radius * ratio
			angle += angleStep
			points.append( (x,y) )
	return points

	
	
def drawAxis(s):
	line = svg.Line( (s.width/2, 0), (s.width/2, s.height) )
	s.add(line)

	line = svg.Line( (0, s.height/2), (s.width, s.height/2) )
	s.add(line)

	
def draw(name, size, radius, points, avgDist):
	scene = svg.Scene(name, size, size)
	drawAxis(scene)
	scene.add(svg.Circle((scene.width/2 , scene.height/2), radius*2.0, (245,245,200))) 
	scene.add(svg.Circle((scene.width/2 , scene.height/2), radius*1.5, (230,230,150))) 
	scene.add(svg.Circle((scene.width/2 , scene.height/2), radius, (215,215,100))) 

	i=0
	for x,y in points:
			i += 1
			scene.add(svg.Circle((x + scene.width/2 , y + scene.height/2),3,(200-40*i,200-40*i,200-40*i)))

	scene.add(svg.Text((30,30),"%s's KeyStroke Dynamics. R=%.1f" % (name, avgDist), 14))
	try:
		scene.write_svg()
	except:
		pass
	#scene.make_jpeg()
	scene.print_html_embed()
	#scene.print_html()
	#scene.display()


def getUserName():
	forms = cgi.FieldStorage()
	if len(forms)==0: return ''

	try:
		user = forms['user'].value.strip()
	except:
		user = ''
	return user

def displaySVG(username, size):
	radius = size/6
	ratios, avgDist = getRatiosToAvg(username)
	points = getCoordinations(ratios, radius)
	draw(username, size, radius, points, avgDist)


if __name__ == "__main__":
	print 'Content-Type: text/html\n'
	print """<html> <head> </head> <body> """

	username = getUserName()
	if username=='': 
		prnUserAll()
		displaySVG("handol", 400)
	else:
		displaySVG(username, 400)

	print """</body> </html> """

