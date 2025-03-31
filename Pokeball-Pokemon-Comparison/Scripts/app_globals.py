import string # To access letters easily without having to type them myself in an array
from json_utils import save_json, load_json

pokedex = []

# Pokemon object
class Pokemon:
    def __init__(self, number, name, gen, has_f_var, has_mega, has_giganta, reg_forms, misc_forms, is_in_game):
        self.number = number
        self.name = name
        self.gen = gen
        self.has_f_var = has_f_var
        self.has_mega = has_mega
        self.has_giganta = has_giganta
        self.reg_forms = reg_forms
        self.misc_forms = misc_forms
        self.is_in_game = is_in_game
        self.form_availability = []
        # dict
        # "form-name": 
        # "gen 1 avail": True
        # etc...
        self.missing_imgs = []
        self.missing_gen1_thru_gen4_back_imgs = []

def retrieve_json_pokedex():
    print("Importing pokedex from JSON...")
    try:
        pokedex = load_json('pokedex.json')
    except ValueError as e:
        # If JSON is empty it will throw error trying to load
        pokedex = []

def save_pokedex():
    print("Saving pokedex to JSON...")
    save_json(pokedex, 'pokedex.json')

def get_pokedex_info(num, info):
    # -1 to account for array starting from zero
    return pokedex[num-1][info]

# TODO: Have all functions utilize the start and to go after start denoters
# TODO: Need to test what happens when go_to_after_start=0, =1, and when start_from=898, after_start=0
# This is so when I get kicked from the server I only have to write once where to pick up
poke_num_start_from = 898
# If pokedex is empty, don't throw error so pokedex can populate
if poke_num_start_from > len(pokedex) and len(pokedex) != 0:
    raise ValueError("Pokemon to start from must be within the pokedex")
# TODO: Generating pokedex should only go to here too
# TODO: This could be put in a text file, with all missing images too
    # So I don't even have to write this after each crash
        # Each new pokemon would rewrite the line of the file where it picked up
        # And delete missing images that the script downloaded
# TODO: Write function to check this does not exceed last pokemon, if so set to last pokemon
# This is amount of pokemon to get info from after the starter pokemon
poke_to_go_after_start = 10
# Adjusts poke to go after start if it exceeds amount of pokemon in the pokedex, to the amount to the last pokemon
if poke_num_start_from + poke_to_go_after_start > len(pokedex):
    poke_to_go_after_start = len(pokedex) - poke_num_start_from

# TODO: Make this a JSON
pokemon_img_urls = []

# These are for back generation differences to be able to loop through and concatonate game name to filename
# TODO: Make this a dict?
# TODO: Where is this used?
# gen1_games = ["Yellow", "Red-Green", "Red-Blue"]
# gen2_games = ["Silver", "Gold", "Crystal"]
# gen3_games = ["Ruby-Sapphire", "FireRed-LeafGreen", "Emerald"]
# gen4_games = ["Platinum", "HGSS", "Diamond-Pearl"]
# gen_1_thru_4_games = [gen1_games, gen2_games, gen3_games, gen4_games]

# TODO: Put into JSON and adjust scrape_bulba_translators.bulba_doesn't_have_this_form() if needed
# NOTE: Double check occasionally
no_bulba_forms = []
# Pikachu World Cap
no_bulba_forms.append("-Form-Cap-World")
# Cosplay Pikachu
no_bulba_forms.append("-Form-Cosplay")
# Overdrive Reshiram, Zekrom, and Kyurem
no_bulba_forms.append("Overdrive")
# Marshadow Zenith
no_bulba_forms.append("-Form-Zenith")
# Urshifu Forms
no_bulba_forms.extend(["-Form-Rapid_Strike", "-Form-Single_Strike"])
# Dada Zarude
no_bulba_forms.append("-Form-Dada")
# Calyrex Riders
no_bulba_forms.extend(["-Form-Shadow_Rider", "-Form-Ice_Rider"])

uppers = list(string.ascii_uppercase)
poke_types = ["Normal", "Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost", "Steel", "Fire", "Water", "Grass", "Electric", "Psychic", "Ice", "Dragon", "Dark", "Fairy", "Qmark"]
# Vanilla Cream is default, so no letter denoter
creams = [("Caramel_Swirl", "CaS"), ("Lemon_Cream", "LeC"), ("Matcha_Cream", "MaC"), ("Mint_Cream", "MiC"), ("Rainbow_Swirl", "RaS"), ("Ruby_Cream", "RaC"), ("Ruby_Swirl", "RuS"), ("Salted_Cream", "SaC"), ("Vanilla_Cream", "")]
# Strawberry Sweet is default, so no letter denoter
sweets = [("Berry_Sweet", "B"), ("Clover_Sweet", "C"), ("Flower_Sweet", "F"), ("Love_Sweet", "L"), ("Ribbon_Sweet", "R"), ("Star_Sweet", "S"), ("Strawberry_Sweet", "")]


save_path_starter = "C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Images\\Pokemon"
game_save_path = save_path_starter + "\\Game Sprites\\"
gen6_menu_sprite_save_path = save_path_starter + "\\Menu Sprites\\Gen6\\"
gen8_menu_sprite_save_path = save_path_starter + "\\Menu Sprites\\Gen8\\"
drawn_save_path = save_path_starter + "\\Drawn\\"
# TODO: This didn't download gen1-3 female back sprites (Are they different?)
gen1_thru_4_backs_save_path = game_save_path + "\\back_imgs_to_be_filtered\\"
