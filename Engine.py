import pygame as pg
import math
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
		x = self.x * oth.x
		y = self.y * oth.y
		z = self.z * oth.z
		return Vector(x, y, z)
	def __div__(self, oth):
		x = self.x / oth.x
		y = self.y / oth.y
		z = self.z / oth.z
		return Vector(x, y, z)
	def __str__(self):
		return "X:{} Y:{} Z:{}".format(self.x, self.y, self.z)
	def copy(self):
		return Vector(self.x, self.y, self.z)
	def set(*coords):
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
		return math.atan2(self.y, self.x) * 180 / math.pi
	def angleBetween(self, oth):
		return abs((self.heading()-oth.heading()))



def gameSize():
    return pg.display.get_surface().get_size()

def drawRect(x, y, w, h, *color):
    if pgRunning:
        pg.draw.rect(pgScreen, color, (x, y, w, h))
    else:
        print("Start the Game")

def drawImage(x, y, w, h, image):
    if pgRunning:
        pgScreen.blit(pg.transform.scale(image.img, (w, h)), (x, y))
    else:
        print("Start the Game")

def drawText(text, x, y, scl, *color):
    tFon = pg.font.SysFont("Calibri", scl)
    tSurf = tFon.render(text, True, color)
    tRec = tSurf.get_rect()
    tRec.center = (x, y)
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
        rec = pg.Rect(0, 0, w, h)
        rec.center = (x, y)
        pg.draw.ellipse(pgScreen, color, rec)
    else:
        print("Start the Game")

def drawLine(x1, y1, x2, y2, color):
    if pgRunning:
        pg.draw.line(pgScreen, (color[0], color[1], color[2]), (x1, y1), (x2, y2), color[3])

def mouseCoords():
    return pg.mouse.get_pos()

def mousePressed():
    return pg.mouse.get_pressed(1, 0, 0)[0]

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
        pgScreen = pg.display.set_mode((width, height))
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