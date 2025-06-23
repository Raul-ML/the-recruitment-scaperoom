import state
import loader
import pygame
import sys
import balls_game
import ui.dialogue as dialogue
import ui.arrows as arrows



class Gaming:
    def __init__(self):
        self.FPS=60
        self.record=0

    def render(self):
        self.screen=state.state["screen"]
        self.w, self.h= state.state["game_size"]

        pos=pygame.mouse.get_pos()
        state.state["pos_cursor"]=pos
        
        bckg= pygame.transform.scale(loader.bckg_gaming, (self.w,self.h))
        self.screen.blit(bckg, (0, 0))

        self.blue_key=pygame.transform.scale(loader.key_blue, (self.w/22,self.h/15))
        if not state.state["key_blue"]:
            self.screen.blit(self.blue_key, (self.w*(30/100), self.h*(32/100)))
        
        # safe_rect=pygame.Surface((self.w*(16/100), self.h*(20/100)), pygame.SRCALPHA)
        # safe_rect.fill((255,0,0,150))
        # self.screen.blit(safe_rect, (self.w*(23/100), self.h*(46/100)))

        game_rect=pygame.Rect(self.w*(57/100), self.h*(46/100), int(self.w*(20/100)), int(self.h*(17/100)))
        self.mouse_in_game=game_rect.collidepoint(state.state["pos_cursor"])
        
        blue_key_rect=self.blue_key.get_rect(topleft=(self.w*(30/100), self.h*(32/100)))
        self.mouse_in_blue_key=blue_key_rect.collidepoint(state.state["pos_cursor"])
        
        code_rect=pygame.Rect(self.w*(23/100), self.h*(46/100), self.w*(16/100), self.h*(20/100))
        self.mouse_in_code=code_rect.collidepoint(state.state["pos_cursor"])
        
        arrows.arrows(pos)
        
        if state.state["substage"]=="waiting":
            state.state["substage"]=""

        elif state.state["substage"]=="code":
            done=dialogue.msgbox(state.state["language"]["code"], "", True, False)
            if done:
                state.state["substage"] = "waiting"

        elif state.state["substage"]=="ballsgame":
            done=dialogue.msgbox(state.state["language"]["gameballs1"], "", True, False)
            if done:
                state.state["substage"] = "ballsgame_wait"
        elif state.state["substage"] == "ballsgame_wait":
            if not any(pygame.key.get_pressed()):
                state.state["substage"] = "ballsgame1"
        elif state.state["substage"]=="ballsgame1":
            if self.record<6:
                dialogue.msgbox(state.state["language"]["gameballs2"]+"RECORD: "+str(self.record), "", True, True)
            else:    
                if dialogue.msgbox(state.state["language"]["gameballs3"], "", True, False):
                    state.state["substage"] = "waiting"
                
        elif state.state["substage"]=="game":
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            game=balls_game.BallGame()
            self.record=game.Main()
            pygame.mouse.set_visible(True)
            state.state["start_game"] = False   
            state.state["substage"] = "waiting"
            
        self.handle_events()
        
    def handle_events(self):
        if self.mouse_in_game and state.state["substage"]=="":
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
        elif self.mouse_in_blue_key and not state.state["key_blue"] and state.state["substage"]=="":
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
        elif self.mouse_in_code and state.state["substage"]=="":
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 

        for event in state.state["events"]:
            keys = pygame.key.get_pressed() # Alternative way to detect keys pressed, it detects key pressed continously
            pos_cursor=pygame.mouse.get_pos()
            if state.state["game_in"]=="gaming":
                    
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    is_click = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                    is_key = event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE)                    # if event.key == pygame.K_RIGHT and keys[pygame.K_z]:
                    if event.type == pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                        state.state["substage"]="waiting"
                    if state.state["substage"]=="":
                        if self.mouse_in_blue_key and is_click:
                            state.state["key_blue"]=True
                        elif self.mouse_in_game and is_click:
                            state.var_ini()
                            state.state["substage"]="ballsgame"
                        elif self.mouse_in_code and is_click:
                            state.var_ini()
                            state.state["substage"]="code"
                        
                        
                    if state.state["substage"]=="ballsgame1":
                        if ((state.state["selec_position"]=="left" and is_key) or  (self.w*(30/100)<pos_cursor[0]<self.w*(38/100) and self.h*(85/100)<pos_cursor[1]<self.h*(92/100) and is_click) ):
                            state.var_ini()
                            state.state["start_game"] = True
                            state.state["substage"]="game"
                        elif (state.state["selec_position"]=="right" and is_key) or (self.w*(60/100)<pos_cursor[0]<self.w*(68/100) and self.h*(85/100)<pos_cursor[1]<self.h*(92/100) and is_click):
                            state.var_ini()
                            state.state["substage"]=""
                        
        
                
                
