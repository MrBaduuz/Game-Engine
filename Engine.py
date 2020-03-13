import pygame as pg
pgScreen = None
pgClock = None
pgFrameRate = 0
pgRunning = False

def gameSize():
    return pg.display.get_surface().get_size()

def drawRect(x, y, w, h, *color):
    if pgRunning:
        pg.draw.rect(pgScreen, color, (x, y, w, h))
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
        pgScreen = pg.display.set_mode((width, height))
        pg.display.set_caption(caption)
        pgClock = pg.time.Clock()
        pgFrameRate = framerate
        pgRunning = True
    else:
        print( "Screen already created")
def stopGame():
    global pgClock, pgRunning, pgScreen
    pg.quit()
    pgClock = None
    pgRunning = False
    pgScreen = None

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
