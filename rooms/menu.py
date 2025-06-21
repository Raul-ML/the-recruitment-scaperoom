import state
import loader
import pygame
import sys
import ui.dialogue as dialogue
import ui.background as background


class Menu:
    def __init__(self):
        self.bckg=loader.bckg_menu
        self.w, self.h=state.state["game_size"]

    def render(self):    
        
        # background dynamic size
        self.w, self.h=state.state["game_size"]
        font = pygame.font.SysFont('Arial', self.h//15, True)
        scaled_image = pygame.transform.scale(self.bckg, (self.w, self.h))
        language=state.state["language"]
        
        state.state["screen"].blit(scaled_image,(0,0))
        
        # message to start               
        text1 = font.render(language["menu"], True, (255,255,255))
        text_rect1 = text1.get_rect(center=(self.w/2, self.h*(4/5)))
        if (state.state["t"]//(state.state["FPS"]//2))%2==0:
            state.state["screen"].blit(text1, text_rect1)
        
        self.handle_events()

    def handle_events(self): 
        
        for event in state.state["events"]:
            keys = pygame.key.get_pressed() # Alternative way to detect keys pressed, it detects key pressed continously
            pos_cursor=pygame.mouse.get_pos()

            if state.state["game_in"]=="menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and keys[pygame.K_z]:
                        state.var_ini()
                        state.state["substage"]="character"
                        state.state["game_in"]="start"
                    if event.key == pygame.K_LEFT and keys[pygame.K_z]:
                        state.state["lang_selected"]=False
                        state.var_ini()
                        state.state["game_in"]="language"
                    elif event.key not in (pygame.K_z, pygame.K_RIGHT, pygame.K_LEFT):
                        background.fade()
                        state.var_ini()
                        state.state["substage"]="character"
                        state.state["game_in"]="start"
                elif event.type ==pygame.MOUSEBUTTONDOWN and event.button == 1:
                    background.fade()
                    state.var_ini()
                    state.state["substage"]="character"
                    state.state["game_in"]="start"
