#!/usr/bin/env python
"""\
SVG.py - Construct/display SVG scenes.

The following code is a lightweight wrapper around SVG files. The metaphor
is to construct a scene, add objects to it, and then write it to a file
to display it.

This program uses ImageMagick to display the SVG files. ImageMagick also 
does a remarkable job of converting SVG files into other formats.

=== http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/325823
"""

import os
display_prog = 'display' # Command to execute to display images.
	  
class Scene:
	def __init__(self,name="svg",height=400,width=400):
		self.name = name
		self.items = []
		self.height = height
		self.width = width
		return

	def add(self,item): self.items.append(item)

	def strarray(self):
		var = ["<?xml version=\"1.0\"?>\n",
			   """
	<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
		"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n """,	
			   """
	<svg height=\"%d\" width=\"%d\"
		xmlns="http://www.w3.org/2000/svg" version="1.1"
		xmlns:xlink="http://www.w3.org/1999/xlink" >\n """ % (self.height,self.width),

			   " <g style=\"fill-opacity:1.0; stroke:black;\n",
			   "  stroke-width:1;\">\n"]
		for item in self.items: var += item.strarray()			
		var += [" </g>\n</svg>\n"]
		return var

	def write_svg(self,filename=None):
		if filename:
			self.svgname = filename
		else:
			self.svgname = self.name + ".svg"
		file = open(self.svgname,'w')
		file.writelines(self.strarray())
		file.close()
		return
	
	def make_jpeg(self):
		## 'convert' tool is from ImageMagicK
		convname = self.svgname.replace(".svg", ".jpg")
		try:
			os.system("convert %s %s" % (self.svgname, convname))
		except:
			pass

	def print_html_embed(self):
		## uses 'embed' tag. working on IE.  Not in HTML spec.
		print """
			<embed src="%s" width="%d" height="%d"
				type="image/svg+xml"
				wmode="transparent"
				pluginspage="http://www.adobe.com/svg/viewer/install/" />
			"""	 % (self.svgname, self.width, self.height)
		return

	def print_html_object(self):
		## uses 'object' tag. Not working on IE.  HTML4 spec.
		
		print """<object classid="clsid:377B5106-3B4E-4A2D-8520-8767590CAC86" id="SVGCtl1" width="%d" height="%d">
	<param name="INTERNALID" value="6dab35f7a8db2142b33b614be2eda8fd00000000">
	<param name="DefaultFontFamily" value="Gulim">
	<param name="DefaultFontSize" value="Gulim">
	<param name="DefaultAntialias" value="Gulim">
	<param name="SRC" value="http://anydic.com/%s">
	<param name="WMODE" value="window">
	<param name="FULLSCREEN" value="no">
	<table width='100%%' cellpadding='0' cellspacing='0' border='0' height='8'><tr><td bgColor='#336699' height='25' width='10%%'>&nbsp;</td><td bgColor='#666666'width='85%%'><font face='Gulim' color='white' size='4'><b>&nbsp; You need a SVG viewer to view this page. Please download Adobe viewer by clicking and install it.</b></font></td></tr><tr><td bgColor='#cccccc' width='15'>&nbsp;</td><td bgColor='#cccccc' width='500px'><br> <font face='Gulim' size='2'>.<p align='center'> <a href='http://download.adobe.com/pub/adobe/magic/svgviewer/win/3.x/3.03/ko/SVGView.exe'>Download Adobe SVG viewer</a>.</p></font><p><font face='Gulim' size='2'></p><p align='center'><a href='http://download.adobe.com/pub/adobe/magic/svgviewer/win/3.x/3.03/ko/SVGView.exe'> .</a>.</font><br>&nbsp;</td></tr></table> 
</object>"""  % (self.width, self.height, self.svgname)
		return


	def print_html(self):
		## uses 'embed' tag. working on IE.  Not in HTML spec.
		print """<html> <head> </head> <body> """
		self.print_html_embed()
		print """</body> </html> """

	def display(self,prog=display_prog):
		os.system("%s %s" % (prog,self.svgname))
		return		
		

class Line:
	def __init__(self,start,end):
		self.start = start #xy tuple
		self.end = end	 #xy tuple
		return

	def strarray(self):
		return ["  <line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" />\n" %\
				(self.start[0],self.start[1],self.end[0],self.end[1])]


class Circle:
	def __init__(self,center,radius,color):
		self.center = center #xy tuple
		self.radius = radius #xy tuple
		self.color = color   #rgb tuple in range(0,256)
		return

	def strarray(self):
		return ["  <circle cx=\"%d\" cy=\"%d\" r=\"%d\"\n" %\
				(self.center[0],self.center[1],self.radius),
				"	style=\"fill:%s;\"  />\n" % colorstr(self.color)]

class Rectangle:
	def __init__(self,origin,height,width,color):
		self.origin = origin
		self.height = height
		self.width = width
		self.color = color
		return

	def strarray(self):
		return ["  <rect x=\"%d\" y=\"%d\" height=\"%d\"\n" %\
				(self.origin[0],self.origin[1],self.height),
				"	width=\"%d\" style=\"fill:%s;\" />\n" %\
				(self.width,colorstr(self.color))]

class Text:
	def __init__(self,origin,text,size=24):
		self.origin = origin
		self.text = text
		self.size = size
		return

	def strarray(self):
		return ["  <text x=\"%d\" y=\"%d\" font-size=\"%d\">\n" %\
				(self.origin[0],self.origin[1],self.size),
				"   %s\n" % self.text,
				"  </text>\n"]
		
	
def colorstr(rgb): return "#%x%x%x" % (rgb[0]/16,rgb[1]/16,rgb[2]/16)

def test():
	scene = Scene('test2')
	scene.add(Rectangle((100,100),200,200,(0,255,255)))
	scene.add(Line((200,200),(200,300)))
	scene.add(Line((200,200),(300,200)))
	scene.add(Line((200,200),(100,200)))
	scene.add(Line((200,200),(200,100)))
	scene.add(Circle((200,200),30,(0,0,255)))
	scene.add(Circle((200,300),30,(0,255,0)))
	scene.add(Circle((300,200),30,(255,0,0)))
	scene.add(Circle((100,200),30,(255,255,0)))
	scene.add(Circle((200,100),30,(255,0,255)))
	scene.add(Text((50,50),"Testing SVG"))
	scene.write_svg()
	scene.make_jpeg()
	scene.print_html_embed()
	#scene.display()
	return

if __name__ == '__main__': test()
