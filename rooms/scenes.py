import state
import loader
import pygame
import sys
import ui.dialogue as dialogue
import ui.background as background


class Scenes:
    def __init__(self):
        self.bckg_boss=loader.bckg_boss  
        self.bckg_house=loader.bckg_house
        
        self.counter=0
        self.n=0
        self.text=0
        self.text_done=False

    def render(self):    
        self.w, self.h=state.state["game_size"]
        font = pygame.font.SysFont('Arial', self.h//15, True)
        if state.state["substage"]=="boss" :
            self.boss()
        elif state.state["substage"]=="house" :
            self.house()
        
        self.handle_events()

    def handle_events(self): 
        
        for event in state.state["events"]:
            keys = pygame.key.get_pressed() # Alternative way to detect keys pressed, it detects key pressed continously
            pos_cursor=pygame.mouse.get_pos()

            if state.state["game_in"]=="scenes" and self.counter>=30:
                
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                        is_click = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                        is_key = event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE)                    # if event.key == pygame.K_RIGHT and keys[pygame.K_z]:
                        if keys[pygame.K_LEFT] and keys[pygame.K_z]:
                            state.var_ini()
                            self.counter=0
                            self.n=0
                            self.text=0
                            self.text_done=False
                            state.state["game_in"]="start"
                            state.state["substage"]="name"
    
    def boss(self):
        bckg = pygame.transform.scale(self.bckg_boss, (self.w, self.h))
        state.state["screen"].blit(bckg,(0,0))
        language=state.state["language"]
        lines = [
            language["boss1"],
            language["boss2"],
            language["boss3"],
            language["boss4"],
            language["boss5"],
            language["boss6"],
            language["boss7"]
        ]
        if self.counter<=30 : # Delay 1s = 60fps
            self.counter+=1 
        else:
            if self.text < len(lines):
                if dialogue.msgbox(lines[self.text].format(player=state.state["name"]), language["boss"]):
                    self.text += 1
                    state.var_ini()
            else:
                background.fade()
                state.state["substage"] = "house"  
                self.text=0
                state.var_ini()
                self.house()      
        
    def house(self):
        state.state["screen"].fill((0,0,0))
        language=state.state["language"]
        bckg = pygame.transform.scale(self.bckg_house, (self.w, self.h))
        if self.text==0:
            done, all_finished=dialogue.render_message(language["house1"], pygame.font.SysFont('Arial', self.h//20, True) , (self.w/2, self.h*(2/6)), True, True, (255,255,255), False)
            if done:                
                self.text+=1
                state.var_ini()
        elif self.text==1:
            done, all_finished=dialogue.render_message(language["house2"], pygame.font.SysFont('Arial', self.h//20, True) , (self.w/2, self.h*(2/6)), True, True, (255,255,255), False)
            if done:                
                self.text+=1
                self.n=0
                state.var_ini()
        else:
            if self.n==0:
                background.fade_back(bckg)
                self.n=1
            elif self.n==1:
                state.state["screen"].blit(bckg,(0,0))
                if dialogue.msgbox(language["house3"], state.state["name"]):
                    background.fade()
                    state.state["substage"]=""
                    state.state["game_in"]="living"