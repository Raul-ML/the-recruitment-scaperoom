import pygame
import os
import state 

# Path to the directory where it is
path=os.path.dirname(os.path.abspath(__file__))

# MENU
bckg_menu = pygame.image.load(path+"/bckg/menu2.png")

# START
boyimg = pygame.image.load(path+"/bckg/onlyboy.png")
boyimg_grey = pygame.image.load(path+"/bckg/onlyboy_grey.png")
girlimg = pygame.image.load(path+"/bckg/onlygirl.png")
girlimg_grey = pygame.image.load(path+"/bckg/onlygirl_grey.png")

# SCENES
bckg_boss = pygame.image.load(path+"/bckg/boss1.png")
bckg_house = pygame.image.load(path+"/bckg/house.png")

# ROOMS
bckg_living_room = pygame.image.load(path+"/bckg/living_safe.png")
bckg_gaming = pygame.image.load(path+"/bckg/gaming1.png")
bckg_bed = pygame.image.load(path+"/bckg/bedroom1.png")
bckg_studio_carpet = pygame.image.load(path+"/bckg/estudio.png")
bckg_studio_no_carpet = pygame.image.load(path+"/bckg/estudio1.png")
bckg_basement = pygame.image.load(path+"/bckg/basement_letters.png")
bckg_end = pygame.image.load(path+"/bckg/end.png")
bckg_kitchen = pygame.image.load(path+"/bckg/kitchen.png")

bckg_drawer=pygame.image.load(path+"/bckg/drawer.png")
bckg_fridge = pygame.image.load(path+"/bckg/fridge.png")

button=pygame.image.load(path+"/img/button_2.png")
key_yellow=pygame.image.load(path+"/img/key_yellow.png")
key_blue=pygame.image.load(path+"/img/key_blue2.png")
key_green=pygame.image.load(path+"/img/key_green.png")
key_red=pygame.image.load(path+"/img/key_red.png")

tomato = pygame.image.load(path+"/img/tomato1.png")
box = pygame.image.load(path+"/img/box2_no_bckg.png")
basketball = pygame.image.load(path+"/img/basketball_no_bckg2.png")
rollers = pygame.image.load(path+"/img/rollers_no_bckg.png")

# UI
arrow_right=pygame.image.load(path+"/icon/arrow_right.png")
arrow_left=pygame.image.load(path+"/icon/arrow_left.png")

dialogue_box1=pygame.image.load(path+"/icon/dialoguebox1.png")

