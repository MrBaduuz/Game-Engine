import time
import random

import sys
engine_path = sys.path[0].replace("Examples", "")
sys.path.append(engine_path)
import Engine as eng


eng.createGame("Drums", 600, 600, 60)
width, height = eng.gameSize()
mouseX, mouseY = (0, 0)
colors = [(223, 226, 122), (226, 122, 122), (132, 226, 122), (122, 122, 226)]
clicked_colors = [(255, 255, 0), (255, 0, 0), (0, 255, 0), (0, 0, 225)]
clicked_fields = [0, 0, 0, 0]
isPlaying = False
play_list = [1, 2, 3]
curr_song = 0
play_mode = False

def click(index):
    global isPlaying, curr_song, play_mode
    clicked_fields[index] = 0.5
    isPlaying = True
    curr_song += 1
    if curr_song == len(play_list):
        if play_mode:
            play_list.append(random.randint(0, 3))
        play_mode = not play_mode
        curr_song = 0

def mouseClicked():
    global isPlaying
    if not isPlaying and play_mode:
        if mouseX < width/2:
            if mouseY < height/2:
                click(0)
            else:
                click(2)
        else:
            if mouseY < height/2:
                click(1)
            else:
                click(3)

def show_clicked(dt):
    global isPlaying
    if clicked_fields[0] > 0:
        if clicked_fields[0] > 0.3:
            eng.drawRect(0, 0, width/2, height/2, clicked_colors[0])
        clicked_fields[0] -= dt
        if clicked_fields[0] <= 0:
            isPlaying = False
    if clicked_fields[1] > 0:
        if clicked_fields[1] > 0.3:
            eng.drawRect(width/2, 0, width/2, height/2, clicked_colors[1])
        clicked_fields[1] -= dt
        if clicked_fields[1] <= 0:
            isPlaying = False
    if clicked_fields[2] > 0:
        if clicked_fields[2] > 0.3:
            eng.drawRect(0, height/2, width/2, height/2, clicked_colors[2])
        clicked_fields[2] -= dt
        if clicked_fields[2] <= 0:
            isPlaying = False
    if clicked_fields[3] > 0:
        if clicked_fields[3] > 0.3:
            eng.drawRect(width/2, height/2, width/2, height/2, clicked_colors[3])
        clicked_fields[3] -= dt
        if clicked_fields[3] <= 0:
            isPlaying = False

def update(deltaTime):
    global mouseX, mouseY
    mouseX, mouseY = eng.mouseCoords()
    eng.drawRect(0, 0, width/2, height/2, colors[0])
    eng.drawRect(width/2, 0, width/2, height/2, colors[1])
    eng.drawRect(0, height/2, width/2, height/2, colors[2])
    eng.drawRect(width/2, height/2, width/2, height/2, colors[3])
    show_clicked(deltaTime)
    if not isPlaying and not play_mode:
        click(play_list[curr_song])


eng.update = update
eng.mouseClicked = mouseClicked
eng.run()