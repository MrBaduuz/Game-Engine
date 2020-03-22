import pygame as pg
import math
import random
pgScreen = None
pgClock = None
pgFrameRate = 0
pgRunning = False

class Image:
    def __init__(self, path):
        self.img = pg.image.load(path)

class Sound:
    def __init__(self, path):
        self.sound = pg.mixer.Sound(path)

class Vector:
	def __init__(self, *coords):
		self.x = 0
		self.y = 0
		self.z = 0
		if len(coords) == 3:
			self.x = coords[0]
			self.y = coords[1]
			self.z = coords[2]
		elif len(coords) == 2:
			self.x = coords[0]
			self.y = coords[1]
		elif len(coords) == 1:
			self.x = math.cos(coords[0] * (math.pi/180))
			self.y = math.sin(coords[0] * (math.pi/180))
	def mag(self):
		return math.sqrt(self.x**2 + self.y**2 +self.z**2)
	def magSq(self):
		return self.x**2 + self.y**2 +self.z**2
	def setMag(self, mg):
		self.x *= mg/self.mag()
		self.y *= mg/self.mag()
		self.z *= mg/self.mag()
	def limit(self, mg):
		if self.mag() > mg:
			self.setMag(mg)

	def __add__(self, oth):
		x = self.x + oth.x
		y = self.y + oth.y
		z = self.z + oth.z
		return Vector(x, y, z)
	def __sub__(self, oth):
		x = self.x - oth.x
		y = self.y - oth.y
		z = self.z - oth.z
		return Vector(x, y, z)
	def __mul__(self, oth):
		if isinstance(oth, self.__class__):
			x = self.x * oth.x
			y = self.y * oth.y
			z = self.z * oth.z
		else:
			x = self.x * oth
			y = self.y * oth
			z = self.z * oth
		return Vector(x, y, z)
	def __truediv__(self, oth):
		x = self.x / oth
		y = self.y / oth
		z = self.z / oth
		return Vector(x, y, z)
	def __rtruediv__(self, oth):
		x = self.x / oth
		y = self.y / oth
		z = self.z / oth
		return Vector(x, y, z)
	def __str__(self):
		return "X:{} Y:{} Z:{}".format(self.x, self.y, self.z)
	def copy(self):
		return Vector(self.x, self.y, self.z)
	def set(self, *coords):
		if len(coords) == 3:
			self.x = coords[0]
			self.y = coords[1]
			self.z = coords[2]
		elif len(coords) == 2:
			self.x = coords[0]
			self.y = coords[1]
		elif len(coords) == 1:
			self.x = math.cos(coords[0] * (math.pi/180))
			self.y = math.sin(coords[0] * (math.pi/180))
	def dist(self, oth):
		return (self-oth).mag()
	def distSq(self, oth):
		return (self-oth).magSq()
	def heading(self):
		return atan2(self.y, self.x) * 180 / math.pi
	def angleBetween(self, oth):
		return abs((self.heading()-oth.heading()))

class Particle:
	def __init__(self, position):
		self.pos = position
		self.vel = Vector(0, 0)
		self.acc = Vector(0, 0)
		self.mass = 1
		self.lifetime = 1
		self.death_speed = 0.001
	def show(self):
		pass
	def physics(self, dt):
		self.vel += self.acc * dt * 60
		self.pos += self.vel * dt * 60
		self.acc.set(0, 0)
		self.lifetime -= self.death_speed * dt * 60
	def update(self, dt):
		pass
	def isDead(self):
		return self.lifetime < 0
	def applyForce(self, f):
		self.acc += f / self.mass
	def applyGravity(self, f):
		self.acc += f

class ParticleSystem:
	def __init__(self, cap, ParticleType, adrate, size):
		self.ps = []
		self.addition_rate = adrate
		self.capacity = cap
		self.ptype = ParticleType
		self.counter = 0
		self.oldest = 0
		self.size = size
		if size <= 0:
			self.size = -2

	def show(self):
		for p in self.ps:
			p.show()
	def update(self, dt):
		self.counter += dt
		self.add()
		for p in self.ps:
			p.update(dt)
			if p.isDead():
				self.ps.remove(p)
	def add(self):
		while self.counter > self.addition_rate:
			self.counter -= self.addition_rate
			if self.size > 0 or self.size == -2:
				self.size -= 1
				if self.size == -3:
					self.size = -2
				if len(self.ps) < self.capacity:
					self.ps.append(self.particle())
				else:
					self.ps[self.oldest] = self.particle()
					self.oldest += 1
					self.oldest %= self.capacity

	def particle(self):
		return self.ptype()


def atan2(y,x):
	return toDegrees((math.atan2(-y, x)))

def toRadians(angle):
	return angle * math.pi/180

def toDegrees(angle):
	return angle * 180/math.pi

def gameSize():
    return pg.display.get_surface().get_size()

def drawPolyRot(cx, cy, lst, angle, *color):
	newList = []
	for i in range(0, len(lst), 2):
		cs = math.cos((270-angle) * math.pi/180)
		sn = math.sin((270-angle) * math.pi/180)
		x = int(lst[i]*cs-lst[i+1]*sn)
		y = int(lst[i]*sn+lst[i+1]*cs)
		newList.append([cx+x, cy+y])
	pg.draw.polygon(pgScreen, color, newList)
def drawPoly(lst, *color):
	newList = []
	for i in range(0, len(lst), 2):
		newList.append([int(lst[i]), int(lst[i+1])])
	pg.draw.polygon(pgScreen, color, newList)

def drawRectRot(x, y, w, h, angle, *color):
	if pgRunning:
		cs = math.cos(-angle * math.pi/180)
		sn = math.sin(-angle * math.pi/180)
		p1 = (int(x+((-w/2)*cs-(-h/2)*sn)), int(y+((-w/2)*sn+(-h/2)*cs)))
		p2 = (int(x+((w/2)*cs-(-h/2)*sn)), int(y+((w/2)*sn+(-h/2)*cs)))
		p3 = (int(x+((w/2)*cs-(h/2)*sn)), int(y+((w/2)*sn+(h/2)*cs)))
		p4 = (int(x+((-w/2)*cs-(h/2)*sn)), int(y+((-w/2)*sn+(h/2)*cs)))
		pointList = (p1, p2, p3, p4)
		pg.draw.polygon(pgScreen, color, pointList)
	else:
		print("Start the Game")

def drawRect(x, y, w, h, *color):
	if pgRunning:
		pg.draw.rect(pgScreen, color, (int(x), int(y), int(w), int(h)))
	else:
		print("Start the Game")

def drawImage(x, y, w, h, image):
    if pgRunning:
        pgScreen.blit(pg.transform.scale(image.img, (int(w), int(h)), (int(x), int(y))))
    else:
        print("Start the Game")

def drawText(text, x, y, scl, *color):
    tFon = pg.font.SysFont("Calibri", scl)
    tSurf = tFon.render(text, True, color)
    tRec = tSurf.get_rect()
    tRec.center = (int(x), int(y))
    pgScreen.blit(tSurf, tRec)

def playSound(sound):
    if pgRunning:
        if not pg.mixer.get_busy():
            sound.sound.play()
    else:
        print("Start the Game")

def stopSound():
    if pgRunning:
        pg.mixer.stop()
    else:
        print("Start the Game")

def drawBg(r, g, b):
    if pgRunning:
        pg.draw.rect(pgScreen, (r, g, b), (0, 0, gameSize()[0], gameSize()[1]))
    else:
        print("Start the Game")

def drawEllipse(x, y, w, h, *color):
    if pgRunning:
        rec = pg.Rect(0, 0, int(w), int(h))
        rec.center = (int(x), int(y))
        pg.draw.ellipse(pgScreen, color, rec)
    else:
        print("Start the Game")

def drawLine(x1, y1, x2, y2, color):
    if pgRunning:
        pg.draw.line(pgScreen, (color[0], color[1], color[2]), (int(x1), int(y1)), (int(x2), int(y2)), color[3])

def mouseCoords():
    return pg.mouse.get_pos()

def mousePressed():
    return pg.mouse.get_pressed(1, 0, 0)[0]

def keyPressed():
	return pg.key.get_pressed()

def hide_mouse(boolean):
    pg.mouse.set_visible(not boolean)

def mouseClicked():
    pass

def mouseReleased():
    pass

def update(deltaTime):
	pass

def events(evts):
    pass

def createGame(caption="New Game", width=600, height=600, framerate=60):
    global pgScreen, pgClock, pgFrameRate, pgRunning
    if not pgScreen:
        pg.init()
        pg.mixer.init()
        pgScreen = pg.display.set_mode((int(width), int(height)))
        pg.display.set_caption(caption)
        pgClock = pg.time.Clock()
        pgFrameRate = framerate
        pgRunning = True
    else:
        print( "Screen already created")

def setIcon(path):
    pg.display.set_icon(pg.image.load(path))

def stopGame():
    global pgClock, pgRunning, pgScreen
    pg.quit()
    pgClock = None
    pgRunning = False
    pgScreen = None
    pg.mixer.quit()

def run():
    lastPressed = False
    global pgRunning, pgClock, pgFrameRate, pgScreen
    while pgRunning:
        deltaTime = pgClock.tick(pgFrameRate)/1000
        pgEvents = pg.event.get()
        if any(evt.type == pg.QUIT for evt in pgEvents):
            stopGame()
            break

        if mousePressed() and not lastPressed:
            mouseClicked()
        elif not mousePressed() and lastPressed:
            mouseReleased()

        lastPressed = mousePressed()
        update(deltaTime)
        events(pg.event.get())
        pg.display.update()