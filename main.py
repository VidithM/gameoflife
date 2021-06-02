import time
import pygame
from pygame.locals import *

from toggle import Toggle

GRID_W = 500
GRID_H = 500
INTV = 100

ALIVE_COLOR = (255, 255, 255)
DEAD_COLOR = (0, 0, 0)

pts = set()


running = True
playing = False
clicked = False

'''
Render the current state of the grid
'''
def render():
    screen.fill(DEAD_COLOR)
    for x, y in pts:
        put = Rect(x, y, 10, 10)
        pygame.draw.rect(screen, ALIVE_COLOR, put)

'''
Simulate the game
'''
def play():
    kill = []
    birth = []
    for i in range(50):
        for j in range(50):
            i *= 10
            j *= 10
            neighbor_cnt = getneighbors((i, j))
            #print((i, j))
            if((i, j) in pts):
                #print(neighbor_cnt)
                if((neighbor_cnt < 2) or (neighbor_cnt > 3)):
                    kill.append((i, j))
            else:
                if(neighbor_cnt == 3):
                    birth.append((i, j))
            i //= 10
    
    #print(birth)
    #print(kill)
    for pt in birth:
        draw(pt)
    for pt in kill:
        destroy(pt)

def getneighbors(pt):
    res = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if(i != 0 or j != 0):
                i *= 10
                j *= 10
                if((pt[0] + i, pt[1] + j) in pts):
                    res += 1
                i /= 10
    return res

def draw(pt):
    x = pt[0]
    y = pt[1]
    x -= x%10
    y -= y%10
    pt = (x, y)
    if pt in pts:
        destroy(pt)
    else:
        pts.add(pt)

def destroy(pt):
    pts.remove(pt)

pygame.init()
screen = pygame.display.set_mode((GRID_W, GRID_H))

key_tog = Toggle()

t = 0

while running:
    key_in = pygame.key.get_pressed()
    toggle_pause = False
    for elem in key_in:
        toggle_pause = toggle_pause or elem 
    
    mouse_in = pygame.mouse.get_pressed()[0]

    if(toggle_pause):
        key_tog.toggle()
    else:
        playing = key_tog.eval()
    if(playing):
        if(time.time_ns()/1000000 - t >= INTV):
            play()
            t = time.time_ns()/1000000
    else:
        t = time.time_ns()/1000000
        if(mouse_in):
            at = pygame.mouse.get_pos()
            if(not clicked):
                draw(at)
            clicked = True
        else:
            clicked = False
    #print(pts)
    render()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    pygame.display.flip()