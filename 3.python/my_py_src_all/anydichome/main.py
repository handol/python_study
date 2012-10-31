#!/usr/bin/env python
import ksdMySQL
import rhythmMath
import svg
import math
import cgi


def doit(user, debug=0):
	allData = ksdMySQL.loadTable('localhost', 'root', 'wpxk00', 'rhythmpass_web')
	vectors = allData[user]

	if len(vectors) < 1:
		print "NO data for", user
		return

	model = rhythmMath.ksdModel(vectors)
	ratios = []
	for v in vectors:
		ratios.append(model.ratioToAvg(v))

	if debug: print ratios
	return ratios

	
	
	
def drawAxis(s):
	line = svg.Line( (s.width/2, 0), (s.width/2, s.height) )
	s.add(line)

	line = svg.Line( (0, s.height/2), (s.width, s.height/2) )
	s.add(line)

	
def draw(name, values):
	scene = svg.Scene(name, 400, 400)
	drawAxis(scene)
	scene.add(svg.Circle((scene.width/2 , scene.height/2), scene.width/5, (200,200,200))) 

	i=0
	angleStep = 360 / len(values)
	angle = angleStep/2
	for v in values:
			i += 1
			angleRad = math.radians(angle)
			x = math.cos(angleRad) * (scene.width/5) * v
			y = math.sin(angleRad) * (scene.width/5) * v
			scene.add(svg.Circle((x + scene.width/2 , y + scene.height/2),3,(200-40*i,200-40*i,200-40*i)))
			angle += angleStep

	scene.add(svg.Text((30,30),"%s's KeyStroke Dynamics " % (name), 14))
	scene.write_svg()
	scene.make_jpeg()
	#scene.print_html_embed()
	scene.print_html()
	#scene.display()


def getUserName():
	forms = cgi.FieldStorage()
	if len(forms)==0: return ''

	try:
		user = forms['user'].value.strip()
	except:
		user = ''
	return user

if __name__ == "__main__":
	username = getUserName()
	if username=='': username = 'handol'

	print 'Content-Type: text/html\n'
	ratios = doit(username)
	draw(username, ratios)

