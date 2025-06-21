import state
import loader
import pygame
import sys
import ui.background as background
import ui.dialogue as dialogue
import ui.arrows as arrows



class Basement:
    def __init__(self):
        self.FPS=60
        self.door_visited=False
        self.password=""
        self.pass_completed=False
    def render(self):
        self.screen=state.state["screen"]
        self.w, self.h= state.state["game_size"]
        self.language=state.state["language"]
        
        self.bckg= pygame.transform.scale(loader.bckg_basement, (self.w,self.h))
        self.screen.blit(self.bckg, (0, 0))                

        stairs_rect=pygame.Rect(self.w*(5/100), self.h*(10/100), self.w*(20/100), self.h*(35/100))
        self.mouse_in_stairs=stairs_rect.collidepoint(state.state["pos_cursor"])

        door_rect=pygame.Rect(self.w*(47/100), self.h*(27/100), self.w*(15/100), self.h*(57/100))
        self.mouse_in_door=door_rect.collidepoint(state.state["pos_cursor"])
        
        # safe_rect=pygame.Surface((self.w*(15/100), self.h*(57/100)), pygame.SRCALPHA)
        # safe_rect.fill((255,0,0,150))
        # self.screen.blit(safe_rect, (self.w*(47/100), self.h*(27/100)))


        if state.state["substage"]=="waiting":
            state.var_ini()
            self.password=""
            state.state["substage"]=""

        if not self.door_visited:
            if state.state["substage"]=="door":
                done=dialogue.msgbox(state.state["language"]["basement"],"", True, False)
                if done:
                    state.var_ini()
                    state.state["substage"]="door1"
            elif state.state["substage"]=="door1":
                done=dialogue.msgbox(state.state["language"]["basement1"],"???", True, False)
                if done:
                    state.var_ini()
                    state.state["substage"]="door2"
            elif state.state["substage"]=="door2":
                done=dialogue.msgbox(state.state["language"]["basement2"],"???", True, False)
                if done:
                    state.var_ini()
                    self.door_visited=True
                    state.state["substage"]="door3"
        if self.door_visited and state.state["substage"]=="door3":
            done=dialogue.msgbox(state.state["language"]["basement3"],"???", True, False)
            
            font = pygame.font.SysFont('Arial', self.h // 10)
            render = font.render("> __________________", True, (255,255,255))
            x, y = (self.w*(5/100), self.h*(85/100))
            text_rect = render.get_rect(topleft=(x, y)) 
            state.state["screen"].blit(render, text_rect)
            
            
            render_code = font.render(self.password, True, (255,255,255))
            x, y = (self.w*(10/100), self.h*(85/100))
            text_rect_code = render_code.get_rect(topleft=(x, y)) 
            state.state["screen"].blit(render_code, text_rect_code)
            if done:
                state.var_ini()
                state.state["substage"]="door4"
            
        if state.state["substage"]=="door4":
            done=dialogue.msgbox(state.state["language"]["basement4"],"???", True, False)            
            if done:
                state.state["substage"]="waiting"
                
        if len(self.password)==20 :
            self.pass_completed=True
                
        
        
        
        self.handle_events()
        
    def handle_events(self):
        pos_cursor=pygame.mouse.get_pos()
        state.state["pos_cursor"]=pos_cursor



        if state.state["substage"]=="":
            if self.mouse_in_stairs:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
            if self.mouse_in_door:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) 
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) 
                

            
        if state.state["game_in"]=="basement":
                    
            for event in state.state["events"]:
                keys = pygame.key.get_pressed() # Alternative way to detect keys pressed, it detects key pressed continously
                is_click = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                is_key = event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE) 
                if event.type == pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                    state.state["substage"]="waiting"
                if state.state["substage"]=="":
                    if self.mouse_in_stairs and is_click:
                        state.state["game_in"]="studio"
                    if self.mouse_in_door and is_click:
                        if self.door_visited:
                            state.state["substage"]="door3"
                        else:
                            state.state["substage"]="door"
                
                
                if state.state["substage"]=="door3":
                    if event.type == pygame.KEYDOWN and pygame.K_a <= event.key <= pygame.K_z and len(self.password)<20:
                        self.password += chr(event.key)+" "
                        self.password=self.password.upper()
                    elif event.type == pygame.KEYDOWN and event.key==pygame.K_BACKSPACE:
                        self.password = self.password[:-2]
                    
                    if self.pass_completed:
                        if self.password=="R A U L M E N D E Z ":
                            state.var_ini()
                            background.fade()
                            state.state["game_in"]="end"
                        elif self.password!="R A U L M E N D E Z ":
                            state.var_ini()
                            self.password=""
                            state.state["substage"]="door4"


                        