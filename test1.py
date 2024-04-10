import pgzrun
from var import *
from func import rerect
from math import sqrt,acos
ti=0
LOT=(450,450)
os=Rect((450,450),(10,10))
re=Rect((800,100),(0,700))
def draw():
    screen.clear()
    screen.draw.filled_rect(os,WHITE)
    screen.draw.filled_rect(re,RED)
def update():
    global ti,os,re
    ti+=1
    cs=rerect(os.copy())
    if cs.colliderect(re):
        print("a")
    else:
        print("A")
    if re.colliderect(cs):
        print("b")
    else:
        print("B")
def on_mouse_down(pos):
    global os
    os=Rect(LOT,(pos[0]-450,pos[1]-450))
pgzrun.go()