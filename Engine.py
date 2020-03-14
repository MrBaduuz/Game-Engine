import pygame as pg
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

def drawBg(r, g, b):
    if pgRunning:
        pg.draw.rect(pgScreen, (r, g, b), (0, 0, gameSize()[0], gameSize()[1]))
    else:
        print("Start the Game")

def drawEllipse(x, y, w, h, *color):
    if pgRunning:
        pg.draw.ellipse(pgScreen, color, (x-w/2, y-h/2, x+w/2, y+h/2))
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