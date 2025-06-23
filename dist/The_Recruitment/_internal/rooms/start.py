import state
import loader
import pygame
import sys
import ui.dialogue as dialogue
import ui.background as background

class Start:
    def __init__(self):
        self.w, self.h=state.state["game_size"]
        
        self.boyimg=loader.boyimg
        self.boyimg_grey=loader.boyimg_grey
        self.girlimg=loader.girlimg
        self.girlimg_grey=loader.girlimg_grey
                
        self.input_rect = pygame.Rect(self.w/4, self.h*(1/3), self.w/2, self.h/10)
        self.input_color_active = pygame.Color('lightskyblue3')
        self.input_color_inactive = pygame.Color('gray15')
        self.font = pygame.font.SysFont('Arial', self.h//10)

        self.active = False
        self.user_text = ""
        self.input_color = self.input_color_inactive

        
    def render(self):    
        self.w, self.h=state.state["game_size"]
        font = pygame.font.SysFont('Arial', self.h//15, True)
        language=state.state["language"]
        
        background.draw_vertical_gradient(state.state["screen"], (185,130,70), (245,205,140))
        if state.state["substage"]=="character":
            dialogue.render_message(language["char"], font, (self.w//2,self.h*(1/6)))
            self.selec_char()
        elif state.state["substage"]=="name":
            dialogue.render_message(language["name"], font, (self.w//2,self.h*(1/6)))
            dialogue.render_message(language["max"], font, (self.w//2,self.h*(1/4)))
            self.input_name()
        

        
        # dialogue.msgcenter(language["name"],self.w//2,self.h*(1/5))
        
        self.handle_events()
                
    def selec_char(self):

        boy_scaled = pygame.transform.scale(self.boyimg, (self.w/3, self.h*(4.5/6)))
        boy_scaled_rect= boy_scaled.get_rect(centerx=int(self.w*(2/3)),bottom=state.state["game_size"][1])

        girl_scaled = pygame.transform.scale(self.girlimg, (self.w/3, self.h*(4.5/6)))
        girl_scaled_rect= girl_scaled.get_rect(centerx=int(self.w*(1/3)),bottom=state.state["game_size"][1])
        
        mouse_in_boy=boy_scaled_rect.collidepoint(state.state["pos_cursor"])
        mouse_in_girl=girl_scaled_rect.collidepoint(state.state["pos_cursor"])
        selection=state.state["selection"]
        
        if mouse_in_boy:
            state.state["mouse_in"]="boy"
            state.state["selection"]=""
            boy_scaled = pygame.transform.scale(self.boyimg, (self.w/2.9, self.h*(4.8/6)))
            girl_scaled = pygame.transform.scale(self.girlimg_grey, (self.w/3, self.h*(4.5/6)))
        elif mouse_in_girl:
            state.state["mouse_in"]="girl"
            state.state["selection"]=""
            boy_scaled = pygame.transform.scale(self.boyimg_grey, (self.w/3, self.h*(4.5/6)))
            girl_scaled = pygame.transform.scale(self.girlimg, (self.w/2.9, self.h*(4.8/6)))
        elif selection=="boy":
            boy_scaled = pygame.transform.scale(self.boyimg, (self.w/2.9, self.h*(4.8/6)))
            girl_scaled = pygame.transform.scale(self.girlimg_grey, (self.w/3, self.h*(4.5/6)))
        elif selection=="girl":
            boy_scaled = pygame.transform.scale(self.boyimg_grey, (self.w/3, self.h*(4.5/6)))
            girl_scaled = pygame.transform.scale(self.girlimg, (self.w/2.9, self.h*(4.8/6)))
        else:
            boy_scaled = pygame.transform.scale(self.boyimg, (self.w/2.9, self.h*(4.8/6)))
            girl_scaled = pygame.transform.scale(self.girlimg, (self.w/2.9, self.h*(4.8/6)))
            
        
        boy_scaled_rect= boy_scaled.get_rect(centerx=int(self.w*(2/3)),bottom=state.state["game_size"][1])
        girl_scaled_rect= girl_scaled.get_rect(centerx=int(self.w*(1/3)),bottom=state.state["game_size"][1])
        state.state["screen"].blit(boy_scaled,boy_scaled_rect)
        state.state["screen"].blit(girl_scaled,girl_scaled_rect)

    def input_name(self):
        pygame.draw.rect(state.state["screen"], self.input_color, self.input_rect, width=3, border_radius=10)
        self.input_rect = pygame.Rect(self.w/4, self.h*(1/3), self.w/2, self.h/10)

        text_surface = self.font.render(self.user_text, True, pygame.Color('white'))
        text_rect=text_surface.get_rect(center=(self.w/2,self.h*(23/60)))
        
        state.state["screen"].blit(text_surface, text_rect)
    
    def handle_events(self):

        keys = pygame.key.get_pressed() # Alternative way to detect keys pressed, it detects key pressed continously
        pos_cursor=pygame.mouse.get_pos()
        for event in state.state["events"]:
            
            if state.state["game_in"]=='start':
                if state.state["substage"]=='character':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT and keys[pygame.K_z]:
                            state.var_ini()                      
                            state.state["game_in"]='menu'      
                        elif event.key == pygame.K_RIGHT :
                            state.state["selection"]='boy'      
                        elif event.key == pygame.K_LEFT :
                            state.state["selection"]='girl'      
                        if (event.key ==pygame.K_RETURN or event.key ==pygame.K_SPACE) and (state.state["selection"]=='girl' or state.state["selection"]=='boy'):
                            state.state["substage"]='name'      
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and (state.state["mouse_in"]=="girl" or state.state["mouse_in"]=="boy"):
                        state.state["substage"]='name'      
                
                if state.state["substage"]=='name':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.input_rect.collidepoint(pos_cursor):
                            self.active = True
                            self.input_color = self.input_color_active
                        else:
                            self.active = False
                            self.input_color = self.input_color_inactive
                    elif event.type == pygame.KEYDOWN:
                        self.active=True    
                        self.input_color = self.input_color_active                    
                        if event.key == pygame.K_RETURN:
                            state.state["name"]=self.user_text
                            self.user_text = ""
                            state.var_ini()  
                            state.state["substage"]="boss" 
                            state.state["game_in"]="scenes"
                        elif  event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        elif len(self.user_text)<=8:
                            self.user_text += event.unicode