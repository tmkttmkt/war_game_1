"""
from sample import argo_move
from time import time 
import numpy as np
from test import cldt
date=[[cldt.plains if i%2==0 else 1 for i in range(300)]for i in range(1000)]
start=time()
argo_move(date,[8,10],[94,840])
print("a",time()-start)
"""

from sample import argo_move
from time import time 
import numpy as np
from test import cldt
import pgzrun
import pygame
HEIGHT=1000
WIDTH=1000
date=[[cldt.plains if i%2==0 else 1 for i in range(1000)]for i in range(1000)]
draw_date=pygame.Surface((1000,1000), flags=0)
ti=0
def sort(pos):
    global date
    start=time()
    cost,lis=argo_move(date,[500,500],pos)
    print(time()-start)
    if len(lis)>0:
        pygame.draw.line(draw_date,(255,255,255),[500,500],[lis[0][0],lis[0][1]], width=1)
        for i in range(len(lis)-1):
            pygame.draw.line(draw_date,(255,255,255),[lis[i][0],lis[i][1]],[lis[i+1][0],lis[i+1][1]], width=1)
def draw():
    screen.fill((255,0,0))
    screen.blit(draw_date,(0,0))
def update():
    global ti
    ti+=1
def on_mouse_down(pos):
    sort(pos)
pgzrun.go()

