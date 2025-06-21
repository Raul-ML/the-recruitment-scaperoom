import state
import loader
import pygame
import sys
import ui.dialogue as dialogue
import ui.arrows as arrows
import ui.background as background

class Living:
    def __init__(self):
        self.FPS=60
        self.code=""
    def render(self):
        self.screen=state.state["screen"]
        self.w, self.h= state.state["game_size"]
        self.bckg= pygame.transform.scale(loader.bckg_living_room, (self.w,self.h))
        self.button = pygame.transform.scale(loader.button, (self.w*(15/100),self.h*(11/100)))
        self.screen.blit(self.bckg, (0, 0))

        if state.state["safe_opened"]:
            self.screen.blit(self.button, (self.w*(51/100),self.w*(26/100)))

        self.basketball= pygame.transform.scale(loader.basketball, (self.w*(12/100),self.h*(20/100)))
        self.yellow_key=pygame.transform.scale(loader.key_yellow, (self.w/22,self.h/15))
        
        basketball_rect=self.basketball.get_rect(topleft=(self.w*(16/100), self.h*(73/100)))
        yellow_key_rect=self.yellow_key.get_rect(topleft=(self.w*(86/100), self.h*(30/100)))
        pictures_rect=pygame.Rect(self.w*(30/100), self.h*(36/100),self.w*(20/100), self.h*(20/100))
        
        self.mouse_in_basketball=basketball_rect.collidepoint(state.state["pos_cursor"])
        self.mouse_in_yellow_key=yellow_key_rect.collidepoint(state.state["pos_cursor"])
        self.mouse_in_pictures=pictures_rect.collidepoint(state.state["pos_cursor"])

        self.screen.blit(self.basketball, basketball_rect)
        
        if not state.state["key_yellow"]:
            self.screen.blit(self.yellow_key, yellow_key_rect)

        pos=pygame.mouse.get_pos()
        arrows.arrows(pos)
        
        if state.state["substage"]=="safe":
            dialogue.msgbox(state.state["language"]["safe"],"", True, True)
        if state.state["substage"]=="safe1":
            done=dialogue.msgbox(state.state["language"]["safe1"],"", True, False)
            
            font = pygame.font.SysFont('Arial', self.h // 10)
            render = font.render("_ _ _ _ ", True, (255,255,255))
            x, y = (self.w*(5/100), self.h*(85/100))
            text_rect = render.get_rect(topleft=(x, y)) 
            state.state["screen"].blit(render, text_rect)
            
            
            render_code = font.render(self.code, True, (255,255,255))
            x, y = (self.w*(5/100), self.h*(85/100))
            text_rect_code = render_code.get_rect(topleft=(x, y)) 
            state.state["screen"].blit(render_code, text_rect_code)
            if done:
                state.state["substage"]="waiting"
                
        if state.state["substage"]=="waiting":
            self.code=""
            state.state["substage"]=""
                
        elif state.state["substage"]=="safe2":
            done=dialogue.msgbox(state.state["language"]["safe2"],"", True, False)
            if done:
                state.state["substage"]="waiting"
        elif state.state["substage"]=="safe3":
            done=dialogue.msgbox(state.state["language"]["safe3"],"", True, False)
            if done:
                state.state["substage"]=""
        elif state.state["substage"]=="button1":
            done=dialogue.msgbox(state.state["language"]["button1"],"", True, False)
            if done:
                state.state["carpet_removed"]=True
                state.state["substage"]="waiting"
            
        elif state.state["substage"]=="basketball":
            done=dialogue.msgbox(state.state["language"]["basketball"],"", True, True)
        elif state.state["substage"]=="basketball1":
            done=dialogue.msgbox(state.state["language"]["basketball1"],"", True, False)
            if done:
                state.state["substage"]="waiting"
        elif state.state["substage"]=="pictures1":
            done=dialogue.msgbox(state.state["language"]["pictures1"],"", True, True)
            if done:
                state.state["selec_position"]="left"
        elif state.state["substage"]=="pictures2":
            done=dialogue.msgbox(state.state["language"]["pictures2"],"", True, False)
            if done:
                state.state["substage"]="waiting"



        self.handle_events()
    def handle_events(self):
        pos_cursor=pygame.mouse.get_pos()
        state.state["pos_cursor"]=pos_cursor

        # safe_rect=pygame.Surface((self.w*(20/100), self.h*(20/100)), pygame.SRCALPHA)
        # safe_rect.fill((255,0,0,150))
        # self.screen.blit(safe_rect, (self.w*(30/100), self.h*(36/100)))
        
        safe_rect=pygame.Rect(self.w*(50/100), self.h*(46/100),int(self.w*(16/100)),int(self.h*(12/100)))
        button_rect=self.button.get_rect(topleft=(self.w*(51/100),self.w*(26/100)))
        
        self.mouse_in_safe=safe_rect.collidepoint(state.state["pos_cursor"])
        self.mouse_in_button=button_rect.collidepoint(state.state["pos_cursor"])
        
        if state.state["substage"]=="":
            if self.mouse_in_safe and not state.state["safe_opened"]:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
            elif self.mouse_in_button and state.state["safe_opened"]:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
            elif self.mouse_in_basketball:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
            elif self.mouse_in_yellow_key and not state.state["key_yellow"]:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
            elif self.mouse_in_pictures :
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 

        for event in state.state["events"]:
            keys = pygame.key.get_pressed() # Alternative way to detect keys pressed, it detects key pressed continously
            
            if state.state["game_in"]=="living":
                    
                is_click = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                is_key = event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE) 
                if event.type == pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                    state.var_ini()
                    self.code=""
                    state.state["substage"]=""
                if state.state["substage"]=="":
                    if self.mouse_in_yellow_key and is_click:
                        state.state["key_yellow"]=True
                    if self.mouse_in_safe and is_click and not state.state["safe_opened"]:
                        state.var_ini()
                        state.state["substage"]="safe"
                    if self.mouse_in_button and is_click and state.state["safe_opened"]:
                        state.var_ini()
                        state.state["substage"]="button1"
                    if self.mouse_in_basketball and is_click:
                        state.var_ini()
                        state.state["substage"]="basketball"
                    if self.mouse_in_pictures and is_click:
                        state.var_ini()
                        state.state["substage"]="pictures1"
    
                if state.state["substage"]=="basketball":
                    if ((state.state["selec_position"]=="left" and is_key) or  (self.w*(30/100)<pos_cursor[0]<self.w*(38/100) and self.h*(85/100)<pos_cursor[1]<self.h*(92/100) and is_click) ):
                        state.var_ini()
                        state.state["substage"]="basketball1"
                    elif (state.state["selec_position"]=="right" and is_key) or (self.w*(60/100)<pos_cursor[0]<self.w*(68/100) and self.h*(85/100)<pos_cursor[1]<self.h*(92/100) and is_click):
                        state.var_ini()
                        self.code=""
                        state.state["substage"]=""
                
                if state.state["substage"]=="pictures1":
                    if ((state.state["selec_position"]=="left" and is_key) or  (self.w*(30/100)<pos_cursor[0]<self.w*(38/100) and self.h*(85/100)<pos_cursor[1]<self.h*(92/100) and is_click) ):
                        state.var_ini()
                        state.state["substage"]="pictures2"
                    elif (state.state["selec_position"]=="right" and is_key) or (self.w*(60/100)<pos_cursor[0]<self.w*(68/100) and self.h*(85/100)<pos_cursor[1]<self.h*(92/100) and is_click):
                        state.var_ini()
                        self.code=""
                        state.state["substage"]=""
                        
                if state.state["substage"]=="safe":
                    if ((state.state["selec_position"]=="left" and is_key) or  (self.w*(30/100)<pos_cursor[0]<self.w*(38/100) and self.h*(85/100)<pos_cursor[1]<self.h*(92/100) and is_click) ):
                        state.var_ini()
                        state.state["substage"]="safe1"
                    elif (state.state["selec_position"]=="right" and is_key) or (self.w*(60/100)<pos_cursor[0]<self.w*(68/100) and self.h*(85/100)<pos_cursor[1]<self.h*(92/100) and is_click):
                        state.var_ini()
                        self.code=""
                        state.state["substage"]="waiting"
                if state.state["substage"]=="safe1":
                    if event.type == pygame.KEYDOWN and pygame.K_0 <= event.key <= pygame.K_9 and len(self.code)<8:
                        self.code += chr(event.key)+" "
                    elif event.type == pygame.KEYDOWN and event.key==pygame.K_BACKSPACE:
                        self.code = self.code[:-2]
                        
                    if len(self.code)==8 and self.code=="7 4 6 8 ":
                        state.var_ini()
                        state.state["substage"]="safe3"
                        state.state["safe_opened"]=True
                    elif len(self.code)==8 and self.code!="7 4 6 8 ":
                        state.var_ini()
                        self.code=""
                        state.state["substage"]="safe2"

                if state.state["substage"]=="button":
                    state.var_ini()
                    state.state["substage"]="safe1"
