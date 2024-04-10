from turtle import speed
import pygame
import pgzrun
import random
import os
import math
from Unit import *#Units
from enu import title_mode
import numpy as np 
import re
import gc
#gc.collect()
from var import *

file_count=None

class Time_sys:
    def __init__(self,now_time):
        self.time=now_time+[0,0]
        self.speed=1
        self.pos=(10,10)
        self.scope=(170,50+100)
        self.stop=Smol_Buttan(WHITE,(20,20),(30,30)," ||",0)
        self.sp1=Smol_Buttan(WHITE,(20+30+10,20),(30,30)," <",1)
        self.sp2=Smol_Buttan(WHITE,(20+(30+10)*2,20),(30,30)," <<",2)
        self.sp3=Smol_Buttan(WHITE,(20+(30+10)*3,20),(30,30),"<<<",4)
    def set_time(self,now_time):
        self.time=now_time+[0,0]
    def draw(self):
        screen.draw.filled_rect(Rect(self.pos,self.scope),(128,64,64))
        self.stop.draw(self.speed)
        self.sp1.draw(self.speed)
        self.sp2.draw(self.speed)
        self.sp3.draw(self.speed)
        screen.draw.text(self.time_text(),(10,60),fontname='genshingothic-bold.ttf',color=BLACK,fontsize=30)
    def mouse_down(self,pos):
        if(self.pos[0]<=pos[0] and pos[0]<=self.pos[0]+self.scope[0] and self.pos[1]<=pos[1] and pos[1]<=self.pos[1]+self.scope[1]):
            if self.stop.collidepoint(pos):
                self.speed=0
            elif self.sp1.collidepoint(pos):
                self.speed=1
            elif self.sp2.collidepoint(pos):
                self.speed=2
            elif self.sp3.collidepoint(pos):
                self.speed=4
            return True
        return False
    def past_time(self,time):
        n=5
        exm_time=[]
        now_time=self.time.copy()
        lis=[0,0,0,24,60,60]
        time+=[0]
        while n>0:
            if now_time[n]-time[n]>=0:
                exm_time.append(now_time[n]-time[n])
            else:
                exm_time.append(now_time[n]-time[n]+lis[n])
                now_time[n-1]-=1
            n-=1
        exm_time+=[0]
        return str(exm_time[5])+"年"+str(exm_time[4])+"月"+str(exm_time[3])+"日"+str(exm_time[2])+"時"+str(exm_time[1])+"分"+str(exm_time[0])+"秒"
    def time_text(self):
        return str(self.time[0])+"年"+str(self.time[1])+"月\n"+str(self.time[2])+"日"+str(self.time[3])+":"+str(self.time[4])+":"+str(self.time[5])
    def save_text(self):
        return str(self.time[0])+"年"+str(self.time[1])+"月"+str(self.time[2])+"日"+str(self.time[3])+"時"+str(self.time[4])+"分"+str(self.time[5])+"秒"
    def update(self):
        self.time[6]+=self.speed
        if self.time[6]>60:
            self.time[6]-=60
            self.time[5]+=1        
            if self.time[5]>60:
                self.time[5]-=60
                self.time[4]+=1
                if self.time[4]>60:
                    self.time[4]-=60
                    self.time[3]+=1
                    if self.time[3]>24:
                        self.time[3]-=24
                        self.time[2]+=1 
        return self.speed   
    def key_down(self,key):
        if key==keys.K_1:
            self.speed=1
        elif key==keys.K_2:
            self.speed=2
        elif key==keys.K_3:
            self.speed=4
        elif key==keys.K_0:
            self.speed=0
class Load:
    def __init__(self,ma,ti,pas) -> None:
        self.map=ma
        self.time=ti
        self.txt_pas=str(pas)
        self.mae=Buttan(WHITE,(700-70-10,600-40-10),(70,40),"mae")
        self.usi=Buttan(WHITE,(700+(-70-10)*2,600+(-40-10)*1),(70,40),"usi")
        self.kettei=Buttan(WHITE,(700+(-70-10)*3,600+(-40-10)*1),(70,40),"ket")
    def draw(self):
        screen.draw.filled_rect(Rect((200,300),(500,300)),GRAY)
        screen.draw.text("map="+self.map,(200,300),fontname='genshingothic-bold.ttf',color=BLACK,fontsize=30)
        screen.draw.text("\ntime="+self.time,(200,300),fontname='genshingothic-bold.ttf',color=BLACK,fontsize=30)
        self.mae.draw()
        self.usi.draw()
        self.kettei.draw()
    def collidepoint(self,pos):
        if self.usi.collidepoint(pos):
            return -1
        elif self.mae.collidepoint(pos):
            return 1
        elif self.kettei.collidepoint(pos):
            return 0
    def pas(self):
        return "save/date"+self.txt_pas
class Buttan:
    def __init__(self,color,pos,scope,txt):
        self.txt=txt
        self.color=color
        self.pos=pos
        self.scope=scope
        if 0!=len(self.txt):
            self.txtsize=(((self.scope[0])/len(self.txt))*(90/60))
        else:
            self.txtsize=0
        self.rect=Rect(pos,scope)
    def draw(self):
        screen.draw.filled_rect(self.rect,self.color)
        screen.draw.text(self.txt,self.pos,fontname='genshingothic-bold.ttf',color=BLACK,fontsize=self.txtsize)
    def key_down(self,key):
        if key==self.key:
            return True
        return False
    def collidepoint(self,pos):
        if(self.pos[0]<=pos[0] and pos[0]<=self.pos[0]+self.scope[0] and self.pos[1]<=pos[1] and pos[1]<=self.pos[1]+self.scope[1]):
            return True
        return False
class Smol_Buttan(Buttan):
    def __init__(self,color,pos,scope,txt,mode):
        self.mode=mode
        super().__init__(color,pos,scope,txt)
    def draw(self,speed):
        super().draw()
        if speed==self.mode:
            screen.draw.rect(self.rect,(255,0,0))
class Start:
    def __init__(self):
        self.title_mode=title_mode.START
        self.start=Buttan(GRAY,[WIDTH/2-120,HEIGHT/2],[240,60],"始める   ")
        self.conit=Buttan(GRAY,[WIDTH/2-120,HEIGHT/2+70],[240,60],"---------")
        self.exp=Buttan(GRAY,[WIDTH/2-120,HEIGHT/2+140],[240,60],"説明   ")
        self.exp_list=[Actor("sxe_1",topleft=(530,123)),Actor("sxe_2",topleft=(620,123)),Actor("sxe_3",topleft=(517,500)),Actor("sxe_4",topleft=(517,819))]
        self.save=[]
        self.save_return=Buttan(GRAY,[60,60],[240,60],"戻る  ")
        self.save_num=0
        self.load_num()
        self.load_all()
        music.set_volume(0.3)
        music.play("-1")
    def set_start(self):
        self.title_mode=title_mode.START
        self.load_num()
        self.load_all()
    def draw(self):
        if self.title_mode==title_mode.START:
            screen.fill((128, 0, 0))
            screen.draw.text("RUZYEF",(WIDTH/2-200,HEIGHT/3-100),fontname='fugazone_regular.ttf',color=BLACK,fontsize=100)
            self.start.draw()
            self.conit.draw()
            self.exp.draw()
        elif self.title_mode==title_mode.execution:
            return
        elif self.title_mode==title_mode.CONTINUATION:
            screen.fill(YELLOW)
            if 0!=len(self.save):
                self.save_return.draw()
                self.save[self.save_num].draw()
            else:
                screen.draw.text("セーブデータが存在しません\nクリックでスタート画面に戻れます",(0,400),fontname='genshingothic-bold.ttf',color=BLACK,fontsize=55)
        elif self.title_mode==title_mode.EXPLANATION:
            screen.fill(WHITE)
            ft=30
            n=0
            for ob in self.exp_list:
                ob.draw()
            screen.draw.text(EX_TXT_1,(0,0),fontname='genshingothic-bold.ttf',color=BLACK,fontsize=ft)
            n+=5
            screen.draw.text(EX_TXT_2,(0,ft*n),fontname='genshingothic-bold.ttf',color=BLACK,fontsize=ft)
            n+=4
            screen.draw.text(EX_TXT_3,(0,ft*n),fontname='genshingothic-bold.ttf',color=BLACK,fontsize=ft)
            n+=5
            screen.draw.text(EX_TXT_4,(0,ft*n),fontname='genshingothic-bold.ttf',color=BLACK,fontsize=ft)
            n+=5
            screen.draw.text(EX_TXT_5,(0,ft*n),fontname='genshingothic-bold.ttf',color=BLACK,fontsize=ft)
            n+=4
            screen.draw.text(EX_TXT_6,(0,ft*n),fontname='genshingothic-bold.ttf',color=BLACK,fontsize=ft)
    def mouse_down(self,pos):
        if self.title_mode==title_mode.START:
            if self.start.collidepoint(pos):
                self.title_mode=title_mode.execution
            elif self.conit.collidepoint(pos):
                self.title_mode=title_mode.CONTINUATION
            elif self.exp.collidepoint(pos):
                self.title_mode=title_mode.EXPLANATION
        elif self.title_mode==title_mode.execution:
            pass
        elif self.title_mode==title_mode.CONTINUATION:
            if 0!=len(self.save):
                if self.save_return.collidepoint(pos):
                    self.title_mode=title_mode.START
                exm=self.save[self.save_num].collidepoint(pos)
                if exm==0:
                    return self.save[self.save_num].pas()
                elif exm==-1 or exm==1:
                    self.save_num+=exm
                    if self.save_num<0:
                        self.save_num=len(self.save)-1
                    if self.save_num>len(self.save)-1:
                        self.save_num=0
            else:
                self.title_mode=title_mode.START
        elif self.title_mode==title_mode.EXPLANATION:
                self.title_mode=title_mode.START
    def load_num(self):
        global file_count
        folder_path = "save"
        file_count = len([f for f in os.listdir(folder_path)])
    def load_all(self):
        global file_count
        n=0
        while n<file_count:
            with open("save/date"+str(n),mode="r") as f:
                txt=f.readlines()[0]
                map_name=txt[:txt.find(":")]
                txt=txt[txt.find(":")+1:]
                time_name=txt[:txt.find(":")]
                self.save.append(Load(map_name,time_name,n))
            n+=1
class Maps:
    def __init__(self):
        self.mode=-1
        self.map=None
        self.pov=[0,0]
        self.ret=Buttan(GRAY,[WIDTH/2-120,HEIGHT/2],[240,60],"ゲームに戻る   ")
        self.seve=Buttan(GRAY,[WIDTH/2-120,HEIGHT/2+70],[240,60],"------")
        self.menu=Buttan(GRAY,[WIDTH/2-120,HEIGHT/2+140],[240,60],"メニュー  ")
        self.return_mode=False
        self.state=None
        self.kyok=0
        self.buttan_list=[Buttan(GRAY,[WIDTH/2-120,HEIGHT/2-70],[240,60],"heiankyou")
                        ,Buttan(GRAY,[WIDTH/2-120,HEIGHT/2],[240,60],"beerui")
                        ,Buttan(GRAY,[WIDTH/2-120,HEIGHT/2+70],[240,60],"sityefk")
                        ,Buttan(GRAY,[WIDTH/2-120,HEIGHT/2+140],[240,60],"戻る  ")]
    def update(self):
        if not self.return_mode:
            moto_pov=self.pov.copy()
            if keyboard.s:
                if(self.pov[1]>-(self.map.rect[3]-HEIGHT)):
                    self.pov[1] -= 10
            if keyboard.w:
                if(self.pov[1]<0):
                    self.pov[1] += 10
            if keyboard.d:
                if(self.pov[0]>-(self.map.rect[2]-WIDTH)):
                    self.pov[0]-= 10
            if keyboard.a:
                if(self.pov[0]<0):
                    self.pov[0] += 10
            if self.map!=None:
                self.map.update((self.pov[0]-moto_pov[0],self.pov[1]-moto_pov[1]))
            if self.map!=None:
                if not music.is_playing(""):
                    music.play_once(str(self.kyok%2))
                    self.kyok+=1
    def time_load(self,txt):
        name_list=["年","月","日","時","分","秒"]
        lis=[]
        for c in name_list:
            lis.append(int(txt[:txt.find(c)]))
            txt=txt[txt.find(c)+1:]
        return lis
    def load(self,pas):
        with open(pas,mode="r") as f:
            txt_list=f.readlines()
            txt=txt_list.pop(0)
            map_name=txt[:txt.find(":")]
            txt=txt[txt.find(":")+2:]
            time_name=txt[:txt.find(":")]
            time=self.time_load(time_name)

            unit_list=[]
            for txt in txt_list:
                pass
            map_class=globals().get(map_name)
            map_class().load(time,unit_list)

    def mouse_down(self,pos,button):
        if self.map==None:
            for obj in self.buttan_list:
                if obj.collidepoint(pos):
                    if obj.txt=="戻る  ":
                        return  BACK
                    map_class=globals().get(re.sub(" ","",obj.txt))
                    self.map=map_class()
                    music.play_once(str(self.kyok%2))
                    self.kyok+=1
                    break
        else:
            if self.return_mode:
                if self.ret.collidepoint(pos):
                    self.return_mode=False
                    music.unpause()
                if self.seve.collidepoint(pos):
                    self.map.save()
                if self.menu.collidepoint(pos):
                    self.return_mode=False
                    self.map=None
                    music.unpause()
                    music.play("-1")
            else:
                if self.map.vic_mode:
                    self.map=None
                    self.state=None
                else:
                    if self.map.start_exm:
                        self.map.start_exm=False
                    else: 
                        if self.map.time_draw:
                            if self.map.time.mouse_down(pos):
                                return NOT_BACK
                        if not self.map.vic_mode:
                            obj=None
                            for units in self.map.units_list:
                                obj=units.mouse_down(pos,button)
                                if obj!=None:
                                    if obj==CHANGE:
                                        self.state=None
                                    else:
                                        self.state=Unit_state(obj)

        return NOT_BACK
    def key_down(self,key):
        if self.map!=None:
            self.map.time.key_down(key)
            if key==keys.ESCAPE:
                self.return_mode=not self.return_mode
                if self.return_mode:
                    music.pause()
                else:
                    music.unpause()

            elif key==keys.SPACE:
                self.map.vic_draw=not self.map.vic_draw
            elif key==keys.T:
                self.map.time_draw=not self.map.time_draw
    def draw(self,screen):
        if self.map==None:
            screen.fill((200,200,200))
            for obj in self.buttan_list:
                obj.draw()
        else:
            self.map.draw(self.pov,screen)
            if self.return_mode:
                screen.draw.filled_rect(Rect((WIDTH/2-120-20,HEIGHT/2-20), (280,40+140+60)),WHITE)
                self.ret.draw()
                self.seve.draw()
                self.menu.draw()
        if self.state!=None:
            self.state.draw(screen)

class Map:
    def __init__(self,wide,time):
        self.rect=Rect((0,0),(wide[0],wide[1]))
        self.date= np.array([[1 for i in range(self.rect[2])] for j in range(self.rect[3])])
        self.draw_date=pygame.Surface((self.rect[2],self.rect[3]), flags=0)
        #0mu 1heiya 2kawa 3tetudou 4douro 5mori 6mati
        self.color=[(0,0,0),(0,255,0),(0,128,255),(32,32,32),(128,64,0),(0,128,0),(128,128,128)]
        self.draw_date.fill(self.color[1],None, special_flags=0)
        self.vic_mode=False
        self.units_list=[]
        self.bullets=Bullets(self)
        self.time=Time_sys(time)
        self.time_draw=True
        self.start_time=time
        self.vic_txt="殲滅せよ！"
        self.vic_draw=True
        self.start_exm=True
    def search(self,rect:Rect):
        lis=[]
        for units in self.units_list:
            for unit in units.list:
                if rect.collidepoint(unit.center):
                    lis.append(unit)
        return lis
    def vic_if(self):
        return False
    def los_if(self):
        return False
    def save(self):
        global file_count
        with open("save/date"+str(file_count),mode="w") as f:
            txt=self.__class__.__name__+":"
            txt+=self.time.save_text()+":"
            f.write(txt)
            file_count+=1
    def setdate(self,name):
        source=pygame.image.load(os.path.join('images', name))
        source=source.convert()
        rect=self.draw_date.blit(source,[0,0], area=None, special_flags = 0)
        for y in range(rect[3]):
            for x in range(rect[2]):
                self.date[y,x]=i=0
                for set_color in self.color:
                    if set_color==self.draw_date.get_at((x,y)):
                        self.date[y,x]=i
                    i+=1
    def draw(self,pov,screen):
        screen.blit(self.draw_date,(pov[0],pov[1]))
        self.bullets.draw()
        for units in self.units_list:
            units.draw(screen)
        if self.time_draw:
            self.time.draw()
        if self.vic_draw:
            screen.draw.filled_rect(Rect((500,0), (400,100)),WHITE)
            screen.draw.text(self.vic_txt,(500,0),fontname='genshingothic-bold.ttf',color=BLACK,fontsize=50)
        if self.vic_mode:
            screen.draw.filled_rect(Rect((200,200), (500,500)),WHITE)
            if self.vic_:
                txt="勝利"
            else:
                txt="敗北"
            screen.draw.text(txt,(WIDTH/2-100,200),fontname='genshingothic-bold.ttf',color=BLACK,fontsize=100)
            txt=self.time.time_text()+"\nかかった時間 \n"+self.time.past_time(self.start_time)+"\n残り部隊  "+str(len(self.units_list[0].list))
            screen.draw.text(txt,(200,200+100),fontname='genshingothic-bold.ttf',color=BLACK,fontsize=50)
    def update(self,pov):
        if not self.vic_mode:
            speed=self.time.update()
            ri=sounds.ri if speed==1 else None
            while speed>0:
                self.bullets.update()
                self.bullets.set_pov(pov)
                for units in self.units_list:
                    units.update(self.bullets.list,ri)
                    units.set_pov(pov)
                speed-=1
            if self.vic_if():
                self.vic_mode=True
                self.vic_=True
            elif self.los_if():
                self.vic_mode=True
                self.vic_=False
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
                            self.date[y,x]=setd
                            self.draw_date.set_at((x,y),self.color[setd])
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
                    self.date[y,x]=setd
                    self.draw_date.set_at((x,y),self.color[setd])
        elif(xsen==0):
            if(pos[1]>go_pos[1]):
                box=pos
                pos=go_pos
                go_pos=box
            haba=int(haba)
            for y in range(pos[1],go_pos[1]):
                for x in range(pos[0]-haba,pos[0]+haba):
                    self.date[y,x]=setd
                    self.draw_date.set_at((x,y),self.color[setd])
    def en(self,pos,haba,setd):
        for y in range(pos[1]-haba,pos[1]+haba):
            for x in range(pos[0]-haba,pos[0]+haba):
                if((x-pos[0])**2+(y-pos[1])**2<=(haba/2)**2):
                    self.date[y,x]=setd
                    self.draw_date.set_at((x,y),self.color[setd])
    def daen(self,fpos,setd):
        x_min=self.rect[2]
        x_max=0
        y_min=self.rect[3]
        y_max=0
        for pos in fpos:
            if(pos[0]<x_min):
                x_min=pos[0]
            if(pos[0]>x_max):
                x_max=pos[0]
            if(pos[1]<y_min):
                y_min=pos[1]
            if(pos[1]>y_max):
                y_max=pos[1]
        xr=(x_max-x_min)/2
        yr=(y_max-y_min)/2
        cen=[(x_max+x_min)/2,(y_max+y_min)/2]
        for y in range(y_min,y_max):
            for x in range(x_min,x_max):
                siki=((x-cen[0])/xr)**2+((y-cen[1])/yr)**2
                if(siki<=1):
                    self.date[y,x]=setd
                    self.draw_date.set_at((x,y),self.color[setd])
    def sikaku(self,pos,go_pos,setd):
        for y in range(pos[1] if pos[1]<go_pos[1] else go_pos[1],go_pos[1] if pos[1]<go_pos[1] else pos[1]):
            for x in range(pos[0] if pos[0]<go_pos[0] else go_pos[0],go_pos[0] if pos[0]<go_pos[0] else pos[0]):
                self.date[y,x]=setd
                self.draw_date.set_at((x,y),self.color[setd])                          
    def all(self,setd):
        self.draw_date.fill(self.color[1],None, special_flags=0)
        self.date= np.array([[setd for i in range(self.rect[2])] for j in range(self.rect[3])])
class sityefk(Map):
    def __init__(self):
        source=pygame.image.load(os.path.join('images', 'test.png'))
        wide_rect=source.get_clip()
        super().__init__([wide_rect[2],wide_rect[3]],[43,7,3,7,30])
        self.setdate('test.png')
        self.set_unit()
    def draw(self, pov, screen):
        super().draw(pov, screen)
        if self.start_exm:
            screen.draw.filled_rect(Rect((200,200), (500,500)),WHITE)
            screen.draw.text("操作する部隊は青色です\n　クリックして始める",(200,HEIGHT/2-25),fontname='genshingothic-bold.ttf',color=BLACK,fontsize=45)
    def load(self,time,unit_list):
        pass
    def vic_if(self):
        return 0==len(self.units_list[1].list)
    def los_if(self):
        return 0==len(self.units_list[0].list)
    def set_unit(self):

        gp=ger_ply(self)
        gp.set_unit((675, 697),Kar98k_syo)
        gp.set_unit((595, 731),Kar98k_syo)
        gp.set_unit((645, 730),Kar98k_syo)
        gp.set_unit((613, 699),Kar98k_syo)
        gp.set_unit((545, 646),Kar98k_syo)
        s=sov(self)
        s.set_unit((8, 480),mosin_syo)
        s.set_unit((296, 434),mosin_syo)
        s.set_unit((361, 416),mosin_syo)
        s.set_unit((518, 422),mosin_syo)
        s.set_unit((605, 435),mosin_syo)
        s.set_unit((649, 430),mosin_syo)
        s.set_unit((785, 429),mosin_syo)
        s.set_unit((577, 359),mosin_syo)
        #プレイヤーは後ろ

        self.units_list+=[gp,s]
class heiankyou(Map):
    def __init__(self):
        source=pygame.image.load(os.path.join('images', 'heiankyou.png'))
        wide_rect=source.get_clip()
        super().__init__([wide_rect[2],wide_rect[3]],[43,7,3,7,30])
        self.setdate('heiankyou.png')
        self.set_unit()
    def draw(self, pov, screen):
        super().draw(pov, screen)
        if self.start_exm:
            screen.draw.filled_rect(Rect((200,200), (500,500)),WHITE)
            screen.draw.text("操作する部隊は青色です\n　クリックして始める",(200,HEIGHT/2-25),fontname='genshingothic-bold.ttf',color=BLACK,fontsize=45)
    def load(self,time,unit_list):
        pass
    def vic_if(self):
        return 0==len(self.units_list[1].list)
    def los_if(self):
        return 0==len(self.units_list[0].list)
    def set_unit(self):

        gp=ger_ply(self)
        gp.set_unit((679, 464),Kar98k_syo)
        gp.set_unit((660, 560),Kar98k_syo)
        gp.set_unit((617, 515),Kar98k_syo)
        gp.set_unit((656, 298),Kar98k_syo)
        gp.set_unit((616, 567),Kar98k_syo)
        s=sov(self)
        s.set_unit((119, 558),mosin_syo)
        s.set_unit((148, 627),mosin_syo)
        s.set_unit((271, 514),mosin_syo)
        #s.set_unit((274, 616),mosin_syo)
        #s.set_unit((233, 561),mosin_syo)
        #s.set_unit((216, 459),mosin_syo)
        #s.set_unit((191, 578),mosin_syo)
        s.set_unit((216, 498),mosin_syo)
        #プレイヤーは後ろ

        self.units_list+=[gp,s]
class beerui(Map):
    def __init__(self):
        super().__init__([900,900],[43,7,3,7,30])
        self.en([0,50],10,2)
        self.sen([0,50],[100,400],10,2)
        self.en([100,400],10,2)
        self.sen([100,400],[600,500],10,2)
        self.en([600,500],10,2)
        self.sen([600,500],[900,400],5,2)
        self.sen([600,500],[700,900],5,2)
        self.sikaku([250,70],[390,140],6)
        self.sen([400,0],[300,100],5,4)
        self.sen([300,100],[900,100],5,4)
        self.sen([300,100],[290,400],5,4)
        self.sen([290,400],[200,800],5,4)
        self.sen([200,800],[100,900],5,4)
        self.sen([300,0],[200,900],10,3)
        self.daen([[100,100],[200,100],[150,-100],[150,200]],5)
        self.daen([[0,400],[100,800],[150,600],[-150,700]],5)
        self.set_unit()
    def draw(self, pov, screen):
        super().draw(pov, screen)
        if self.start_exm:
            screen.draw.filled_rect(Rect((200,200), (500,500)),WHITE)
            screen.draw.text("操作する部隊は赤色です\n　クリックして始める",(200,HEIGHT/2-25),fontname='genshingothic-bold.ttf',color=BLACK,fontsize=45)
    def vic_if(self):
        return 0==len(self.units_list[1].list)
    def los_if(self):
        return 0==len(self.units_list[0].list)
    def load(self,time,unit_list):
        pass
    def set_unit(self):
        g=ger(self)
        g.set_unit((300,100),Kar98k_syo)
        g.set_unit((600,400),Kar98k_syo)
        g.set_unit((200,400),Kar98k_syo)
        sp=sov_ply(self)
        sp.set_unit((300,800),mosin_syo)
        sp.set_unit((570, 530),mosin_syo)
        sp.set_unit((65, 450),mosin_syo)
        sp.set_unit((65, 650),mosin_syo)
        #プレイヤーは後ろ
        self.units_list+=[sp,g]
maps=Maps()
start=Start()
def draw():
    start.draw()
    if start.title_mode==title_mode.execution:
        maps.draw(screen)
    
def update():
    maps.update()
def on_key_down(key):
    maps.key_down(key)
def on_mouse_down(pos,button):
    if button==mouse.LEFT or button==mouse.RIGHT:
        print(pos)
        sounds.clic.play()
        if start.title_mode==title_mode.execution:
            if maps.mouse_down(pos,button)==BACK:
                start.set_start()
        else:
            exm=start.mouse_down(pos)
            if None!=exm:
                maps.load(exm)



pgzrun.go()
