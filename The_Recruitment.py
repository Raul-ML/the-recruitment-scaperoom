
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame 
import sys, random
from pygame.locals import *

import balls_game
import loader
import state
import language
import ui.dialogue as dialogue

from rooms.menu import Menu
from rooms.start import Start
from rooms.scenes import Scenes
from rooms.living import Living
from rooms.gaming import Gaming
from rooms.kitchen import Kitchen
from rooms.studio import Studio
from rooms.bed import Bedroom
from rooms.basement import Basement
from rooms.end import End

pygame.init()
pygame.mixer.init()


# Find path of the program
path=os.path.dirname(os.path.abspath(__file__))

MUSIC_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END)

# Start music randomly
music_files = [f for f in os.listdir(path+"/music") if f.endswith((".mp3"))]
last_song=None

def play_random_music():
        global last_song
        available = [s for s in music_files if s != last_song] or music_files
        song = random.choice(available)
        last_song = song
        music_path = os.path.join(path+"/music", song)
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.15)

# Start basic variables
w=1024
h=720

pygame.display.set_caption("The Recruitment")

white=(255,255,255)
black=(0,0,0)
FPS=60

    
class MainProgram():
    def __init__(self):
        state.state["language"] = language.es  # Initialize dict variable for language phrases
        if state.state["game_in"]=="":
            state.state["game_in"]="language" 
        self.info = pygame.display.Info()
        state.state["monitor_size"] = self.info.current_w,self.info.current_h
        self.monitor=state.state["monitor_size"]
        state.state["game_size"] = int(self.monitor[0] * 0.9),int(self.monitor[1] * 0.9)
        self.w, self.h=state.state["game_size"]
        
        self.font = pygame.font.SysFont('Arial', self.h//12, True)
        self.font2 = pygame.font.SysFont('Arial', self.h//20, True)
        state.state["screen"] = pygame.display.set_mode((self.w, self.h))
        
        state.state["scenes"]=self.roomManager()
        self.Main()
    
    def instructions(self):
        state.state["screen"].fill((0,0,0))
        language=state.state["language"]
        
        dialogue.render_message(language["instructions3"], pygame.font.SysFont('Arial', self.h//10, True) , (self.w/2, self.h*(1/6)), False, True, (255,0,0), False)
        
        dialogue.render_message(language["instructions4"], pygame.font.SysFont('Arial', self.h//20, True) , (self.w/2, self.h*(35/100)), False, True, dialogue=False)
        dialogue.render_message(language["instructions5"], pygame.font.SysFont('Arial', self.h//20, True) , (self.w/2, self.h*(45/100)), False, True, dialogue=False)
        dialogue.render_message(language["instructions6"], pygame.font.SysFont('Arial', self.h//20, True) , (self.w/2, self.h*(55/100)), False, True, dialogue=False)
        dialogue.render_message(language["instructions7"], pygame.font.SysFont('Arial', self.h//20, True) , (self.w/2, self.h*(65/100)), False, True, dialogue=False)
        dialogue.render_message(language["instructions8"], pygame.font.SysFont('Arial', self.h//20, True) , (self.w/2, self.h*(75/100)), False, True, dialogue=False)
        
        dialogue.render_message(str(state.state["n_end"]//60-state.state["n"]//60), pygame.font.SysFont('Arial', self.h//20, True) , (self.w/2, self.h*(85/100)), False, True, dialogue=False)
        
        state.state["n"]+=1
        
    def lang(self,pos):
        state.state["screen"].fill((0,0,0))
        
        text1 = self.font.render(state.state["language"]["lang"], True, (255,255,255))
        text_rect1 = text1.get_rect(center=(self.w/2, self.h*(1/5)))
        state.state["screen"].blit(text1, text_rect1)

        text2 = self.font.render("English", True, (255,255,255))
        text_rect2 = text2.get_rect(center=(self.w/2, self.h*(2/5)))
        mouse_in_english=text_rect2.collidepoint(pos)
        
        text3 = self.font.render("Español", True, (255,255,255))
        text_rect3 = text3.get_rect(center=(self.w/2, self.h*(3/5)))
        mouse_in_spanish=text_rect3.collidepoint(pos)
        
        text4 = self.font2.render(state.state["language"]["instructions"], True, (255,255,255))
        text_rect4 = text4.get_rect(center=(self.w/2, self.h*(4/5)))
        state.state["screen"].blit(text4, text_rect4)

        text5 = self.font2.render(state.state["language"]["instructions2"], True, (255,255,255))
        text_rect5 = text5.get_rect(center=(self.w/2, self.h*(6/7)))
        state.state["screen"].blit(text5, text_rect5)

        if state.state["language_selection"]=="en":
            text_black=self.font.render("English", True, (0,0,0))
            text_white=text2
            text_rect=text_rect2
            
            state.state["screen"].blit(text3, text_rect3)
        elif state.state["language_selection"]=="es":
            text_black=self.font.render("Español", True, (0,0,0))
            text_white=text3
            text_rect=text_rect3
        
            state.state["screen"].blit(text2, text_rect2)
        
        if (state.state["t"]//(FPS//2))%2==0:
            pygame.draw.rect(state.state["screen"], (255, 255, 255), text_rect)
            state.state["screen"].blit(text_black, text_rect)
        else:
            state.state["screen"].blit(text_white, text_rect)
            
        return mouse_in_english,mouse_in_spanish
    
    def toggle_fullscreen(self):
        if not state.state["is_fullscreen"]:
            state.state["screen"] = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            state.state["screen"] = pygame.display.set_mode((self.monitor[0]*0.9, self.monitor[1]*0.9))
        self.w, self.h = state.state["screen"].get_size()
        state.state["game_size"]=self.w, self.h
        state.state["is_fullscreen"] = not state.state["is_fullscreen"]
    
    def handle_language_selection(self, event, mouse_in_english, mouse_in_spanish, click):
        if state.state["language_selection"]=="en":
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    state.state["language_selection"]="es"
                    state.state["language"] = language.es
                elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    state.state["language"] = language.en
                    state.state["lang_selected"]=True
                    state.state["game_in"]="instructions"
            if mouse_in_spanish:
                state.state["language_selection"]="es"
                state.state["language"] = language.es
            if mouse_in_english and (event.type ==pygame.MOUSEBUTTONDOWN and event.button == 1):
                state.state["language"] = language.en
                state.state["lang_selected"]=True
                state.state["game_in"]="instructions"
        if state.state["language_selection"]=="es"    :
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    state.state["language_selection"]="en"
                    state.state["language"] = language.en
                elif event.key  in (pygame.K_SPACE, pygame.K_RETURN):
                    state.state["language"] = language.es
                    state.state["lang_selected"]=True
                    state.state["game_in"]="instructions"
            if mouse_in_english:
                state.state["language_selection"]="en"
                state.state["language"] = language.en
            if mouse_in_spanish and (event.type ==pygame.MOUSEBUTTONDOWN and event.button == 1):
                state.state["language"] = language.es
                state.state["lang_selected"]=True
                state.state["game_in"]="instructions"

    def roomManager(self):
        
        scenes={
            "menu": Menu(),
            "start": Start(),
            "scenes": Scenes(),
            "living": Living(),
            "studio": Studio(),
            "gaming": Gaming(),
            "kitchen": Kitchen(),
            "bedroom": Bedroom(),
            "basement": Basement(),
            "end": End(),
        }
        
        return scenes
            
    def Main(self): # Main loop of the game
        play_random_music()
        
        executing=True
        while executing:
            keys = pygame.key.get_pressed() # Alternative way to detect keys pressed, it detects key pressed continously
            mouse_buttons = pygame.mouse.get_pressed()
            pos_cursor=state.state["pos_cursor"]=pygame.mouse.get_pos()
            state.state["events"]=pygame.event.get()
            
            if state.state["game_in"] not in ("language", "instructions"):
                room=state.state["game_in"]
                if room:
                    scenes=state.state["scenes"]
                    scenes[room].render()
                    if state.state["play_music"]:
                        play_random_music()
                        state.state["play_music"]=False
            else:
                if state.state["game_in"]=="instructions" and state.state["n"]<=state.state["n_end"]:
                    self.instructions()
                elif state.state["game_in"]=="instructions" and state.state["n"]>state.state["n_end"]:
                    state.var_ini()
                    state.state["game_in"]="menu"
                elif state.state["game_in"]=="language":
                    mouse_in_english, mouse_in_spanish=self.lang(pos_cursor)


            # ----- General Events -----
            for event in state.state["events"]:
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()   
                elif state.state["game_in"]=="language":    
                        self.handle_language_selection(event, mouse_in_english, mouse_in_spanish, mouse_buttons[0])
                elif event.type == MUSIC_END:
                    play_random_music()
                
                if keys[pygame.K_r] and keys[pygame.K_a] and keys[pygame.K_u] and keys[pygame.K_l] : # Press RAUL to on/off fullscreen mode
                        self.toggle_fullscreen()
                elif keys[pygame.K_h] and keys[pygame.K_i] and keys[pygame.K_r] and keys[pygame.K_e] and keys[pygame.K_d] :
                    state.state['game_in']="end"                
                
            state.state["t"]+=1 # Increase time count
            pygame.display.update()
            pygame.time.Clock().tick(FPS) # Stablishes FPS

if __name__ == '__main__':
    MainProgram()


