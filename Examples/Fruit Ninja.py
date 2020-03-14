import time
import random
import sys
engine_path = sys.path[0].replace("Examples", "")
sys.path.append(engine_path)
import Engine as eng

class Slice:
	def __init__(self, mx, my):
		self.list = [[mx, my, del_time]]
	def add(self, x, y):
		self.list.append([x, y, del_time])

class Fruit:
	def __init__(self):
		self.r = random.randint(50, 70)
		self.x = random.randint(self.r, eng.gameSize()[0]-self.r)
		self.y = random.randint(eng.gameSize()[1] + 100, eng.gameSize()[1] + 190)
		self.col = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		self.vel = random.randint(-25, -20)
	def show(self):
		eng.drawEllipse(self.x, self.y, self.r, self.r, self.col)
	def update(self, dt):
		self.vel += 0.3 * dt * 120
		self.y += self.vel * dt * 120
		if (mouseX-self.x)**2 + (mouseY-self.y)**2 < self.r**2:
			p1 = slices[slice_ind].list[len(slices[slice_ind])-1]
			p2 = slices[slice_ind].list[len(slices[slice_ind])-2]
			if (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 < 20**2:
				print("Hit")

eng.createGame("Fruit Ninja", 800, 800, 120)
eng.setIcon(sys.path[0] + "\\fruit_icon.ico")
del_time = 0.1
mouseX, mouseY = (0, 0)
score = 0
slices = []
slice_ind = -1
f = Fruit()

def update(deltaTime):
	global mouseX, mouseY, slices, slice_ind
	mouseX, mouseY = eng.mouseCoords()
	if eng.mousePressed():
		slices[slice_ind].add(mouseX, mouseY)

	eng.drawBg(50, 50, 50)
	f.update(deltaTime)
	f.show()
	for slice in slices:
		for i in range(1, len(slice.list)):
			p1 = slice.list[i]
			p2 = slice.list[i-1]
			eng.drawLine(p1[0], p1[1], p2[0], p2[1], (255, 255, 255, 3))

	for slice in slices:
		for point in slice.list:
			point[2] -= deltaTime
			if point[2] < 0:
				slice.list.remove(point)

def mouseClicked():
	global slices, slice_ind
	slice_ind += 1
	slices.append(Slice(mouseX, mouseY))

def mouseReleased():
	pass

eng.update = update
eng.mouseClicked = mouseClicked
eng.mouseReleased = mouseReleased
eng.run()