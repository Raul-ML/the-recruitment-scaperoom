import state
import loader
import pygame
import sys
import ui.dialogue as dialogue
import ui.arrows as arrows



class Bedroom:
    def __init__(self):
        self.FPS=60
        self.counter=0


    def render(self):
        self.screen=state.state["screen"]
        self.w, self.h= state.state["game_size"]
        self.language=state.state["language"]

        bckg= pygame.transform.scale(loader.bckg_bed, (self.w,self.h))
        self.screen.blit(bckg, (0, 0))

        self.box=pygame.transform.scale(loader.box, (self.w*(25/100),self.h*(40/100)))
        self.green_key=pygame.transform.scale(loader.key_green, (self.w/30,self.h/25))
        
        box_rect=pygame.Rect(self.w*(77/100), self.h*(73/100), self.w*(20/100),self.h*(25/100))
        box_rect2=self.box.get_rect(topleft=(self.w*(75/100), self.h*(65/100)))

        green_key_rect=self.green_key.get_rect(topleft=(self.w*(47/200), self.h*(26/100)))
        
        self.mouse_in_box=box_rect.collidepoint(state.state["pos_cursor"])
        self.mouse_in_green_key=green_key_rect.collidepoint(state.state["pos_cursor"])
        
        clothes_rect=pygame.Rect(self.w*(4/100), self.h*(13/100), self.w*(10/100), self.h*(30/100))
        self.mouse_in_clothes=clothes_rect.collidepoint(state.state["pos_cursor"])
        
        self.screen.blit(self.box, box_rect2)
        
        pos=pygame.mouse.get_pos()
        arrows.arrows(pos)
        
        if not state.state["key_green"]:
            self.screen.blit(self.green_key, green_key_rect)
        
        if state.state["substage"]=="waiting":
            state.var_ini()
            state.state["substage"]=""
        
        elif state.state["substage"]=="clothes":
            done=dialogue.msgbox(state.state["language"]["clothes"],"", True, False)
            if done:
                state.state["substage"]="waiting"

        elif state.state["substage"]=="box":
            if not state.state["box_status"]:
                done=dialogue.msgbox(state.state["language"]["box_closed"],"",True,True)                        
            else:
                done=dialogue.msgbox(state.state["language"]["box_opened"],"",True, True)                    
        
        elif state.state["substage"] == "box2":
            done=dialogue.msgbox(state.state["language"]["box_clue"],"", True, False)
            if done:
                state.var_ini()
                state.state["substage"] = "box3"
        
        elif state.state["substage"] == "box3":
            done=dialogue.msgbox(state.state["language"]["box_clue1"],"", True, False)
            if done:
                state.state["substage"]="waiting"
        elif state.state["substage"] == "box1":
            if "box1_keys" not in state.state:
                state.state["box1_keys"] = []

                if not state.state["key_blue"]:
                    state.state["box1_keys"].append(self.language["box_blue"])
                if not state.state["key_red"]:
                    state.state["box1_keys"].append(self.language["box_red"])
                if not state.state["key_green"]:
                    state.state["box1_keys"].append(self.language["box_green"])
                if not state.state["key_yellow"]:
                    state.state["box1_keys"].append(self.language["box_yellow"])
                state.state["box1_index"] = 0

                if state.state["box1_keys"]!=[]:
                    dialogue.msgbox(state.state["box1_keys"][0], "",True, False)

            else:  
                if state.state["box1_keys"]==[]:
                    done=dialogue.msgbox(self.language["box_open"], "",True, False)
                    if done:
                        state.state["box_status"] = True
                        state.var_ini()
                        state.state["substage"] = "box2"
                        del state.state["box1_keys"]
                        del state.state["box1_index"]
                        
                else:                    
                    if state.state["box1_index"] < len(state.state["box1_keys"]):
                        done=dialogue.msgbox(state.state["box1_keys"][state.state["box1_index"]], "", True, False)
                        if done:
                            state.var_ini()
                            state.state["box1_index"] += 1
                    else:
                        state.state["substage"] = "waiting"
                        del state.state["box1_keys"]
                        del state.state["box1_index"]
        
        self.handle_events()
    def handle_events(self):
        pos_cursor=pygame.mouse.get_pos()
        state.state["pos_cursor"]=pos_cursor

        # safe_rect=pygame.Surface((self.w*(10/100), self.h*(30/100)), pygame.SRCALPHA)
        # safe_rect.fill((255,0,0,150))
        # self.screen.blit(safe_rect, (self.w*(4/100), self.h*(13/100)))
        
        if state.state["substage"]=="":
            if self.mouse_in_box:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
            elif self.mouse_in_green_key and not state.state["key_green"]:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
            elif self.mouse_in_clothes:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 

            
        if state.state["game_in"]=="bedroom":
                    
            for event in state.state["events"]:
                keys = pygame.key.get_pressed() # Alternative way to detect keys pressed, it detects key pressed continously
                is_click = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                is_key = event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE) 
                if event.type == pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                    state.state["substage"]="waiting"
                if self.mouse_in_green_key and is_click and state.state["substage"]=="":
                    state.state["key_green"]=True
                if self.mouse_in_box and is_click and state.state["substage"]=="":
                    state.var_ini()
                    state.state["substage"]="box"
                if self.mouse_in_clothes and is_click and state.state["substage"]=="":
                    state.var_ini()
                    state.state["substage"]="clothes"
                            
                if state.state["substage"]=="box":
                    if ((state.state["selec_position"]=="left" and is_key) or  (self.w*(30/100)<pos_cursor[0]<self.w*(38/100) and self.h*(85/100)<pos_cursor[1]<self.h*(92/100) and is_click) ):
                        self.counter = 0
                        state.var_ini()
                        if not state.state["box_status"]:
                            state.state["substage"]="box1"
                        elif state.state["box_status"]:
                            state.state["substage"]="box2"
                            
                    elif (state.state["selec_position"]=="right" and is_key) or (self.w*(60/100)<pos_cursor[0]<self.w*(68/100) and self.h*(85/100)<pos_cursor[1]<self.h*(92/100) and is_click):
                        state.var_ini()
                        state.state["substage"]="waiting"
