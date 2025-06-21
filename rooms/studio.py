import state
import loader
import pygame
import sys
import ui.dialogue as dialogue
import ui.arrows as arrows



class Studio:
    def __init__(self):
        self.FPS=60


    def render(self):
        self.screen=state.state["screen"]
        self.w, self.h= state.state["game_size"]

        self.bckg= pygame.transform.scale(loader.bckg_studio_carpet, (self.w,self.h))
        self.bckg_no_carpet= pygame.transform.scale(loader.bckg_studio_no_carpet, (self.w,self.h))
        if not state.state["carpet_removed"]:
            self.screen.blit(self.bckg, (0, 0))
        elif  state.state["carpet_removed"]:
            self.screen.blit(self.bckg_no_carpet, (0, 0))
            
        self.rollers= pygame.transform.scale(loader.rollers, (self.w*(15/100),self.h*(25/100)))
        rollers_rect=self.rollers.get_rect(topleft=(self.w*(75/100), self.h*(40/100)))
        self.mouse_in_rollers=rollers_rect.collidepoint(state.state["pos_cursor"])
        self.screen.blit(self.rollers, rollers_rect)
            
        music_rect=pygame.Rect(self.w*(9/100), self.h*(37/100), self.w*(20/100), self.h*(23/100))
        self.mouse_in_music=music_rect.collidepoint(state.state["pos_cursor"])
        
        hole_basement=pygame.Rect(self.w*(30/100), self.h*(63/100), self.w*(45/100), self.h*(20/100))
        self.mouse_in_hole=hole_basement.collidepoint(state.state["pos_cursor"])
        
        books=pygame.Rect(self.w*(83/100), self.h*(20/100), self.w*(17/100), self.h*(15/100))
        self.mouse_in_books=books.collidepoint(state.state["pos_cursor"])
        
        # rect=pygame.Surface((self.w*(17/100), self.h*(15/100)), pygame.SRCALPHA)
        # rect.fill((255,0,0,150))
        # self.screen.blit(rect, (self.w*(83/100), self.h*(20/100)))

        pos=pygame.mouse.get_pos()
        arrows.arrows(pos)

        if state.state["substage"]=="waiting":
            state.state["substage"]=""

        if state.state["substage"]=="music":
            done=dialogue.msgbox(state.state["language"]["music"],"", True, True)
        
        if state.state["substage"]=="rollers":
            done=dialogue.msgbox(state.state["language"]["rollers"],"", True, True)

        elif state.state["substage"]=="rollers1":
            done=dialogue.msgbox(state.state["language"]["rollers1"],"", True, False)
            if done:
                state.state["substage"]="waiting"
        
        elif state.state["substage"]=="books":
            done=dialogue.msgbox(state.state["language"]["books"],"", True, False)
            if done:
                state.state["substage"]="waiting"
        
        self.handle_events()
    def handle_events(self):
        pos_cursor=pygame.mouse.get_pos()
        state.state["pos_cursor"]=pos_cursor

        if state.state["substage"]=="":
            if self.mouse_in_rollers:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
            if self.mouse_in_hole and state.state["carpet_removed"]==True:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
            if self.mouse_in_music:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
            if self.mouse_in_books:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 

        for event in state.state["events"]:
            keys = pygame.key.get_pressed() # Alternative way to detect keys pressed, it detects key pressed continously
            
            if state.state["game_in"]=="studio":
                    
                is_click = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                is_key = event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE) 
                if event.type == pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                    state.var_ini()
                    self.code=""
                    state.state["substage"]=""
                if state.state["substage"]=="":
                    if self.mouse_in_rollers and is_click:
                        state.var_ini()
                        state.state["substage"]="rollers"
                    elif self.mouse_in_music and is_click:
                        state.var_ini()
                        state.state["substage"]="music"
                    elif self.mouse_in_hole and is_click and state.state["carpet_removed"]==True:
                        state.var_ini()
                        state.state["game_in"]="basement"
                    elif self.mouse_in_books and is_click:
                        state.var_ini()
                        state.state["substage"]="books"
                        
                if state.state["substage"]=="rollers":
                    if ((state.state["selec_position"]=="left" and is_key) or  (self.w*(30/100)<pos_cursor[0]<self.w*(38/100) and self.h*(85/100)<pos_cursor[1]<self.h*(92/100) and is_click) ):
                        state.var_ini()
                        state.state["substage"]="rollers1"
                    elif (state.state["selec_position"]=="right" and is_key) or (self.w*(60/100)<pos_cursor[0]<self.w*(68/100) and self.h*(85/100)<pos_cursor[1]<self.h*(92/100) and is_click):
                        state.var_ini()
                        self.code=""
                        state.state["substage"]=""

                if state.state["substage"]=="music":
                    if ((state.state["selec_position"]=="left" and is_key) or  (self.w*(30/100)<pos_cursor[0]<self.w*(38/100) and self.h*(85/100)<pos_cursor[1]<self.h*(92/100) and is_click) ):
                        state.var_ini()
                        state.state["play_music"]=True                  
                        state.state["substage"]=""
                    elif (state.state["selec_position"]=="right" and is_key) or (self.w*(60/100)<pos_cursor[0]<self.w*(68/100) and self.h*(85/100)<pos_cursor[1]<self.h*(92/100) and is_click):
                        state.var_ini()
                        self.code=""
                        state.state["substage"]=""

