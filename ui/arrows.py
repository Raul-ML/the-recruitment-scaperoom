import pygame
import state
import loader

def arrows(pos_cursor):
    w,h=state.state["game_size"]
    screen=state.state["screen"]

    arrow_right = pygame.transform.scale(loader.arrow_right, (w*(9/100),h*(9/100)))
    arrow_left = pygame.transform.scale(loader.arrow_left, (w*(9/100),h*(9/100)))
    
    arr_r_rect=arrow_right.get_rect(topleft=(w*(90/100), state.state["arrow_yl"]))
    arr_l_rect=arrow_left.get_rect(topleft=(w*(1/100), state.state["arrow_yr"]))
    
    mouse_in_rightarrow=arr_r_rect.collidepoint(pos_cursor)
    mouse_in_leftarrow=arr_l_rect.collidepoint(pos_cursor)    
    
    if not mouse_in_leftarrow and not mouse_in_rightarrow:
        state.state["sum"]=h*(1/300)
    
    substage=state.state["substage"]
    # Arrows for moving through rooms
    if mouse_in_leftarrow and substage=="":
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) # Change the arrow to a hand to click
        state.state["arrow_yl"] +=state.state["sum"]
        if state.state["arrow_yl"]>=h*(53/100) or state.state["arrow_yl"]<=h*(47/100):
            state.state["sum"]=state.state["sum"]*(-1)        
    elif mouse_in_rightarrow and substage=="":
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) # Change the arrow to a hand to click
        state.state["arrow_yr"] +=state.state["sum"]
        if state.state["arrow_yr"]>=h*(53/100) or state.state["arrow_yr"]<=h*(47/100):
            state.state["sum"]=state.state["sum"]*(-1)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        state.state["arrow_yl"]=h//2
        state.state["arrow_yr"]=h//2
        
    arr_r_rect.y=state.state["arrow_yr"]
    arr_l_rect.y=state.state["arrow_yl"]
    
    screen.blit(arrow_right, arr_r_rect)
    screen.blit(arrow_left, arr_l_rect)
    
    arrow_events(mouse_in_rightarrow, mouse_in_leftarrow)
    
def arrow_events(mouse_in_rightarrow, mouse_in_leftarrow):
    for event in state.state["events"]:
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            is_click = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
            is_right_key = event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT
            is_left_key = event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT
            room=state.state["game_in"]
            substage=state.state["substage"]
            if room=="living" and substage=="":
                if (is_click and mouse_in_rightarrow) or is_right_key:
                    state.state["game_in"]="kitchen"
                elif (is_click and mouse_in_leftarrow) or is_left_key:
                    state.state["game_in"]="bedroom"
            elif room=="kitchen" and substage=="":
                if (is_click and mouse_in_rightarrow) or is_right_key:
                    state.state["game_in"]="gaming"
                elif (is_click and mouse_in_leftarrow) or is_left_key:
                    state.state["game_in"]="living"
            elif room=="gaming" and substage=="":
                if (is_click and mouse_in_rightarrow) or is_right_key:
                    state.state["game_in"]="studio"
                elif (is_click and mouse_in_leftarrow) or is_left_key:
                    state.state["game_in"]="kitchen"
            elif room=="studio" and substage=="":
                if (is_click and mouse_in_rightarrow) or is_right_key:
                    state.state["game_in"]="bedroom"
                elif (is_click and mouse_in_leftarrow) or is_left_key:
                    state.state["game_in"]="gaming"
            elif room=="bedroom" and substage=="":
                if (is_click and mouse_in_rightarrow) or is_right_key:
                    state.state["game_in"]="living"
                elif (is_click and mouse_in_leftarrow) or is_left_key:
                    state.state["game_in"]="studio"
