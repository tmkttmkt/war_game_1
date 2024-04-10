import pygame
import pgzrun
import math
import random
import os
from enum import Enum
import math
from math import sqrt
from imag import arrays_to_gif
import numpy as np
from moz import cldt,goal
from time import time as now_time
from sample import argo_move
HEIGHT=900
WIDTH=900
TITLE="RUZYEF"



class Units:
    def __init__(self,rect):
        self.list=[Unit(10,10,4,1,255,0,100),Unit(HEIGHT/2,WIDTH/2,4,1,255,0,100),Unit(HEIGHT-100,WIDTH-100,4,1,255,0,100)]
        self.bullet=[]
        self.flg=False
    def draw(self):
        for obj in self.list:
            obj.draw()
    def update(self,pov):
        for obj in self.list:
            obj.x+=pov[0]
            obj.y+=pov[1]
            for lis in obj.point_list:
                lis[0]+=pov[0]
                lis[1]+=pov[1]
            obj.update()
        if 0!=len(self.bullet):
            for obj in self.bullet:   
                obj.x+=pov[0]
                obj.y+=pov[1]
                obj.update()
                for mato in self.list:
                    if obj.colliderect(mato):
                        mato.atac(obj.dam,obj.kan)
                        self.bullet.remove(obj)
                        
    def mouse_down(self,pos):
        key=pygame.mouse.get_pressed()
        if self.flg==False:
            if key[0]==True or key[2]==True:
                for obj in self.list:
                    if obj.collidepoint(pos):
                        obj.flg=True
                        self.flg=True
                    else:
                        obj.flg=False
        else:
            if key[0]==True:
                for obj in self.list:
                    if obj.flg==True:
                        obj.move(pos)
            elif key[2]==True:
                self.flg=False
                for obj in self.list:
                    if obj.collidepoint(pos):
                        obj.flg=True
                        self.flg=True
                    else:
                        self.flg=False


class Unit(Actor):
    def __init__(self,x,y,speed,hit_rate,morale,soukou,hp):
        super().__init__('tank_syo',center=(x,y))
        self.flg=False
        self.max_morale=self.morale=morale
        self.loc=[int(x),int(y)]
        self.point_list=[]
        self.point=[None,None]
        self.cost=[]
        self.speed=speed
        self.hit_rate=hit_rate
        self.soukou=soukou
        self.hp=hp
        self.stat=goal.defense
    def update(self):
        if self.stat==goal.defense:
            print
        elif self.stat==goal.fire:
            print
        elif self.stat==goal.move:
            if(0==len(self.point_list)):
                self.stat=goal.defense
            else :
                global maps
                amari=self.speed
                se=maps.get_mapdate(self.loc)
                if(se==cldt.road):
                    amari*=2
                elif(se==cldt.river):
                    amari*=0.1
                tc_x=self.x
                tc_y=self.y
                while(amari>0 and len(self.point_list)>0):
                    self.point[0]=self.point_list[0][0]
                    self.point[1]=self.point_list[0][1]
                    self.point_list=self.point_list[1:,:]
                    x=self.point[0]-self.x
                    y=self.point[1]-self.y
                    sya=sqrt(x**2+y**2)
                    self.x+=amari*(x/sya)
                    self.y+=amari*(y/sya)
                    amari=0
                    if(x>0 and self.x>self.point[0])or(x<0 and self.x<self.point[0])or(y>0 and self.y>self.point[1])or(y<0 and self.y<self.point[1]):
                        amari=sqrt((self.x-self.point[0])**2+(self.y-self.point[1])**2)
                        self.x=self.point[0]
                        self.y=self.point[1]
                self.loc[0]+=self.x-tc_x
                self.loc[1]+=self.y-tc_y
        elif self.stat==goal.speed_move:
            print

    def move(self,pos):
        global maps
        start=now_time()
        self.stat=goal.move
        print(self.x,self.y,self.loc[0],self.loc[1],pos[0],pos[1])
        self.point_list=argo_move(maps.list[maps.mode].date,self.loc,pos)
        print(now_time()-start)
    def atac(self,dam,kan):
        if kan>self.soukou:
            self.hp-=dam
            self.morale-=dam*2
        else:
            self.morale-=dam


class Bullet(Actor):
    def __init__(self,x,y,dam,kan):
        super().__init__('tama',center=(x,y))
        self.dam=dam
        self.kan=kan
        self.speed=[x,y]
    def update(self):
        self.x+=self.speed[0]
        self.y+=self.speed[1]

class Buttan:
    def __init__(self,color,pos,scope,txt):
        self.txt=txt
        self.key=keys.Q
        self.color=color
        self.pos=pos
        self.scope=scope
        if 0!=len(self.txt):
            self.txtsize=(((self.scope[0]-60)/len(self.txt))*(90/60))
        else:
            self.txtsize=0
        self.rect=Rect(pos,scope)
    def draw(self):
        screen.draw.filled_rect(self.rect,self.color)
        screen.draw.text(self.txt,self.pos,fontname='genshingothic-bold.ttf',color=(0,0,0),fontsize=self.txtsize)
        screen.draw.text("(Q)",(self.pos[0]+self.scope[0]-60,self.pos[1]),color=(0,0,0),fontsize=60)
    def key_down(self,key):
        if key==self.key:
            return 1
        return 0
    def collidepoint(self,pos,key):
        if key==mouse.LEFT or key==mouse.RIGHT:
            if(self.pos[0]<=pos[0] and pos[0]<=self.pos[0]+self.scope[0] and self.pos[1]<=pos[1] and pos[1]<=self.pos[1]+self.scope[1]):
                return 1
        return 0
        

        
class Start:
    def __init__(self):
        self.title_mode=0
        self.start=Buttan((64,64,64),[WIDTH/2-120,HEIGHT/2],[240,60],"START")
        self.conit=Buttan((64,64,64),[WIDTH/2-120,HEIGHT/2+70],[240,60],"CONTINUATION")
        self.exp=Buttan((64,64,64),[WIDTH/2-120,HEIGHT/2+140],[240,60],"EXPLANATION")
        self.txt ="\n"
        self.txt+="\n"
        self.txt+="\n"
    def set_start(self):
        self.title_mode=0
    def draw(self):
        if self.title_mode==0:
            screen.fill((128, 0, 0))
            screen.draw.text("RUZYEF",(WIDTH/2-200,HEIGHT/3-100),fontname='fugazone_regular.ttf',color=(0,0,0),fontsize=100)
            self.start.draw()
            self.conit.draw()
            self.exp.draw()
        elif self.title_mode==1:
            return
        elif self.title_mode==2:
            screen.fill((255,255,0))
            screen.draw.text("chachachachara\nchachachachara",(0,0),fontname='genshingothic-bold.ttf',color=(0,0,0),fontsize=50)
        elif self.title_mode==3:
            screen.fill((255,255,255))
            screen.draw.text(self.txt,(0,0),fontname='genshingothic-bold.ttf',color=(0,0,0),fontsize=50)
    def mouse_down(self,pos,key):
        if self.title_mode==0:
            if self.start.collidepoint(pos,key):
                self.title_mode=1
                return 1
            elif self.conit.collidepoint(pos,key):
                self.title_mode=2
            elif self.exp.collidepoint(pos,key):
                self.title_mode=3
        elif self.title_mode==1:
            return 0
        elif self.title_mode==2:
            if key==mouse.LEFT or key==mouse.RIGHT:
                self.title_mode=0
        elif self.title_mode==3:
            if key==mouse.LEFT or key==mouse.RIGHT:
                self.title_mode=0
        return 0
class Maps:
    def __init__(self):
        self.mode=-1
        self.list=[tesmap(),test(),Map([900,900])]
        self.set_buttan()
        self.pov=[0,0]
    def get_mapdate(self,loc):
            return cldt(self.list[self.mode].draw_date.get_at((int(loc[0]),int(loc[1]))))
    def set_buttan(self):
        self.buttan_list=[Buttan((64,64,64),[WIDTH/2-120,HEIGHT/2],[240,60]," test "),Buttan((64,64,64),[WIDTH/2-120,HEIGHT/2+70],[240,60]," map "),Buttan((64,64,64),[WIDTH/2-120,HEIGHT/2+140],[240,60],"return")]
    def update(self):
        moto_pov=[self.pov[0],self.pov[1]]
        if keyboard.s:
            if(self.pov[1]>-(self.list[self.mode].rect[3]-HEIGHT)):
                self.pov[1] -= 10
        if keyboard.w:
            if(self.pov[1]<0):
                self.pov[1] += 10
        if keyboard.d:
            if(self.pov[0]>-(self.list[self.mode].rect[2]-WIDTH)):
                self.pov[0]-= 10
        if keyboard.a:
            if(self.pov[0]<0):
                self.pov[0] += 10
        self.list[self.mode].units.update([self.pov[0]-moto_pov[0],self.pov[1]-moto_pov[1]])
    def mouse_down(self,pos,key):
        if self.mode==-1:
            if key==mouse.LEFT or key==mouse.RIGHT:
                i=0
                for obj in self.buttan_list:
                    if obj.collidepoint(pos,key):
                        self.mode=i
                    i+=1
                if self.mode==2:
                    self.mode=-1
                    return 1
        else :
            self.list[self.mode].mouse_down(pos)
        return 0
    def draw(self):
        screen.fill((172,172,172))
        if self.mode==-1:
            for obj in self.buttan_list:
                obj.draw()
        else:
            self.list[self.mode].draw(self.pov)
class Map:
    def __init__(self,wide):
        self.rect=Rect((0,0),(wide[0],wide[1]))
        self.date= [[cldt.plains for i in range(self.rect[2])] for j in range(self.rect[3])]
        self.draw_date=pygame.Surface((self.rect[2],self.rect[3]), flags=0)
        #0mu 1heiya 2kawa 3tetudou 4douro 5mori 6mati
        self.draw_date.fill(cldt.plains.value,None, special_flags=0)
        self.units=Units(self.rect)
    def mawari(self):
        self.date= [[(cldt.mu if i<3 or j<3 or self.rect[2]-3<=i or self.rect[2]-3<=i else self.date[j][i]) for i in range(self.rect[2])] for j in range(self.rect[3])]
    def mouse_down(self,pos):
            self.units.mouse_down(pos)
    def setdate(self,name):
        source=pygame.image.load(os.path.join('images', name))
        source=source.convert()
        rect=self.draw_date.blit(source,[0,0], area=None, special_flags = 0)
        for y in range(rect[1]):
            for x in range(rect[0]):
                self.date[y][x]=cldt.mu
                for cld in cldt:
                    if cld.value==self.draw_date.get_at((x, y)):
                        self.date[y][x]=cld.value
                if self.date[y][x]==cldt.mu:
                    self.draw_date.set((x, y),cldt.mu.value)
    def draw(self,pov):
        screen.blit(self.draw_date,(pov[0],pov[1]))
        self.units.draw()
    def sen(self,pos,go_pos,haba,setd):
        haba/=2
        xsen=(pos[0]-go_pos[0])
        ysen=(pos[1]-go_pos[1])
        if(ysen!=0 and xsen!=0):
            a=ysen/xsen
            b=pos[1]-a*pos[0]
            ap=-1/a
            hyp=(math.sqrt(ysen**2+xsen**2)/xsen)
            haba*=abs(hyp)
            if(pos[1]<go_pos[1]):
                bp=pos[1]-ap*pos[0]
                bgp=go_pos[1]-ap*go_pos[0]
            else:
                bgp=pos[1]-ap*pos[0]
                bp=go_pos[1]-ap*go_pos[0]
            for y in range(self.rect[3]):
                for x in range(self.rect[2]):
                    if(y >= a*x+b -haba and y <= a*x+b +haba):
                        if(y >= ap*x+bp and y <= ap*x+bgp):
                            self.date[y][x]=setd
                            self.draw_date.set_at((x,y),setd.value)
        elif(ysen==0 and xsen==0):
            return
        elif(ysen==0):
            if(pos[0]>go_pos[0]):
                box=pos
                pos=go_pos
                go_pos=box
            haba=int(haba)
            for x in range(pos[0],go_pos[0]):
                for y in range(pos[1]-haba,pos[1]+haba):
                    self.date[y][x]=setd
                    self.draw_date.set_at((x,y),setd.value)
        elif(xsen==0):
            if(pos[1]>go_pos[1]):
                box=pos
                pos=go_pos
                go_pos=box
            haba=int(haba)
            for y in range(pos[1],go_pos[1]):
                for x in range(pos[0]-haba,pos[0]+haba):
                    self.date[y][x]=setd
                    self.draw_date.set_at((x,y),setd.value)
    def en(self,pos,haba,setd):
        for y in range(pos[1]-haba,pos[1]+haba):
            for x in range(pos[0]-haba,pos[0]+haba):
                if((x-pos[0])**2+(y-pos[1])**2<=(haba/2)**2):
                    self.date[y][x]=setd
                    self.draw_date.set_at((x,y),setd.value)
    def daen(self,fpos,setd):
        x_min=self.rect[2]
        x_max=0
        y_min=self.rect[3]
        y_max=0
        for pos in fpos:
            #print(pos)
            if(pos[0]<x_min):
                x_min=pos[0]
            if(pos[0]>x_max):
                x_max=pos[0]
            if(pos[1]<y_min):
                y_min=pos[1]
            if(pos[1]>y_max):
                y_max=pos[1]
        #print(x_min,x_max,y_min,y_max)
        xr=(x_max-x_min)/2
        yr=(y_max-y_min)/2
        cen=[(x_max+x_min)/2,(y_max+y_min)/2]
        #print(cen,xr,yr)
        for y in range(y_min,y_max):
            for x in range(x_min,x_max):
                siki=((x-cen[0])/xr)**2+((y-cen[1])/yr)**2
                if(siki<=1):
                    self.date[y][x]=setd
                    self.draw_date.set_at((x,y),setd.value)
    def sikaku(self,pos,go_pos,setd):
        for y in range(pos[1] if pos[1]<go_pos[1] else go_pos[1],go_pos[1] if pos[1]<go_pos[1] else pos[1]):
            for x in range(pos[0] if pos[0]<go_pos[0] else go_pos[0],go_pos[0] if pos[0]<go_pos[0] else pos[0]):
                self.date[y][x]=setd
                self.draw_date.set_at((x,y),setd.value)                          
    def all(self,setd):
        self.draw_date.fill(setd.value,None, special_flags=0)
        self.date= [[setd for i in range(self.rect[2])] for j in range(self.rect[3])]
class test(Map):
    def __init__(self):
        source=pygame.image.load(os.path.join('images', 'test.png'))
        wide_rect=source.get_clip()
        super().__init__([wide_rect[2],wide_rect[3]])
        self.setdate('test.png')  
class tesmap(Map):
    def __init__(self):
        super().__init__([1000,1000])
        
        self.en([0,50],10,cldt.river)
        self.sen([0,50],[100,400],10,cldt.river)
        self.en([100,400],10,cldt.river)
        self.sen([100,400],[600,500],10,cldt.river)
        self.en([600,500],10,cldt.river)
        self.sen([600,500],[900,400],5,cldt.river)
        self.sen([600,500],[700,900],5,cldt.river)
    
        self.sikaku([250,70],[390,140],cldt.urban)
        self.sen([400,0],[300,100],5,cldt.road)
        self.sen([300,100],[900,100],5,cldt.road)
        self.sen([300,100],[290,400],5,cldt.road)
        self.sen([290,400],[200,800],5,cldt.road)
        self.sen([200,800],[100,900],5,cldt.road)


        self.sen([300,0],[200,900],10,cldt.rail)

        self.daen([[100,100],[200,100],[150,-100],[150,200]],cldt.woods)
        self.daen([[0,400],[100,800],[150,600],[-150,700]],cldt.woods)
maps=Maps()
start=Start()
time=0
def draw():
    start.draw()
    if start.title_mode==1:
        maps.draw()
    
def update():
    global time,maps
    time+=1
    maps.update()
def on_mouse_down(pos,button):
    if start.title_mode==1:
        if 1==maps.mouse_down(pos,button):
            start.set_start()
    else:
        start.mouse_down(pos,button)
            
        
#import sys
#sys.setrecursionlimit(1000000)

pgzrun.go()
"""
(*args, **kwargs)


C:\ProgramData\Anaconda3\Lib\site-packages\pygame
C:\ProgramData\Anaconda3\Lib\site-packages\pgzero


C:/Program Files/Python37/Lib/site-packages/pgzero/__pycache__
C:/Program Files/Python37/Lib/site-packages/pgzero/data

C:/Program Files/Python37/Lib/site-packages/pgzero/__init__.py
C:/Program Files/Python37/Lib/site-packages/pgzero/__main__.py
C:/Program Files/Python37/Lib/site-packages/pgzero/actor.py
C:/Program Files/Python37/Lib/site-packages/pgzero/animation.py
C:/Program Files/Python37/Lib/site-packages/pgzero/builtins.py
C:/Program Files/Python37/Lib/site-packages/pgzero/clock.py
C:/Program Files/Python37/Lib/site-packages/pgzero/constants.py
C:/Program Files/Python37/Lib/site-packages/pgzero/game.py
C:/Program Files/Python37/Lib/site-packages/pgzero/keyboard.py
C:/Program Files/Python37/Lib/site-packages/pgzero/loaders.py
C:/Program Files/Python37/Lib/site-packages/pgzero/music.py
C:/Program Files/Python37/Lib/site-packages/pgzero/ptext.py
C:/Program Files/Python37/Lib/site-packages/pgzero/rect.py
C:/Program Files/Python37/Lib/site-packages/pgzero/runner.py
C:/Program Files/Python37/Lib/site-packages/pgzero/screen.py
C:/Program Files/Python37/Lib/site-packages/pgzero/soundfmt.py
C:/Program Files/Python37/Lib/site-packages/pgzero/spellcheck.py
C:/Program Files/Python37/Lib/site-packages/pgzero/tone.py


https://camp.trainocate.co.jp/magazine/python_machine_learning/

"""

