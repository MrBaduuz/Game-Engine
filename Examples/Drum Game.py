import Engine as eng
from time import sleep
from random import randint

soundList = []
currSound = 0
newS = True
isPlaying = False
    
class Drum:
    def __init__(self, x, y, w, h, counter,  col, clickcol):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.counter = counter
        self.color = col
        self.clickedcol = clickcol
        self.pressed = 0

    def show(self, dt):
        global currSound
        if self.pressed > 0:
            isPlaying = True
            eng.drawRect(self.x, self.y, self.w, self.h, self.clickedcol)
            self.pressed -= dt
            if self.pressed < 0:
                isPlaying = False
                currSound += 1
        else:
            eng.drawRect(self.x, self.y, self.w, self.h, self.color)
            isPlaying = False

    def clicked(self):
        mX, mY = eng.mouseCoords()
        if mX > self.x and mX < self.x + self.w and mY > self.y and mY < self.y + self.h and newS:
            self.pressed = 0.25
            if soundList[currSound] == counter:
                currSound += 1
                if currSound == len(soundList):
                    currSound = 0
                    newS = True
                    soundList.append(randint(0, len(drums)-1))
            else:
                eng.stopGame()
                exit()
            
    def click(self):
        self.pressed = 0.25

eng.createGame("Drums", 400, 400, 60)

drums = (Drum(0, 0, eng.gameSize()[0]/2, eng.gameSize()[1]/2, 0, (255, 200, 0),  (255, 255, 0)), Drum(eng.gameSize()[0]/2, 0, eng.gameSize()[0]/2, eng.gameSize()[1]/2, 1, (255, 100, 100),  (255, 0, 0)), \
         Drum(0, eng.gameSize()[1]/2, eng.gameSize()[0]/2, eng.gameSize()[1]/2, 2, (130, 200, 102),  (0, 255, 0)), Drum(eng.gameSize()[0]/2, eng.gameSize()[1]/2, eng.gameSize()[0]/2, eng.gameSize()[1]/2, 3, (125, 130, 255),  (0, 0, 255)))

def mouseClicked():
    for drum in drums:
        drum.clicked()
eng.mouseClicked = mouseClicked

def update(deltaTime):
    global isPlaying, soundList, currSound, newS
    eng.drawBg(50, 50, 50)
    for drum in drums:
        drum.show(deltaTime)
    if not isPlaying:
        drums[currSound].click()
    ''' if newS:
        if not isPlaying:
            if currSound == len(soundList):
                newS = False
                currSound = 0
                isPlaying = False
            else:
                drums[soundList[currSound]].click()
                currSound += 1'''

                
                
def events(evts):
    pass

eng.update = update
eng.events = events
eng.run()
exit()
