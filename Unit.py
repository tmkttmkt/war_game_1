from ast import List
from os import remove
import re
from turtle import back, width
from pgzero.actor import Actor
from pgzero.keyboard import keyboard
from pgzero.constants import mouse
from pgzero.rect import Rect
from math import fabs, sqrt,cos,sin,asin,acos,degrees
from var import *
from enu import goal,unit_type,bullet_type
from func import rerect
#from pgzero.game import screen
from rapper import call_move_func,call_withdrawal_fnuc
import random
import numpy as np
class Units:
    def __init__(self,map):
        self.list=[]
        #self.command=command
        self.map=map
        self.pov=[0,0]
    def draw(self,screen):
        for obj in self.list:
            obj.draw(screen)
    def update(self,list,ri):
        bullets=[]
        for obj in self.list:
            exm=obj.update(self.map.date,self.list,ri)
            if exm!=None:
                bullets+=exm
            for bul in list:
                if bul.unit!=obj:
                    dameg=bul.collide(obj,self.map.date[int(obj.center[1]),int(obj.center[0])])
                    if dameg!=None:
                        print(dameg)
                        obj.atacked(dameg,bul.unit)
            if obj.delete():
                self.list.remove(obj)
                del obj
        list+=bullets
    def set_unit(self,pos,unit_class):
        self.list.append(unit_class(pos))
    def set_pov(self,pov):
        for obj in self.list:
            obj.set_pov(pov)
    def mouse_down(self,pos,button):
        if button==mouse.RIGHT or button==mouse.LEFT:
            for obj in self.list:
                if obj.mouse_down_off(pos):
                    return obj
class sov_ply(Units):
    def mouse_down(self,pos,button):
        ret_obj=None
        if button==mouse.RIGHT:
            flg=False
            for obj in self.list:
                if obj.mouse_down_on(pos):
                    flg=True
                    ret_obj=obj
            if not flg:
                for obj in self.list:
                    obj.move(pos,self.pov,self.map.date)
                    obj.mouse_up()
                ret_obj=CHANGE
        elif button==mouse.LEFT:
            flg=False
            for obj in self.list:
                if obj.mouse_down_on(pos):
                    flg=True
                    ret_obj=obj
                    break
            if not flg:
                for obj in self.list:
                    obj.fire(pos)
                    obj.mouse_up()
                ret_obj=CHANGE
            else:
                for obj in self.list:
                    if obj!=ret_obj:
                        obj.mouse_up()
        return ret_obj
class ger_ply(Units):
    def mouse_down(self,pos,button):
        ret_obj=None
        if button==mouse.RIGHT:
            flg=False
            for obj in self.list:
                if obj.mouse_down_on(pos):
                    flg=True
                    ret_obj=obj
            if not flg:
                for obj in self.list:
                    obj.move(pos,self.pov,self.map.date)
                    obj.mouse_up()
                ret_obj=CHANGE
        elif button==mouse.LEFT:
            flg=False
            for obj in self.list:
                if obj.mouse_down_on(pos):
                    flg=True
                    ret_obj=obj
                    break
            if not flg:
                for obj in self.list:
                    obj.fire(pos)
                    obj.mouse_up()
                ret_obj=CHANGE
            else:
                for obj in self.list:
                    if obj!=ret_obj:
                        obj.mouse_up()
        return ret_obj
class sov(Units):
    def update(self, list,sou):
        self.AI()
        super().update(list,sou)
    def AI(self):
        for unit in self.list:
            lis=self.map.search(Rect((unit.x-100,unit.y-100),(unit.width+200,unit.height+200)))
            i=0
            de_list=[]
            for o in lis:
                for obj in self.list:
                    if o==obj:
                        de_list.append(o)
                        break
            for ob in de_list:
                lis.remove(ob)
            if len(lis)!=0:
                unit.fire(lis[0].center,True)
            else:
                unit.goal=goal.defense
            if len(unit.atacked_unit)>2 and not unit.back_flg:
                unit.withdrawal(self.map.date,self.list)
class ger(Units):
    def update(self, list,sou):
        self.AI()
        super().update(list,sou)
    def AI(self):
        for unit in self.list:
            lis=self.map.search(Rect((unit.x-100,unit.y-100),(unit.width+200,unit.height+200)))
            i=0
            de_list=[]
            for o in lis:
                for obj in self.list:
                    if o==obj:
                        de_list.append(o)
                        break
            for ob in de_list:
                lis.remove(ob)
            if len(lis)!=0:
                unit.fire(lis[0].center,True)
            else:
                unit.goal=goal.defense
            if len(unit.atacked_unit)>2 and not unit.back_flg:
                unit.withdrawal(self.map.date,self.list)
class Unit(Actor):
    def __init__(self,pos,speed,armor,soldier,morale,hei,type:unit_type):
        super().__init__('sol_syo',center=pos)
        self.mouse=False
        self.goal=goal.defense
        self.point_list=[]
        self.back_list=[]
        self.fire_point=(-1,-1)
        self.nokori=(-1,-1)
        self.back_nokori=(-1,-1)
        self.name="NULL"

        self.type=type
        self.speed=speed
        self.armor=armor
        self.soldier=soldier
        self.MAX_morale=morale
        self.morale=morale
        self.hei=hei
        self.time=0
        self.guns=[]
        self.atacked_unit=[]
        self.back_flg=False
    def delete(self):
        if self.soldier<=0:
            return True
        return False
    def atacked(self,damag,uni):
        self.soldier-=damag[0]
        self.morale-=damag[1]
        flg=True
        for o in self.atacked_unit:
            if o[0]==uni:
                flg=False
        if flg:
            self.atacked_unit.append([uni,10])
    def set_pov(self,pov):
        self.x+=pov[0]
        self.y+=pov[1]
    def draw(self,screen):
        super().draw()
        if self.mouse:
            screen.draw.circle(self.center,10, (255,0,0))
    def fire(self,pos,flg=False):
        if self.mouse or flg:
            self.point_list=[]
            self.fire_point=pos
            self.goal=goal.fire
        return False
    def withdrawal(self,date,lit):
        self.point_list=[]
        self.back_flg=True
        out=[]
        for uni in self.atacked_unit:
            flg=True
            for obj in lit:
                if uni[0]==obj:
                    flg=False
            if flg:
                out+=[[int(uni[0].center[0]),int(uni[0].center[1])]]
        if len(out)!=0:
            self.back_list=call_withdrawal_fnuc(date,self.center,np.array(out),len(out))
        else:
            for uni in self.atacked_unit:
                out+=[[int(uni[0].center[0]),int(uni[0].center[1])]]
            if len(out)!=0:
                self.back_list=call_withdrawal_fnuc(date,self.center,np.array(out),len(out))
            else:
                return
        if len(self.back_list)<2:
            self.back_list=[]
            self.back_flg=False

    def mouse_down_on(self,pos):
        if self.collidepoint(pos):
            self.mouse=True
            return True
        return False
    def mouse_down_off(self,pos):
        return self.collidepoint(pos)
    def mouse_up(self):
        self.mouse=False
    def move(self,pos,pov,date):
        if self.mouse:
            self.goal=goal.move
            self.point_list=call_move_func(date,self.center,pos,pov)
    def update(self,date,lit,ri):
        if not self.back_flg:
            for gun in self.guns:
                gun.update()
        self.time+=1
        if self.time>=180:
            self.time-=180
            for state in self.atacked_unit:
                state[1]-=1
                if state[1]<0:
                    self.atacked_unit.remove(state)
            if self.MAX_morale>self.morale:
                self.morale+=1
            else:
                self.morale=self.MAX_morale
        if self.back_flg:
            if 0<len(self.back_list):
                #print(self.nokori)
                if self.back_nokori==(-1,-1):
                    nokori=0
                else:
                    nokori=sqrt((self.back_nokori[0])**2+(self.back_nokori[1])**2)
                    #print("a",self.back_nokori,(self.x,self.y))
                while(0<len(self.back_list)):
                    back_speed=self.speed*0.7
                    if nokori>back_speed:
                        x=(nokori-back_speed)*(self.back_nokori[0]/nokori)
                        y=(nokori-back_speed)*(self.back_nokori[1]/nokori)
                        self.back_nokori=(x,y)
                        #print("b",(back_spee-(nokori-sya)),self.back_nokori)
                        break
                    li=self.back_list.pop(0)
                    sya=sqrt(li[0]**2+li[1]**2)
                    syaka=sya
                    pos=(int(self.center[0]+li[0]),int(self.center[1]+li[1]))
                    if pos[0]>=900 or pos[1]>=900:
                        print("で",pos)
                        self.back_list=[]
                        break
                    sta=date[pos[1],pos[0]]
                    #0mu 1heiya 2kawa 3tetudou 4douro 5mori 6mati
                    if sta==2:
                        sya*=50
                    elif sta==5 or sta==6:
                        sya*=2
                    elif sta==2 or sta==3:
                        sya*=0.5
                    nokori+=sya
                    self.x+=li[0]
                    self.y+=li[1]
                    if nokori>back_speed:
                        x=(nokori-back_speed)*(li[0]/syaka)
                        y=(nokori-back_speed)*(li[1]/syaka)
                        self.back_nokori=(x,y)
                        #print("b",(back_spee-(nokori-sya)),self.back_nokori)
                        break
                    elif nokori==back_speed:
                        self.back_nokori=(-1,-1)
                        break
                    #print(li,(self.x,self.y))
            else:
                self.back_flg=False
                self.morale+=round((100-self.morale)/2)
                self.goal=goal.defense
                self.back_nokori=(-1,-1)
        elif self.morale<0:
            self.withdrawal(date,lit)
        elif self.goal==goal.move:
            if 0<len(self.point_list):
                #print(self.nokori)
                if self.nokori==(-1,-1):
                    nokori=0
                else:
                    nokori=sqrt((self.nokori[0])**2+(self.nokori[1])**2)
                    #print("a",self.nokori,(self.x,self.y))
                while(0<len(self.point_list)):
                    if nokori>self.speed:
                        x=(nokori-self.speed)*(self.nokori[0]/nokori)
                        y=(nokori-self.speed)*(self.nokori[1]/nokori)
                        self.nokori=(x,y)
                        #print("b",(self.speed-(nokori-sya)),self.nokori)
                        break
                    li=self.point_list.pop(0)
                    sya=sqrt(li[0]**2+li[1]**2)
                    syaka=sya
                    pos=(int(self.center[0]+li[0]),int(self.center[1]+li[1]))
                    print(pos,self.center,li,len(self.point_list))
                    sta=date[pos[1],pos[0]]
                    #0mu 1heiya 2kawa 3tetudou 4douro 5mori 6mati
                    if sta==2:
                        sya*=50
                        print(pos)
                    elif sta==5 or sta==6:
                        sya*=2
                    elif sta==2 or sta==3:
                        sya*=0.5
                    nokori+=sya
                    self.x+=li[0]
                    self.y+=li[1]
                    if nokori>self.speed:
                        x=(nokori-self.speed)*(li[0]/syaka)
                        y=(nokori-self.speed)*(li[1]/syaka)
                        self.nokori=(x,y)
                        #print("b",(self.speed-(nokori-sya)),self.nokori)
                        break
                    elif nokori==self.speed:
                        self.nokori=(-1,-1)
                        break
                    #print(li,(self.x,self.y))
            else:
                self.goal=goal.defense
                self.nokori=(-1,-1)
        elif self.goal==goal.speed_move:
            pass
        elif self.goal==goal.defense:
            unit_list=self.atacked_unit.copy()
            li=[]
            for unit in unit_list:
                for obj in lit:
                    if unit[0]==obj:
                        li.append(unit)
            for s in li:
                unit_list.remove(s)
            if 0!=len(unit_list):
                bullets=[]
                n=0
                flg=random.randint(0,10)%60==0 and ri!=None
                for gun in self.guns:
                    if n>=self.soldier:
                        break
                    n+=1
                    if gun.can:
                        um=random.randint(0,len(unit_list)-1)
                        point=unit_list[um][0].center
                        """
                        if self.center[0]<point[0]:
                            x=point[0]+self.atacked_unit[um][0].width/2
                        else:
                            x=point[0]-self.atacked_unit[um][0].width/2
                        if self.center[1]<point[1]:
                            y=point[1]+self.atacked_unit[um][0].height/2
                        else:
                            y=point[1]-self.atacked_unit[um][0].height/2
                        bul=gun.fire(self.center,(x,y),self)
                        """
                        if flg:
                            ri.play()
                            flg=False
                        bul=gun.fire(self.center,point,self)
                        if bul!=None:
                            bullets.append(bul)
                return bullets
        elif self.goal==goal.fire:
            if self.fire_point!=(-1,-1):
                bullets=[]
                n=0
                flg=random.randint(0,20)%60==0 and ri!=None
                for gun in self.guns:
                    if n>=self.soldier:
                        break
                    n+=1
                    if gun.can:
                        if flg:
                            ri.play()
                            flg=False
                        bul=gun.fire(self.center,self.fire_point,self)
                        if bul!=None:
                            bullets.append(bul)
                return bullets
            else:
                self.goal=goal.defense
        elif self.goal==goal.precision_fire:
            pass
class test_syo(Unit):
    def __init__(self,pos):
        super().__init__(pos,2,0,12,100,2,unit_type.infantry)
        i=1
        while i>0:
            self.guns.append(Mosin_Nagant())
            i-=1
    def draw(self, screen):
        screen.draw.filled_rect(Rect((self.topleft[0]-2,self.topleft[1]-2), (self.width+4,self.height+4)),RED)
        super().draw(screen)
class mosin_syo(Unit):
    def __init__(self, pos):
        super().__init__(pos,2,0,12,100,2,unit_type.infantry)
        self.name="モシン分隊"
        self.guns.append(DP28())
        i=13
        while i>0:
            self.guns.append(Mosin_Nagant())
            i-=1
    def draw(self, screen):
        screen.draw.filled_rect(Rect((self.topleft[0]-2,self.topleft[1]-2), (self.width+4,self.height+4)),RED)
        super().draw(screen)
class Kar98k_syo(Unit):
    def __init__(self, pos):
        super().__init__(pos,2,0,12,100,2,unit_type.infantry)
        self.name="カービン98分隊"
        self.guns.append(MG34())
        i=11
        while i>0:
            self.guns.append(Kar98k())
            i-=1
    def draw(self, screen):
        screen.draw.filled_rect(Rect((self.topleft[0]-2,self.topleft[1]-2), (self.width+4,self.height+4)),BLUE)
        super().draw(screen)
class Gun:
    def __init__(self,cal,explo,penet,wei,ran,inter,speed,hei,bul,sou):
        self.caliber=cal
        self.explosive=explo
        self.penetration=penet
        self.weight=wei
        self.range=ran
        self.interval=inter
        self.bullet_speed=speed
        self.height=hei
        self.time=0
        self.bullet=bul
        self.can=False
        self.sou_max=sou[0]
        self.sou=0
        self.sou_interval=sou[1]
    def update(self):
        if not self.can:
            self.time+=1
            if self.sou>=self.sou_max:
                if self.sou_interval<self.time:
                    self.time=0
                    self.sou=0
            elif self.interval<self.time:
                self.time=0
                self.can=True
    def fire(self,loc,pos,uni):
        speed=self.bullet_speed*TIME_SCL
        sya=sqrt((loc[0]-pos[0])**2+(loc[1]-pos[1])**2)
        tate_kaku=G*sya/speed**2
        if tate_kaku>1:
            tate_kaku=1
        tate_seeta=asin(tate_kaku)/2
        if degrees(tate_kaku)>20:
            return
        tate_seeta+=random.gauss(0,tate_kaku*tate_kaku/10)
        yx_speed=speed*cos(tate_seeta)
        seeta=acos((pos[0]-loc[0])/sya)
        seeta+=random.gauss(0,0.1)
        speed_x=yx_speed*cos(seeta)
        speed_y=yx_speed*sin(seeta)
        if pos[1]-loc[1]<0:
            speed_y*=-1
        speed_z=speed*sin(tate_seeta)
        speed=[speed_x,speed_y,speed_z]
        self.time=0
        self.sou+=1
        self.can=False
        return Bullet(self.caliber,loc,self.height+1,speed,self.bullet,uni)
class Mosin_Nagant(Gun):
    def __init__(self):
        super().__init__(7.62,0,5,9.7,400,FPS_SCL*(12+random.gauss(0,4)),810*random.gauss(1,0.1),1.5,bullet_type.rifles,(5,7*FPS_SCL))
class DP28(Gun):
    def __init__(self):
        super().__init__(7.62,0,5,9.7,800,FPS_SCL*1/10,840*random.gauss(1,0.1),0.3,bullet_type.ki_rifles,(47,10*FPS_SCL))
class Kar98k(Gun):
    def __init__(self):
        super().__init__(7.92,0,5,9.9,500,FPS_SCL*(12+random.gauss(0,4)),760*random.gauss(1,0.1),1.5,bullet_type.rifles,(5,6*FPS_SCL))
class MG34(Gun):
    def __init__(self):
        super().__init__(7.92,0,5,9.9,700,FPS_SCL*60/800,755*random.gauss(1,0.1),0.3,bullet_type.ki_rifles,(50,13*FPS_SCL))
class Bullet(Actor):
    def __init__(self,cal,pos,hei,speed,type:bullet_type,uni) -> None:
        if type==bullet_type.ki_rifles:
            super().__init__('ki',center=pos)
        else:
            super().__init__('ho',center=pos)
        self.caliber=cal
        self.past=(0,0)
        self.type=type
        self.z=hei
        self.speed=speed
        self.unit=uni
        self.time=0
    def update(self):
        #self.speed[0]+=0.25*self.caliber/1000*self.speed[0]**2*(1 if self.speed[0]<0 else -1)
        #self.speed[1]+=0.25*self.caliber/1000*self.speed[1]**2*(1 if self.speed[1]<0 else -1)
        self.past=(self.x,self.y)
        self.x+=self.speed[0]
        self.y+=self.speed[1]
        self.speed[2]-=G
        self.z+=self.speed[2]
        self.time+=1
        print(self.speed,self.center,self.z)
                            #sol,mora
    def collide(self,obj,sta):
        ex=Rect(self.center,(self.past[0]-self.center[0],self.past[1]-self.center[1]))
        ex=rerect(ex)
        if obj.colliderect(ex):
            print("b",self.z)
            if self.z<obj.hei:
                if obj.type==unit_type.infantry:
                    #0mu 1heiya 2kawa 3tetudou 4douro 5mori 6mati
                    if sta==2:
                        a=1
                    elif sta==5 or sta==6:
                        a=7
                    else:
                        a=2
                    if a>=random.randint(1,10):
                        if self.type==bullet_type.rifles: 
                            return (1,3)
                        elif self.type==bullet_type.ki_rifles:
                            return (1,5)
                        elif self.type==bullet_type.AP:
                            return (1,15)
                        elif self.type==bullet_type.HE:
                            return (3,40)
                    else:
                        return (0,1)
            else:
                return (0,1)
    def set_pov(self,pov):
        self.x+=pov[0]
        self.y+=pov[1]
class Bullets:
    def __init__(self,map):
        self.map=map
        self.list=[]
    def draw(self):
        for bul in self.list:
            bul.draw()
    def update(self):
        for bul in self.list:
            bul.update()
            pos=bul.center
            if pos[0]<0 or pos[1]<0 or pos[1]>=899.5 or pos[0]>=899.5:
                li=self.map.search(Rect((bul.center[0]-10,bul.center[1]-10),(bul.center[0]+20,bul.center[1]+20)))
                if len(li)!=0:
                    for obj in li:
                        dameg=bul.collide(obj,self.map.date[int(obj.center[1]),int(obj.center[0])])
                        if dameg!=None:
                            print(dameg)
                            obj.atacked(dameg,bul.unit)
                self.list.remove(bul)
            elif bul.time>1:
                pos=(int(round(pos[0])),int(round(pos[1])))
                sta=self.map.date[pos[1],pos[0]]
                #0mu 1heiya 2kawa 3tetudou 4douro 5mori 6mati
                if sta==2:
                    if bul.z<-1:
                        self.list.remove(bul)
                        continue
                else:
                    if bul.z<0:
                        self.list.remove(bul)
                        continue
                if sta==5:
                    if bul.z<20:
                        if 1==random.randint(1,10):
                            self.list.remove(bul)
                            continue
                elif sta==6:
                    if 1==random.randint(1,4):
                        self.list.remove(bul)
                        continue   
    def set_pov(self,pov):
        for obj in self.list:
            obj.set_pov(pov)
class Unit_state:
    def __init__(self,unit:Unit):
        self.unit=unit
    def draw(self,screen):
        screen.draw.filled_rect(Rect((200,HEIGHT-200), (WIDTH-200*2,200)),WHITE)
        screen.draw.text(self.text(),(200,HEIGHT-200),fontname='genshingothic-bold.ttf',color=BLACK,fontsize=30)
        screen.draw.text(self.gun_text(),(200,HEIGHT-200+30),fontname='genshingothic-bold.ttf',color=BLACK,fontsize=15)
    def gun_text(self):
        txt=""
        for gun in self.unit.guns:
            txt+=gun.__class__.__name__
            txt+="  残弾数:"+str(gun.sou_max-gun.sou)
            if gun.sou_max-gun.sou!=0:
                if gun.can:
                    txt+="  装填"+"100%"
                else:
                    txt+="  装填 "+str(int(gun.time/gun.interval*100))+"%"
            else:
                txt+="装填残り"+str(int((gun.sou_interval-gun.time)/60))+"秒"
            txt+="\n"
        return txt
    def text(self):
        return self.unit.name+"　兵数："+str(self.unit.soldier)+"  士気："+str(self.unit.morale)







