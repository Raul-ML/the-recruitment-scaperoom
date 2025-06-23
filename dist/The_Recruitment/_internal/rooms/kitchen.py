import state
import loader
import pygame
import sys
import ui.dialogue as dialogue
import ui.arrows as arrows



class Kitchen:
    def __init__(self):
        self.FPS=60
        self.mouse_in_tomato=False
        self.mouse_in_red_key=False

    def render(self):
        self.screen=state.state["screen"]
        self.w, self.h= state.state["game_size"]
        self.language=state.state["language"]
        
        bckg= pygame.transform.scale(loader.bckg_kitchen, (self.w,self.h))
        self.screen.blit(bckg, (0, 0))

        fridge_rect=pygame.Rect(self.w*(33/100), self.h*(33/100), self.w*(15/100), self.h*(26/100))
        self.mouse_in_fridge=fridge_rect.collidepoint(state.state["pos_cursor"])
        
        list_rect=pygame.Rect(self.w*(38/100), self.h*(23/100), self.w*(8/100), self.h*(8/100))
        self.mouse_in_list=list_rect.collidepoint(state.state["pos_cursor"])
        
        # safe_rect=pygame.Surface((self.w*(15/100), self.h*(26/100)), pygame.SRCALPHA)
        # safe_rect.fill((255,0,0,150))
        # self.screen.blit(safe_rect, (self.w*(33/100), self.h*(33/100)))

        pos=pygame.mouse.get_pos()
        arrows.arrows(pos)

        if state.state["substage"]=="waiting":
            state.var_ini()
            state.state["substage"]=""

        elif state.state["substage"]=="fridge":
            dialogue.msgbox(state.state["language"]["fridge"],"", True, True)
        elif state.state["substage"]=="fridge1":
            done=dialogue.msgbox(state.state["language"]["fridge1"],"", True, False)
            if done:
                state.state["substage"]="waiting"
            fridge_bckg=pygame.transform.scale(loader.bckg_fridge, (self.w*(40/100),self.h*(70/100)))
            self.screen.blit(fridge_bckg, (self.w*(30/100), self.h*(0/100)))
            if not state.state["tomato"]:
                tomato=pygame.transform.scale(loader.tomato, (self.w*(6/100),self.h*(21/100)))
                tomato_rect=tomato.get_rect(topleft=(self.w*(51/100), self.h*(26/100)))
                self.mouse_in_tomato=tomato_rect.collidepoint(state.state["pos_cursor"])
                self.screen.blit(tomato, tomato_rect)
            if not state.state["key_red"] and state.state["tomato"]:
                red_key=pygame.transform.scale(loader.key_red, (self.w*(5/100),self.h*(10/100)))
                red_key_rect=red_key.get_rect(topleft=(self.w*(52/100), self.h*(35/100)))
                self.mouse_in_red_key=red_key_rect.collidepoint(state.state["pos_cursor"])
                self.screen.blit(red_key, red_key_rect)
            
        elif state.state["substage"]=="list":
            done=dialogue.msgbox(state.state["language"]["list"],"", True, True)
        elif state.state["substage"]=="list1":
            done=dialogue.msgbox(state.state["language"]["list1"],"", True, False)
            if done:
                state.state["substage"]="waiting"
        
        self.handle_events()
    def handle_events(self):
        pos_cursor=pygame.mouse.get_pos()
        state.state["pos_cursor"]=pos_cursor

        if state.state["substage"]=="":
            if self.mouse_in_fridge:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
            elif self.mouse_in_list:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
        elif state.state["substage"]=="fridge1":
            if self.mouse_in_tomato and not state.state["tomato"]:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
            if self.mouse_in_red_key and not state.state["key_red"]:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
                
            
        if state.state["game_in"]=="kitchen":
                    
            for event in state.state["events"]:
                keys = pygame.key.get_pressed() # Alternative way to detect keys pressed, it detects key pressed continously
                is_click = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                is_key = event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE) 
                if event.type == pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                    state.state["substage"]=""
                if state.state["substage"]=="":
                    if self.mouse_in_fridge and is_click:
                        state.state["substage"]="fridge"
                    if self.mouse_in_list and is_click:
                        state.state["substage"]="list"
                elif state.state["substage"]=="fridge1":
                    if self.mouse_in_tomato and is_click:
                        state.state["tomato"]=True
                    if self.mouse_in_red_key and is_click:
                        state.state["key_red"]=True
                        # state.state["substage"]="waiting"
                        

                if state.state["substage"]=="list":
                    if ((state.state["selec_position"]=="left" and is_key) or  (self.w*(30/100)<pos_cursor[0]<self.w*(38/100) and self.h*(85/100)<pos_cursor[1]<self.h*(92/100) and is_click)):
                        state.var_ini()
                        state.state["substage"]="list1"
                    elif (state.state["selec_position"]=="right" and is_key) or (self.w*(60/100)<pos_cursor[0]<self.w*(68/100) and self.h*(85/100)<pos_cursor[1]<self.h*(92/100) and is_click):
                        state.var_ini()
                        state.state["substage"]="waiting"

                elif state.state["substage"]=="fridge":
                    if ((state.state["selec_position"]=="left" and is_key) or  (self.w*(30/100)<pos_cursor[0]<self.w*(38/100) and self.h*(85/100)<pos_cursor[1]<self.h*(92/100) and is_click)):
                        state.var_ini()
                        state.state["substage"]="fridge1"
                    elif (state.state["selec_position"]=="right" and is_key) or (self.w*(60/100)<pos_cursor[0]<self.w*(68/100) and self.h*(85/100)<pos_cursor[1]<self.h*(92/100) and is_click):
                        state.var_ini()
                        state.state["substage"]="waiting"

            
