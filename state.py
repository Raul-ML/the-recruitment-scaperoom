state={
    "game_in": "basement" ,
    "substage": "",
    "pos_cursor":"",
    "mouse_in":"",
    "selection":"",
    "name":"",
    
    "is_fullscreen":False,
    
    # Language selection
    "language_selection": "en",
    "lang_selected":True,
    "language":"",
    
    # Character (not used)
    "character":"",
    
    # Events and resolution
    "scenes":[],
    "events": [],
    "screen":[],
    "monitor_size":0,
    "game_size":0,
    
    # Render text
    "counter_to_letter":0,
    "text_speed":1, # The bigger the slower
    "line":0,
    "space_counter":0,
    "text_finished_0":False,
    "text_finished_1":False,
    "text_index_0":0,
    "text_index_1":0,
    "rendered_0":False,
    "rendered_1":False,
    "selec_position":"",
    "dialogue_active":False,
    
    
    # Arrows
    "sum":500,
    "arrow_yr":500,
    "arrow_yl":500,
    
    # Rooms
    "safe_opened":False,
    "play_music":False,
    "safe_opened":False,
    "fridge_status":False,
    "box_status":False,
    "door_status":False,
    "music_box_on": False,
    "carpet_removed":False,
    "tomato":False,
    "record":0,
    
    # General variables
    "t":0,
    "FPS":60,
    "n":0, # Generic counter
    "n_end":9*60, # Instructions time counter

    # Keys collection
    "key_blue":False,
    "key_green":False,
    "key_yellow":False,
    "key_red":False,
    
    
}

# Reset of some variables when room changes
def var_ini():    
    state["pos_cursor"]=''
    state["code_num"]=''
    
    state["counter_to_letter"]=0
    state["text_finished_0"]=False
    state["text_finished_1"]=False
    state["text_index_0"]=0
    state["text_index_1"]=0
    state["rendered_0"]=0
    state["rendered_1"]=0
    state["space_counter"]=0
    state["selec_position"]=""
    
    state["n"]=0


var_ini()