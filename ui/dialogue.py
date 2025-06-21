import pygame
import loader
import state

def msgbox(text1, person="", transparent=False, selection=False):
    w, h = state.state["game_size"]
    dialogue_box = pygame.transform.scale(loader.dialogue_box1, (w, h * (5 / 16)))

    if transparent:
        alpha_key = 150
        black_surface = pygame.Surface((state.state["screen"].get_width(), state.state["screen"].get_height()), pygame.SRCALPHA)
        black_surface.fill((0, 0, 0, alpha_key))
        state.state["screen"].blit(black_surface, (0, 0))

    state.state["screen"].blit(dialogue_box, (0, h * (90 / 130)))
    font = pygame.font.SysFont('Arial', h // 15)

    if person != "":
        person_name(person, w, h)
    
    if "RED" in text1 or "ROJA" in text1:
        color=(255,0,0)
    elif "BLUE" in text1 or "AZUL" in text1:
        color=(0,80,255)
    elif "GREEN" in text1 or "VERDE" in text1:
        color=(0,255,0)
    elif "YELLOW" in text1 or "AMARILLA" in text1:
        color=(255,255,0)
    else:
        color=(255,255,255)
    done, all_finished = render_message(text1, font, (w * (5 / 100), h * (96 / 130)), generative=True, center=False, dialogue=True, color=color)

    if selection and all_finished:
        selec_option(w, h, all_finished)
    return done

def selec_option(w, h, all_finished):
    grey = (30, 30, 30)
    white = (255, 255, 255)
    font1 = pygame.font.SysFont('Arial', h // 15)
    pos = state.state["selec_position"]
    blink = (state.state["t"] *2// state.state["FPS"]) % 2 == 0

    if state.state["substage"]=="box":
        img1 = font1.render(state.state["language"]["selec2"], True, (0, 0, 0) if blink and pos == 'left' else white)
    elif state.state["substage"]=="ballsgame1":
        img1 = font1.render(state.state["language"]["selec3"], True, (0, 0, 0) if blink and pos == 'left' else white)
    elif state.state["substage"]=="music":
        img1 = font1.render(state.state["language"]["selec4"], True, (0, 0, 0) if blink and pos == 'left' else white)
    else:
        img1 = font1.render(state.state["language"]["selec1"], True, (0, 0, 0) if blink and pos == 'left' else white)
    img2 = font1.render(state.state["language"]["selec"], True, (0, 0, 0) if blink and pos == 'right' else white)

    rect1=img1.get_rect(topleft=(w*(30/100), h*(85/100)))
    rect2=img2.get_rect(topleft=(w*(60/100), h*(85/100)))
    
    for event in state.state["events"]:
        pos_cursor=pygame.mouse.get_pos()
        if (event.type == pygame.KEYDOWN and event.key ==pygame.K_RIGHT) or rect2.collidepoint(pos_cursor):
            pos="right"
            state.state["selec_position"]=pos
        elif (event.type == pygame.KEYDOWN and event.key ==pygame.K_LEFT) or rect1.collidepoint(pos_cursor):    
            pos="left"
            state.state["selec_position"]=pos

    if pos=="left":
        pygame.draw.rect(state.state["screen"],(255,255,255)if blink else grey, rect1)
    elif pos=="right":
        pygame.draw.rect(state.state["screen"],(255,255,255)if blink else grey, rect2)
    if all_finished:
        if state.state["selec_position"]=="":
            state.state["selec_position"]="left"
        state.state["screen"].blit(img1, rect1)
        state.state["screen"].blit(img2, rect2)
# (self.w*(30/100)<pos_cursor[0]<self.w*(38/100) and self.h*(85/100)<pos_cursor[1]<self.h*(92/100) and is_click) 
# (self.w*(60/100)<pos_cursor[0]<self.w*(68/100) and self.h*(85/100)<pos_cursor[1]<self.h*(92/100) and is_click) 

def person_name(person, w, h):
    name_length=len(person)
    if name_length==0:
        name_length=8
    box_w=w*(name_length/42)
    box_x=w * (4 / 100)
    box_h= h / 13
    box_y= h * (85 / 130)
    name_box = pygame.transform.scale(loader.dialogue_box1, (box_w, box_h))
    state.state["screen"].blit(name_box, (box_x, box_y))
   
    font = pygame.font.SysFont('Arial', h // 18)
    text = font.render(person, True, (255, 255, 255))
    text_rect = text.get_rect(center=(box_x + box_w/2, box_y + box_h/2))
    state.state["screen"].blit(text, text_rect)

def render_message(text, font, pos, generative=False, center=True, color=(255, 255, 255), dialogue=False):
    w, h = state.state["game_size"]

    if dialogue:
        n = 9
        words_list = text.split("/n")
        lines = [e.split() for e in words_list] if len(words_list) == 2 else [text.split()[:n], text.split()[n:]]
        joined_lines = [" ".join(line) for line in lines]
        line_space = h * (5 / 48)
    else:
        joined_lines = [text]
        line_space = 0

    all_finished = all(state.state.get(f"text_finished_{i}", False) for i in range(len(joined_lines)))
    
    for event in state.state["events"]:
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            is_key = event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE)
            is_click = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
            if is_key or is_click:
                if not all_finished:
                    for i in range(len(joined_lines)):
                        state.state[f"text_index_{i}"] = len(joined_lines[i])
                        state.state[f"text_finished_{i}"] = True
                else:
                    if state.state["substage"]=="fridge1" and is_click:
                        pass
                    else:
                        return True, all_finished
                        
                
    for i, line in enumerate(joined_lines):
        index_key = f"text_index_{i}"
        finished_key = f"text_finished_{i}"

        if generative and not state.state[finished_key]:
            if i == 0 or state.state.get(f"text_finished_{i - 1}", False):
                state.state["counter_to_letter"] += 1
                if state.state["counter_to_letter"] >= state.state["text_speed"]:
                    state.state["counter_to_letter"] = 0
                    state.state[index_key] += 1
                    if state.state[index_key] >= len(line):
                        state.state[finished_key] = True
        else:
            state.state[finished_key] = True
            state.state[index_key] = len(line)

        to_draw = line[:state.state[index_key]]
        render = font.render(to_draw, True, color)
        x, y = pos[0], pos[1] + i * line_space
        text_rect = render.get_rect(center=(x, y)) if center else render.get_rect(topleft=(x, y))
        state.state["screen"].blit(render, text_rect)

    return False, all_finished
