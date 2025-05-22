import re

#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def get_translated_game(my_filename, game_map_dict, mid_gen_poke_intro_game_map_dict):
    # Check if its a pokemon introduced mid-gen, if so adjust game name appropriately
    mid_gen_poke_intro_game = get_game_needing_special_translation_for_mid_gen_pokes(my_filename)
    if mid_gen_poke_intro_game: return f" {mid_gen_poke_intro_game_map_dict[mid_gen_poke_intro_game]}"

    for game, translation in game_map_dict.items():
        if "-Back" in my_filename:
            game = game.replace(" ", "_")
        if game in my_filename:
            return(f" {translation}")
        

def get_translated_universal_form(my_filename, mapping):
    for u_form, translation in mapping.items():
        if u_form in my_filename: return(translation)
    return ("")


def extract_gen_num_from_my_filename(my_filename):
    gen_str = re.search(r' Gen(\d+)', my_filename) # Extracting gen from my filename
    gen_int = int(gen_str.group(1))  # Getting just the gen number
    return gen_int


def get_game_needing_special_translation_for_mid_gen_pokes(my_filename):
    for game, pokes in ALT_GAME_MAP.items():
        for poke in pokes:
            if game in my_filename and poke[0] in my_filename and poke[1] in my_filename:
                return game
            
    return None




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     DEFINITIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

# This is to filter out these forms when translating species forms
# The exceptions that have a universal AND species form (See 555 Galarian Darmanitan Zen form) have their own unique form id generated in db_utils > FORM_EXCEPTION_POKEMON
UNIVERSAL_FORMS = {
    "Default", 
    "-f", 
    "-Mega", 
    "-Mega_X", 
    "-Mega_Y", 
    "-Gigantamax", 
    "-Region_Alola", 
    "-Region_Galar", 
    "-Region_Hisui", 
    "-Region_Paldea"
}


EXCLUDE_TRANSLATIONS_MAP = {
    "DBH": "-DO_BY_HAND",
    "DNE": "-DOES_NOT_EXIST_ON_PLATFORM"
}



# This dict maps the few pokemon introduced later in the same gen for games that share sprites, so they are potentially denoted differently on websites
# NOTE: These pokes & Games are excluded from GEN_FALLBACK (file substitution)
ALT_GAME_MAP = {
    # NOTE: Technically the gen5 starters have different animations (NOT statics) for b2w2 vs bw, but I'm not going to put that logic in since I'm axing alts
    "BW_B2W2": {
        ("Keldeo", "-Form_Resolute"),
        ("Kyurem", "-Form_Black"),
        ("Kyurem", "-Form_White"),
        ("Landorus", "-Form_Therian"),
        ("Thundurus", "-Form_Therian"),
        ("Tornadus", "-Form_Therian")
    },

    "XY_ORAS": {
        ("Groudon", "-Form_Primal"),
        ("Kyogre", "-Form_Primal"),
        ("Hoopa", "-Form_Unbound"),
        ("Altaria", "-Mega"),
        ("Audino", "-Mega"),
        ("Beedrill", "-Mega"),
        ("Camerupt", "-Mega"), 
        ("Diancie", "-Mega"),
        ("Gallade", "-Mega"),
        ("Glalie", "-Mega"),
        ("Lopunny", "-Mega"), 
        ("Metagross", "-Mega"),
        ("Pidgeot", "-Mega"),
        ("Rayquaza", "-Mega"),
        ("Sableye", "-Mega"), 
        ("Salamence", "-Mega"),
        ("Sceptile", "-Mega"),
        ("Sharpedo", "-Mega"),
        ("Slowbro", "-Mega"), 
        ("Steelix", "-Mega"),
        ("Swampert", "-Mega"),
        ("Pikachu", "-Form_Cosplay"),
        ("Pikachu", "-Form_Cosplay_Belle"),
        ("Pikachu", "-Form_Cosplay_Libre"), 
        ("Pikachu", "-Form_Cosplay_PhD"),
        ("Pikachu", "-Form_Cosplay_Pop_Star"),
        ("Pikachu", "-Form_Cosplay_Rock_Star")
    },

    "SM_USUM": {
        ("Blacephalon", ""),
        ("Lycanroc", "-Form_Dusk"),
        ("Naganadel", ""),
        ("Necrozma", "-Form_Dusk_Mane"),
        ("Necrozma", "-Form_Dawn_Wings"),
        ("Necrozma", "-Form_Ultra"),
        ("Pikachu", "-Form_Cap_Partner"),
        ("Poipole", ""),
        ("Stakataka", ""),
        ("Zeraora", "")
    }
}