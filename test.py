"""
import rapper
import numpy as np 
import random as rd
date=np.array([[rd.randint(0,10) for i in range(1100)] for j in range(1100)])
rapper.call_move_func(date,(10,10),(0,0))
"""


from rapper import call_move_func
import random as rd
from time import time 
import numpy as np
import pgzrun
import pygame
HEIGHT=900
WIDTH=900
date=np.array([[rd.randint(1,1) for i in range(900)] for j in range(900)])
draw_date=pygame.Surface((900,900), flags=0)
ti=0
def sort(pos):
    global date
    start=time()
    lis=call_move_func(date,[500,500],pos,[0,0])
    print("all",time()-start)
    if len(lis)>0:
        naw=[500+lis[0][0],500+lis[0][1]]
        pygame.draw.line(draw_date,(255,255,255),[500,500],naw)
        for i in range(len(lis)-1-1):
            pygame.draw.line(draw_date,(255,255,255),naw,[naw[0]+lis[i+1][0],naw[1]+lis[i+1][1]])
            naw[0]+=lis[i+1][0]
            naw[1]+=lis[i+1][1]
def draw():
    screen.fill((255,0,0))
    screen.blit(draw_date,(0,0))
def update():
    global ti
    ti+=1
def on_mouse_down(pos):
    sort(pos)
pgzrun.go()