import string # To access letters easily without having to type them myself in an array
from db_utils import get_last_poke_num, populate_db

# TODO: Have all functions utilize the start and to go after start denoters
# TODO: This could be put in a text file, So I don't even have to write this after each crash. Each new pokemon would rewrite the line of the file where it picked up
# This is so when I get kicked from the server I only have to write once where to pick up
POKE_NUM_START_FROM = 1
POKE_TO_GO_AFTER_START = 10000
LAST_POKE_NUM = -1
try: LAST_POKE_NUM = get_last_poke_num()
except:
    populate_db()
    LAST_POKE_NUM = get_last_poke_num()

if POKE_NUM_START_FROM < 1: POKE_NUM_START_FROM=1
if POKE_NUM_START_FROM > LAST_POKE_NUM: POKE_NUM_START_FROM = LAST_POKE_NUM
if POKE_TO_GO_AFTER_START < 1: POKE_TO_GO_AFTER_START=0
if POKE_NUM_START_FROM + POKE_TO_GO_AFTER_START > LAST_POKE_NUM: POKE_TO_GO_AFTER_START = LAST_POKE_NUM - POKE_NUM_START_FROM
POKE_NUM_END_AT = POKE_NUM_START_FROM + POKE_TO_GO_AFTER_START


save_path_starter = "C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Images\\Pokemon"
game_save_path = save_path_starter + "\\Game Sprites\\"
gen6_menu_sprite_save_path = save_path_starter + "\\Menu Sprites\\Gen6\\"
gen8_menu_sprite_save_path = save_path_starter + "\\Menu Sprites\\Gen8\\"
drawn_save_path = save_path_starter + "\\Drawn\\"