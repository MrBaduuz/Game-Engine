import pygame
import time
import random
class Fruit:
    def __init__(self, wi, hei):
        self.x = random.randint(0, wi)
        self.y = random.randint(hei+40, hei+70)
        self.vel = -1*random.randint(20, 37)
        self.wHeight = hei

    def run(self, dT):
        self.vel += 1 * dT * 60
        self.y += self.vel * dT * 60
        ellipse(self.x, self.y , 50, 50, (255, 255, 0))
        killed = False
        speed = 0
        if(len(lastPoints[listIndex])):
            p1 = lastPoints[listIndex][len(lastPoints[listIndex])-1]
            p2 = lastPoints[listIndex][len(lastPoints[listIndex])-2]
            speed = (p1[0]-p2[0])**2 + (p1[1]-p2[1])
        if (mouseX-self.x)**2 + (mouseY-self.y) **2 < 30**2 and speed > 10**2:
            global score
            score += 1
            killed = True
        return (self.vel > 1 and self.y > 50+self.wHeight) or killed
WIDTH = 600
HEIGHT = 600
frameRate = 60
mouseX = 0
mouseY = 0
mousePressed = False
lastPoints = [[]]
listIndex = 0
fruits = [Fruit(WIDTH, HEIGHT)]
score = 0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Ninja")
pygame.mouse.set_visible(False)

def rect(x, y, w, h, *color):
    pygame.draw.rect(screen, color, (x, y, w, h))

def ellipse(x, y, w, h, *color):
    pygame.draw.ellipse(screen, color, (int(x-w/2), int(y-h/2), w, h))

def line(x1, y1, x2, y2, *color):
    pygame.draw.line(screen, color, (x1, y1), (x2, y2))

def update(deltaTime):
    for l in lastPoints:
       for point in l:
           point[2] -= deltaTime
           if point[2] < 0:
               l.remove(point)
    rect(0, 0, WIDTH, HEIGHT, (50, 50, 50))
    ellipse(mouseX, mouseY, 5, 5, (255, 255, 255))
    for l in lastPoints:
        for i in range(1, len(l)):
            currP = l[i]
            lastP = l[i-1]
            line(currP[0], currP[1], lastP[0], lastP[1], (255, 255, 255))
    for fruit in fruits:
        if fruit.run(deltaTime):
            fruits.remove(fruit)
            fruits.append(Fruit(WIDTH, HEIGHT))
            break
    
    pygame.display.update()

def mouseReleased():
    global listIndex
    
    listIndex += 1
    lastPoints.append([])

def mouseClicked():
    pass

def events(evts):
    global mouseX, mouseY, mousePressed
    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]
    lastPressed = mousePressed
    mousePressed = pygame.mouse.get_pressed()[0]
    if lastPressed and not mousePressed:
        mouseReleased()
    elif not lastPressed and mousePressed:
        mouseClicked()
    if mousePressed:
        lastPoints[listIndex].append([mouseX, mouseY, 0.1])
    
    for event in evts:
        if event.type == pygame.QUIT:
            pygame.display.quit()
            exit()


while True:
    lastTime = time.time()
    print(score)
    while time.time() < lastTime + 1/frameRate:
        pass
    deltaTime = time.time()-lastTime
    events(pygame.event.get())
    update(deltaTime)
