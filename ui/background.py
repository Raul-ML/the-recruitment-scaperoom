import pygame
import loader
import state

def draw_vertical_gradient(surface, color_top, color_bottom):
    height = surface.get_height()
    width = surface.get_width()
    for y in range(height):
        # Interpolación entre color_top y color_bottom
        ratio = y / height
        r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
        g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
        b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))

def draw_outline(surface, image, pos, outline_color=(255, 255, 255)):
    x, y = pos
    mask = pygame.mask.from_surface(image)
    outline = mask.outline()

    for ox, oy in outline:
        surface.set_at((x + ox, y + oy), outline_color)

    surface.blit(image, pos)
def fade():
    black_surface = pygame.Surface((state.state["screen"].get_width(), state.state["screen"].get_height()), flags= pygame.SRCALPHA)
    for alpha in range(0,255,10): # Step to increse speed of fade
        black_surface.fill((0, 0, 0, alpha))
        state.state["screen"].blit(black_surface, (0, 0))            
        pygame.display.update()
        pygame.time.Clock().tick(10) # Stablishes fade speed

def fade_back(bckg):
    screen=state.state["screen"]
    w,h=screen.get_size()
    black_surface = pygame.Surface((w,h), pygame.SRCALPHA)
    for alpha in range(255,-1,-5): # Step to increse speed of fade
        screen.blit(bckg, (0, 0))
        
        black_surface.fill((0, 0, 0, alpha))
        screen.blit(black_surface, (0, 0))            
        pygame.display.update()
        pygame.time.Clock().tick(20) # Stablishes fade speed
    
def transparent(): # Load transparent black background when clicking something and text appears
    alpha_key=150
    black_surface = pygame.Surface((state.state["screen"].get_width(), state.state["screen"].get_height()), pygame.SRCALPHA)
    black = (0, 0, 0, alpha_key)
    black_surface.fill(black)
    state.state["screen"].blit(black_surface, state.state["screen"].get_rect())
