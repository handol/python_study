import math
import sys
R = 6378137.0 # meter
degreeToMeter = (R * math.pi / 180)


##
def earthDist(x1, y1, x2, y2):
	# x = longitude
	# y = latitude
	
	dX = abs(x1-x2) * math.cos(y1)
	dY = abs(y1-y2)
	z = math.sqrt(dX*dX + dY*dY)
	dist = z * degreeToMeter
	print "dist=", dist


earthDist(127.1, 36.7, 127.2, 36.8)
earthDist(127.11, 36.71, 127.12, 36.72)
	
def earthDist2(dX, dY, midY):
	dX = dX * math.cos(midY)
	z = math.sqrt(dX*dX + dY*dY)
	dist = z * degreeToMeter
	print "dist=", dist

	

koreaX1 = 125 + (4/60.0)  # 125:04
koreaX2 = 131 + (52/60.0)  # 125:04
koreaY1 = 33 + (06/60.0)  # 125:04
koreaY2 = 38 + (27/60.0)  # 125:04
invalid = -1
class KoreaGrid:
	def __init__(self, columns, rows):
		self.numCols = columns
		self.numRows = rows
		self.stepX = (koreaX2 - koreaX1) / columns
		self.stepY = (koreaY2 - koreaY1) / rows
		self.maxRoomId = rows * columns - 1
		self.roomRadius = earthDist2(self.stepX, self.stepY, koreaY2)

	def info(self):
		print "stepX=", self.stepX
		print "stepY=", self.stepY
		print "numRows=", self.numRows
		print "numCols=", self.numCols

	def getRoomId(self, x, y):
		if x < koreaX1 or x > koreaX2 or y < koreaY1 or y > koreaY2:
			return invalid
			
		col = (x - koreaX1) / self.stepX
		col = int(col)
		row = (koreaY2 - y) / self.stepY
		row = int(row)

		id = row * self.numCols + col
		print "x,y=",x,y,"\tid=", id
		return id
		

	def getNeighborRooms(self, room):
		neighbors = []
		neighbors.append(room-self.numCols-1)
		neighbors.append(room-self.numCols)
		neighbors.append(room-self.numCols+1)
		neighbors.append(room-1)
		neighbors.append(room)
		neighbors.append(room+1)
		neighbors.append(room+self.numCols-1)
		neighbors.append(room+self.numCols)
		neighbors.append(room+self.numCols+1)
		
		if room % self.numCols == 0:
			neighbors[0] = -1
			neighbors[3] = -1
			neighbors[6] = -1

		if (room+1) % self.numCols == 0:
			neighbors[2] = -1
			neighbors[5] = -1
			neighbors[8] = -1

		for i in range(9):
			if neighbors[i] > self.maxRoomId or neighbors[i] < 0:
				neighbors[i] = -1 

		print
		for i in range(3):
			print "[%d] [%d] [%d]" % \
			 (neighbors[i*3], neighbors[i*3+1], neighbors[i*3+2])
		



grid = KoreaGrid(150, 200)
grid.info()
grid.getRoomId(127.5, 36.5)
grid.getRoomId(127.5, 36.6)
grid.getRoomId(127.6, 36.6)
grid.getNeighborRooms(0)
grid.getNeighborRooms(149)
grid.getNeighborRooms(150)
grid.getNeighborRooms(301)

