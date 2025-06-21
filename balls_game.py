
import state
import pygame, sys, random
from pygame.locals import *


pygame.init()


# Initialize basic variables
white=(255,255,255)
black=(0,0,0)
background=(0,150,150) # Random color 
FPS=100



class BallGame():
    def __init__(self):
        pass
    def var_ini(self, w,h):
        
        rad_main=20
        rad_main_dec=rad_main//10
        radini=3
        radfin=8
        nvel=5 # Speed 
        t=0 # Time counter
        m=1.5 # Size of hidden screen
        nc=5 # Number circles in screen
        score=0    
        
        execute=True
        
        l=[]
        lcirc=[]
        lcol=[]
        n=random.randint(4,20)
        for e in range(n):
            lcirc.append(Ball(w,h,radini,radfin,nvel,m))
            lcol.append(tuple([random.randint(50,255)]+[random.randint(0,255)]+[random.randint(0,255)]))
        for e in range(len(lcirc)):
            l.append([lcirc[e],lcol[e],t])

        return rad_main,rad_main_dec,radini,radfin,nvel,t,m,nc,score,execute,l,lcirc,lcol,n
       
    def Main(self): # Main loop 
        w, h = state.state["game_size"]
        screen=state.state["screen"]
        rad_main,rad_main_dec,radini,radfin,nvel,t,m,nc,score,execute,l,lcirc,lcol,n=self.var_ini(w,h)
        record=0
        GAMEOVER=0
        running ='INIT'

        while execute:
            ls=[]
            if running =='INIT':
                screen.fill(background)
                dificulty=state.state["language"]["low"]
                font= pygame.font.SysFont('Arial', h//8, True)
                font2= pygame.font.SysFont('Arial', h//18, True)
                if ((t//(FPS/3))%2)==0: # Blink to select
                    text5 = font.render(state.state["language"]["START"], True, (0,0,0),(50,200,200)) 
                else:
                    text5 = font.render(state.state["language"]["START"], True, (0,0,0)) 
                text_rect5 = text5.get_rect(center=(w/2, h*(35/100)))
                screen.blit(text5, text_rect5)
                
                text6 = font.render(state.state["language"]["difficulty"] + dificulty, True, (0,0,0))
                text_rect6 = text6.get_rect(center=(w/2, h*(55/100)))
                screen.blit(text6, text_rect6)
                
                text7 = font2.render(state.state["language"]["escape"], True, (255,255,255))
                text_rect7 = text7.get_rect(center=(w/2, h*(85/100)))
                screen.blit(text7, text_rect7)
                
                for event in pygame.event.get():
                    if event.type==QUIT:
                        pygame.quit()
                        sys.exit()                 
                    if  (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        return int(record)
                    elif (event.type==pygame.KEYDOWN and event.key == pygame.K_SPACE) or (text_rect5.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1): 
                            running =True

            elif running =='RESET': # Reset of variables
                screen.fill(background)
                l=[]
                running =True
                rad_main,rad_main_dec,radini,radfin,nvel,t,m,nc,score,execute,l,lcirc,lcol,n=self.var_ini(w,h)

            elif running ==True: 
                GAMEOVER=0
                screen.fill(background)
                pos_cursor=pygame.mouse.get_pos()
                for e in l: 
                    pygame.draw.circle(screen,e[1],(e[0].x,e[0].y),e[0].radius)
                    e[0].new_pos()
                    e[2]+=1
                    if e[0].radius<=rad_main:
                        if (e[0].x-e[0].radius<=pos_cursor[0]-rad_main<=e[0].x+e[0].radius and (e[0].y-e[0].radius<=pos_cursor[1]-rad_main<=e[0].y+e[0].radius or e[0].y-e[0].radius<=pos_cursor[1]+rad_main<=e[0].y+e[0].radius)) or (e[0].x-e[0].radius<=pos_cursor[0]+rad_main<=e[0].x+e[0].radius and (e[0].y-e[0].radius<=pos_cursor[1]-rad_main<=e[0].y+e[0].radius or e[0].y-e[0].radius<=pos_cursor[1]+rad_main<=e[0].y+e[0].radius)):
                            ls=ls+[e]
                            rad_main+=1
                            score+=1
                    else: 
                        if (e[0].x-e[0].radius<=pos_cursor[0]-rad_main<=e[0].x+e[0].radius and (e[0].y-e[0].radius<=pos_cursor[1]-rad_main<=e[0].y+e[0].radius or e[0].y-e[0].radius<=pos_cursor[1]+rad_main<=e[0].y+e[0].radius)) or (e[0].x-e[0].radius<=pos_cursor[0]+rad_main<=e[0].x+e[0].radius and (e[0].y-e[0].radius<=pos_cursor[1]-rad_main<=e[0].y+e[0].radius or e[0].y-e[0].radius<=pos_cursor[1]+rad_main<=e[0].y+e[0].radius)):
                            running =False
                        
                    if (e[0].x-e[0].radius>w or e[0].y-e[0].radius>h) and e[2]>300: # Time before circle disappears
                        ls=ls+[e]
                for e in ls:
                    l.remove(e)
                if rad_main//10==rad_main_dec+1: 
                    radini+=2
                    radfin+=2
                    rad_main_dec+=1
                    if radfin>30:
                        nc=4
                if len(l)<nc: 
                    n=random.randint(1,5)
                    while n!=0:
                        l.append([Ball(w,h,radini,radfin,nvel,m),tuple([random.randint(0,255)]+[random.randint(0,255)]+[random.randint(0,255)]),0])
                        n=n-1
                if t>600: 
                    nvel+=1
                    if nvel>50:
                        m=m*5
                    t=0
                pygame.draw.circle(screen,(255,0,0),pos_cursor,rad_main)      


            elif running ==False: 
                if record<score:
                    record=score
                GAMEOVER=1
                
                font = pygame.font.SysFont("Arial", h//8)
                font2= pygame.font.SysFont('Arial', h//18, True)

                img1 = font.render('GAME OVER', True, (0,0,0))
                img2 = font.render('Score    '+str(score), True, (0,0,0))
                img3 = font.render('Record   '+str(record), True, (0,0,0))

                rect1=img1.get_rect(center=(w*(1/2), h*(25/100)))
                rect2=img2.get_rect(center=(w*(1/2), h*(40/100)))
                rect3=img3.get_rect(center=(w*(1/2), h*(55/100)))

                screen.blit(img1, rect1)
                screen.blit(img2, rect2)
                screen.blit(img3, rect3)
                
                text7 = font2.render(state.state["language"]["escape"], True, (255,255,255))
                text8 = font2.render(state.state["language"]["space"], True, (255,255,255))
                text_rect7 = text7.get_rect(center=(w/2, h*(78/100)))
                text_rect8 = text8.get_rect(center=(w/2, h*(87/100)))
                screen.blit(text7, text_rect7)
                screen.blit(text8, text_rect8)

                    
            t+=1
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()                 
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return int(record)
                if GAMEOVER==1:
                    if event.type==pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            running ='RESET'
            pygame.display.update()
            pygame.time.Clock().tick(FPS) 


# Class for circles
class Ball():
    def __init__(self,w,h,radini,radfin,nvel,m):
        
        if random.random()<0.5:
            self.x=random.randint(w,int(w*m))
            self.y=random.randint(0,int(h*m))
        else:
            self.x=random.randint(0,int(w*m))
            self.y=random.randint(h,int(h*m))
        self.velx=(-1)**random.randint(0,2)
        self.vely=(-1)**random.randint(0,2)
        self.radius = random.randint(radini,radfin)*5
        self.h=int(h*m)
        self.w=int(w*m)
        self.nvel=nvel
        self.m=m
    
    def new_pos(self):
        if self.y+self.radius>=self.h:
            self.vely=-1
            self.y=self.h-self.radius
        elif self.y-self.radius<=0:
            self.vely=1
            self.y=self.radius
        if self.x+self.radius>=self.w :
            self.velx=-1
            self.x=self.w-self.radius
        elif self.x-self.radius<=0:
            self.velx=1
            self.x=self.radius
        self.x=self.x+self.velx*self.nvel
        self.y=self.y+self.vely*self.nvel    





