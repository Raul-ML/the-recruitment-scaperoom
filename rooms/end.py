import state
import loader
import pygame
import sys
import ui.background as background
import ui.dialogue as dialogue
import ui.arrows as arrows



class End:
    def __init__(self):
        self.FPS=60
        self.counter=0
        self.timer=True
    def render(self):
        self.screen=state.state["screen"]
        self.w, self.h= state.state["game_size"]
        self.language=state.state["language"]
        
        self.bckg= pygame.transform.scale(loader.bckg_end, (self.w,self.h))
        self.screen.blit(self.bckg, (0, 0))                



        if state.state["substage"]=="waiting":
            state.var_ini()
            state.state["substage"]=""

        if state.state["substage"]=="end1":
            done=dialogue.msgbox(state.state["language"]["end1"],"Raul", False, False)
            if done:
                state.var_ini()
                state.state["substage"]="end2"
        elif state.state["substage"]=="end2":
            done=dialogue.msgbox(state.state["language"]["end2"],"Raul", False, False)            
            if done:
                state.var_ini()
                state.state["substage"]="end3"
        elif state.state["substage"]=="end3":
            done=dialogue.msgbox(state.state["language"]["end3"],"Raul", False, False)            
            if done:
                state.var_ini()
                state.state["substage"]="end4"
        elif state.state["substage"]=="end4":
            done=dialogue.msgbox(state.state["language"]["end4"],"Raul", False, False)            
            if done:
                state.var_ini()
                state.state["substage"]="end5"
        elif state.state["substage"]=="end5":
            done=dialogue.msgbox(state.state["language"]["end5"],"Raul", False, False)            
            if done:
                state.var_ini()
                state.state["substage"]="end6"
        elif state.state["substage"]=="end6":
            done=dialogue.msgbox(state.state["language"]["end6"],"Raul", False, False)            
            if done:
                state.var_ini()
                background.fade()
                state.state["game_in"]="menu"
                
        if self.counter<60*2:
            self.counter+=1
        elif self.counter>=60*2 and self.timer:
            self.timer=False
            state.var_ini()
            state.state["substage"]="end1"
        self.handle_events()
        
    def handle_events(self):
        pos_cursor=pygame.mouse.get_pos()
        state.state["pos_cursor"]=pos_cursor                

            
        if state.state["game_in"]=="end":
                    
            for event in state.state["events"]:
                keys = pygame.key.get_pressed() # Alternative way to detect keys pressed, it detects key pressed continously
                is_click = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                is_key = event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE) 
                # if event.type == pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                #     state.state["substage"]="waiting"
                

                        