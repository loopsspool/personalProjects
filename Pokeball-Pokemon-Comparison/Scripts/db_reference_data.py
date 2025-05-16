#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     IMPORT WORKAROUND     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|
import importlib
# To cache dynamically imported funcs so it only imports once
# Necessary to avoid circular import
_module_cache = {}
def lazy_import(module_name):
    if module_name not in _module_cache:
        _module_cache[module_name] = importlib.import_module(module_name)
    return _module_cache[module_name]




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     GAME DATA     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

# NOTE: These are in chronological order and that is IMPORTANT since I rely on game ids sometimes for form filtering (eg mid gen form introductions)
GAMES = (
    ("Red_Green", 1),
    ("Red_Blue", 1),
    ("Yellow", 1),
    ("Gold", 2),
    ("Silver", 2),
    ("Crystal", 2),
    ("Ruby_Sapphire", 3),
    ("FRLG", 3),
    ("Emerald", 3),
    ("Diamond_Pearl", 4),
    ("Platinum", 4),
    ("HGSS", 4),
    ("BW_B2W2", 5),
    ("XY_ORAS", 6),
    ("SM_USUM", 7),
    ("LGPE", 7),
    ("SwSh", 8),
    ("BDSP", 8),
    ("LA", 8),
    ("SV", 9)
)


# If no file exists for the key game, it may be a recycled sprite from the value games
# Used to evaulte "substitution" sprites 
GAME_FALLBACKS = {
    "Gen2 Silver": ["Gen2 Gold", "Gen2 Crystal"],
    "Gen2 Crystal": ["Gen2 Gold"],
    "Gen3 Emerald": ["Gen3 Ruby_Sapphire", "Gen3 FRLG"],
    "Gen3 FRLG": ["Gen3 Ruby_Sapphire"],
    "Gen4 HGSS": ["Gen4 Platinum", "Gen4 Diamond_Pearl"],
    "Gen4 Platinum": ["Gen4 Diamond_Pearl"],
    "Gen6 XY_ORAS": ["Gen7 SM_USUM"],
    "Gen7 SM_USUM": ["Gen6 XY_ORAS"]
}




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     POKEMON DATA     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     FORMS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|

NO_DEFAULT_FORM_POKE_NUMS = {201, 412, 413, 421, 422, 423, 487, 492, 493, 550, 555, 585, 586, 641, 642, 645, 647, 648, 
                             666, 669, 670, 671, 681, 710, 711, 716, 718, 720, 741, 745, 746, 773, 774, 778, 849, 869, 
                             875, 877, 888, 889, 892, 905, 925, 931, 964, 978, 982, 999, 1017, 1024}


STAMPED_FORM_POKES = {854, 855, 1012, 1013}


# Poke_num: ({"remove_this, "and_this"}, ["replace_with_this", "and_this"])
FORM_EXCEPTION_POKEMON = {
    6: ({"-Mega"}, ["-Mega_X", "-Mega_Y"]),  # Charizard has two mega forms
    128: ({"-Region_Paldea", "-Form_Combat", "-Form_Blaze", "-Form_Aqua"}, ["-Region_Paldea-Form_Combat", "-Region_Paldea-Form_Blaze", "-Region_Paldea-Form_Aqua"]),     # Only Paldean Tauros has misc forms
    150: ({"-Mega"}, ["-Mega_X", "-Mega_Y"]),  # Mewtwo has two mega forms
    215: (set(), ["-Region_Hisui-f"]),   # *Just adding* Sneasel's female Hisuian form 
    555: ({"-Region_Galar"}, ["-Region_Galar-Form_Standard", "-Region_Galar-Form_Zen"]),     # Galarian Darmanitan has his misc forms too
    892: ({"-Gigantamax"}, ["-Gigantamax-Form_Single_Strike", "-Gigantamax-Form_Rapid_Strike"])     # Urshifu forms impact gigantamax appearance
    }


# Minior and Alcremie have special "shared" forms for their shinies
SHARED_SHINY_FORMS = {  774: ["-Form_Core"], 
                        869: ["-Form_Berry_Sweet", "-Form_Clover_Sweet", "-Form_Flower_Sweet", "-Form_Love_Sweet", "-Form_Ribbon_Sweet", "-Form_Star_Sweet", "-Form_Strawberry_Sweet"]
}


FORM_EXCLUSIONS = {
    # Species game availability
    "filtering_for_LGPE_dex_if_needed": lambda poke_form, game: game["name"] == "LGPE" and lazy_import("spreadsheet_utils").poke_isnt_in_game(poke_form["poke num"], "LGPE"),
    "filtering_for_SwSh_dex_if_needed": lambda poke_form, game: game["name"] == "SwSh" and lazy_import("spreadsheet_utils").poke_isnt_in_game(poke_form["poke num"], "SwSh"),
    "filtering_for_BDSP_dex_if_needed": lambda poke_form, game: game["name"] == "BDSP" and lazy_import("spreadsheet_utils").poke_isnt_in_game(poke_form["poke num"], "BDSP"),
    "filtering_for_LA_dex_if_needed": lambda poke_form, game: game["name"] == "LA" and lazy_import("spreadsheet_utils").poke_isnt_in_game(poke_form["poke num"], "LA"),
    "filtering_for_SV_dex_if_needed": lambda poke_form, game: game["name"] == "SV" and lazy_import("spreadsheet_utils").poke_isnt_in_game(poke_form["poke num"], "SV"),

    # Universal Rules
    "no_pokemon_with_a_higher_generation_than_game_generation": lambda poke_form, game: poke_form["poke gen"] > game["gen"],
    "no_f_form_visual_differences_before_gen_4": lambda poke_form, game: poke_form["form name"] == "-f" and game["gen"] < 4,
    "no_fairy_forms_before_gen_6": lambda poke_form, game: poke_form["form name"] == "-Form_Fairy" and game["gen"] < 6,
    "no_megas_outside_XY_ORAS_SM_USUM_LGPE": lambda poke_form, game: "-Mega" in poke_form["form name"] and game["name"] not in ("XY_ORAS", "SM_USUM", "LGPE"),
    "no_gigantamax_outside_SwSh": lambda poke_form, game: poke_form["form name"] == "-Gigantamax" and game["name"] != "SwSh",
    "no_regional_forms_before_gen_7": lambda poke_form, game: "-Region" in poke_form["form name"] and game["gen"] < 7,
    "no_alolan_forms_before_SM_USUM": lambda poke_form, game: "-Region_Alola" in poke_form["form name"] and lazy_import("db_utils").get_game_id(game["name"]) < lazy_import("db_utils").get_game_id("SM_USUM"),
    "no_galarian_forms_before_SwSh": lambda poke_form, game: "-Region_Galar" in poke_form["form name"] and lazy_import("db_utils").get_game_id(game["name"]) < lazy_import("db_utils").get_game_id("SwSh"),
    "no_hisuian_forms_before_LA": lambda poke_form, game: "-Region_Hisui" in poke_form["form name"] and lazy_import("db_utils").get_game_id(game["name"]) < lazy_import("db_utils").get_game_id("LA"),
    "no_paldean_forms_before_SV": lambda poke_form, game: "-Region_Paldea" in poke_form["form name"] and lazy_import("db_utils").get_game_id(game["name"]) < lazy_import("db_utils").get_game_id("SV"),
    "no_regional_forms_in_BDSP": lambda poke_form, game: game["name"] == "BDSP" and "-Region" in poke_form["form name"],
    "no_regional_forms_in_LA_other_than_hisui_and_alola_kitties": lambda poke_form, game: game["name"] == "LA" and "-Region" in poke_form["form name"] and "-Region_Hisui" not in poke_form["form name"] and not (poke_form["poke name"] in ("Vulpix", "Ninetales") and poke_form["form name"] == "-Region_Alola"),

    # Specific pokemon
    "no_cosplay_pikachu_outside_ORAS": lambda poke_form, game: poke_form["poke num"] == 25 and "-Form_Cosplay" in poke_form["form name"] and game["name"] != "XY_ORAS",
    "no_cap_pikachu_before_gen_7": lambda poke_form, game: poke_form["poke num"] == 25 and "-Form_Cap" in poke_form["form name"] and game["gen"] < 7,
    "no_cap_pikachu_in_these_games": lambda poke_form, game: poke_form["poke num"] == 25 and "-Form_Cap" in poke_form["form name"] and game["name"] in ("LGPE", "BDSP", "LA"),  # Don't have to add earlier games because line above filters out everything below gen 7
    "no_world_cap_pikachu_in_SM_USUM": lambda poke_form, game: poke_form["poke num"] == 25 and poke_form["form name"] == "-Form_Cap_World" and game["name"] == "SM_USUM",
    "no_female_form_eevees_until_gen_8": lambda poke_form, game: poke_form["poke num"] == 133 and poke_form["form name"] == "-f" and game["gen"] < 8,
    "no_spiky_eared_pichu_outside_HGSS": lambda poke_form, game: poke_form["poke num"] == 172 and poke_form["form name"] == "-Form_Spiky_Eared" and game["name"] != "HGSS",
    "no_unown_punctuation_before_gen_3": lambda poke_form, game: poke_form["poke num"] == 201 and poke_form["form name"] in ("-Form_!", "-Form_Qmark") and game["gen"] < 3,
    "no_primal_kyogre_or_groudon_outside_XY_ORAS_and_SM_USUM": lambda poke_form, game: (poke_form["poke num"] in (382, 383)) and poke_form["form name"] == "-Form_Primal" and game["name"] not in ("XY_ORAS", "SM_USUM"),
    "no_deoxys_non_normal_forms_in_ruby_sapphire": lambda poke_form, game: poke_form["poke num"] == 386 and game["name"] == "Ruby_Sapphire" and poke_form["form name"] != "Default",
    "no_deoxys_speed_form_in_FRLG": lambda poke_form, game: poke_form["poke num"] == 386 and game["name"] == "FRLG" and poke_form["form name"] == "-Form_Speed",
    "no_deoxys_attack_and_defense_form_in_emerald": lambda poke_form, game: poke_form["poke num"] == 386 and game["name"] == "Emerald" and poke_form["form name"] in ("-Form_Attack", "-Form_Defense"),
    "no_rotom_forms_until_after_platinum": lambda poke_form, game: poke_form["poke num"] == 479 and poke_form["form name"] != "Default" and lazy_import("db_utils").get_game_id(game["name"]) < lazy_import("db_utils").get_game_id("Platinum"),
    "no_origin_dialga_palkia_forms_until_after_LA": lambda poke_form, game: poke_form["poke num"] in (483, 484) and poke_form["form name"] == "-Form_Origin" and lazy_import("db_utils").get_game_id(game["name"]) < lazy_import("db_utils").get_game_id("LA"),
    "no_origin_form_giratina_until_after_platinum": lambda poke_form, game: poke_form["poke num"] == 487 and poke_form["form name"] == "-Form_Origin" and lazy_import("db_utils").get_game_id(game["name"]) < lazy_import("db_utils").get_game_id("Platinum"),
    "no_sky_form_shaymin_until_after_platinum": lambda poke_form, game: poke_form["poke num"] == 492 and poke_form["form name"] == "-Form_Sky" and lazy_import("db_utils").get_game_id(game["name"]) < lazy_import("db_utils").get_game_id("Platinum"),
    "no_???_arceus_form_outside_of_gen_4": lambda poke_form, game: poke_form["poke num"] == 493 and poke_form["form name"] == "-Form_Qmark" and game["gen"] != 4,
    "no_white_striped_basculin_until_LA": lambda poke_form, game: poke_form["poke num"] == 550 and poke_form["form name"] == "-Form_White_Striped" and lazy_import("db_utils").get_game_id(game["name"]) < lazy_import("db_utils").get_game_id("LA"),
    "no_ash_greninja_outside_of_SM_USUM": lambda poke_form, game: poke_form["poke num"] == 658 and poke_form["form name"] == "-Form_Ash" and game["name"] != "SM_USUM",
    "no_zygarde_forms_until_gen_7": lambda poke_form, game: poke_form["poke num"] == 718 and poke_form["form name"] != "-Form_50%" and game["gen"] < 7,
    "no_solgaleo_lunala_forms_outside_SM_USUM": lambda poke_form, game: poke_form["poke num"] in (791, 792) and poke_form["form name"] != "Default" and game["name"] != "SM_USUM",
    "no_zenith_marshadow_form_outside_gen_SM_USUM": lambda poke_form, game: poke_form["poke num"] == 802 and poke_form["form name"] != "Default" and game["name"] != "SM_USUM",
    "no_meltan_or_melmetal_until_LGPE": lambda poke_form, game: poke_form["poke num"] in (808, 809) and lazy_import("db_utils").get_game_id(game["name"]) < lazy_import("db_utils").get_game_id("LGPE"),    # Technically these are gen 7 pokemon, they just werent introduced until LGPE
    "no_stamped_poke_sprites_in_games": lambda poke_form, game: poke_form["poke num"] in (854, 855, 1012, 1013) and poke_form["form name"] != "Default"     # Both forms look the same except for the stamp, which is really only visible in HOME anyways. This is where the stamp img will be downloaded
}



#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     SPRITES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|

# Default meaning front, normal color, static sprite
SPRITE_TYPES = ["Default", "-Animated", "-Shiny", "-Shiny-Animated", "-Back", "-Back-Animated", "-Shiny-Back", "-Shiny-Back-Animated"]

# Home sprites use the above sprite types with the exception of the below
# NOTE: Back sprites are also excluded (no HOME back sprites), but are used for Stamped form pokemon to show stamps (854, 855, 1012, 1013)
HOME_SPRITE_EXCLUDE = {"-Back-Animated", "-Shiny-Back-Animated"}


# Certain rules to be excluded but exist elsewhere, for nonexistant sprites, see NONEXISTANT_SPRITES
SPRITE_EXCLUSIONS = {
    # UNIVERSAL EXCLUSIONS
    "no_sprites_if_form_is_unavailable": lambda pfgo_info, sprite_type: pfgo_info["obtainable"] == 0,
    "no_shiny_sprites_in_gen_1": lambda pfgo_info, sprite_type: pfgo_info["game gen"] == 1 and "Shiny" in sprite_type,
    "no_animated_sprites_in_gen_1": lambda pfgo_info, sprite_type: pfgo_info["game gen"] == 1 and "Animated" in sprite_type,
    "no_animated_back_sprites_below_gen_5": lambda pfgo_info, sprite_type: pfgo_info["game gen"] < 5 and "-Back-Animated" in sprite_type,
    "no_animated_sprites_in_these_games": lambda pfgo_info, sprite_type: pfgo_info["game name"] in ("Gold", "Silver", "FRLG", "Ruby_Sapphire") and "Animated" in sprite_type,

    # INDIVIDUAL POKEMON
    "no_shiny_castform_forms_until_gen_8": lambda pfgo_info, sprite_type: pfgo_info["poke num"] == 351 and pfgo_info["form name"] != "Default" and "Shiny" in sprite_type and pfgo_info["game gen"] < 8
}


# Sprites that don't exist. Shouldn't even be marked unobtainable, which is why theyre here not SPRITE_EXCLUSIONS
NONEXISTANT_SPRITES={
    # UNIVERSAL EXCLUSIONS
    "skip_all_shared_shiny_forms_that_arent_adjusted_appropriately": lambda poke_num, form_name, sprite_type: poke_num in SHARED_SHINY_FORMS and "Shiny" in sprite_type and form_name not in SHARED_SHINY_FORMS[poke_num],
    "skip_all_non_shiny_sprites_for_shared_shinies_that_are_adjusted": lambda poke_num, form_name, sprite_type: poke_num in SHARED_SHINY_FORMS and "Shiny" not in sprite_type and form_name in SHARED_SHINY_FORMS[poke_num],

    # INDIVIDUAL POKEMON
    # Now, technically the games had cosplay pikachu shiny locked. However, you can get around this and Wikidex has sprites for it, so why not include it
    #"no_shiny_cosplay_pikachu": lambda poke_num, form_name, sprite_type: poke_num == 25 and "-Form_Cosplay" in form_name and "Shiny" in sprite_type,
    "no_shiny_cap_pikachu": lambda poke_num, form_name, sprite_type: poke_num == 25 and "-Form_Cap" in form_name and "Shiny" in sprite_type,
    # The below only affects home because (non-default) forms of the stamped pokes were already marked as unobtainable in games (since no way to see stamp in game and all other sprites are identical)
    # Further processing is done in the generate_home_filenames function to exclude default form back sprites (couldn't include here bc would also filter them for games)
    "no_stamped_poke_forms_except_show_stamp_back_sprite": lambda poke_num, form_name, sprite_type: poke_num in (854, 855, 1012, 1013) and form_name != "Default" and sprite_type not in ("-Back", "-Shiny-Back")
}


NO_DRAWN_FORMS = {
    172: {"-Form_Spiky_Eared"},
    493: {"-Form_Qmark"},
    # Only using Average Size for drawn 710-711
    710: {"-Form_Small_Size", "-Form_Large_Size", "-Form_Super_Size"},
    711: {"-Form_Small_Size", "-Form_Large_Size", "-Form_Super_Size"},
    854: {"-Form_Antique", "-Form_Phony"},
    855: {"-Form_Antique", "-Form_Phony"},
    1012: {"-Form_Artisan", "-Form_Counterfeit"},
    1013: {"-Form_Masterpiece", "-Form_Unremarkable"},
}
# Excludes shared shiny forms (minior, alcremie, etc)
for k,v in SHARED_SHINY_FORMS.items(): NO_DRAWN_FORMS[k] = set(v)




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     POKEBALL DATA     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

POKEBALLS = [
    {"name": "Poke Ball", "gen": 1},
    {"name": "Great Ball", "gen": 1},
    {"name": "Ultra Ball", "gen": 1},
    {"name": "Master Ball", "gen": 1},
    {"name": "Safari Ball", "gen": 1},
    {"name": "Fast Ball", "gen": 2},
    {"name": "Level Ball", "gen": 2},
    {"name": "Lure Ball", "gen": 2},
    {"name": "Heavy Ball", "gen": 2},
    {"name": "Love Ball", "gen": 2},
    {"name": "Friend Ball", "gen": 2},
    {"name": "Moon Ball", "gen": 2},
    {"name": "Sport Ball", "gen": 2},
    {"name": "Net Ball", "gen": 3},
    {"name": "Dive Ball", "gen": 3},
    {"name": "Nest Ball", "gen": 3},
    {"name": "Repeat Ball", "gen": 3},
    {"name": "Timer Ball", "gen": 3},
    {"name": "Luxury Ball", "gen": 3},
    {"name": "Premier Ball", "gen": 3},
    {"name": "Dusk Ball", "gen": 4},
    {"name": "Heal Ball", "gen": 4},
    {"name": "Quick Ball", "gen": 4},
    {"name": "Cherish Ball", "gen": 4},
    {"name": "Park Ball", "gen": 4},
    {"name": "Dream Ball", "gen": 5},
    {"name": "Beast Ball", "gen": 7},
    {"name": "Strange Ball", "gen": 8},
    # Hisuian
    {"name": "Poke Ball-Hisui", "gen": 8, "exclusive_to": "LA, HOME"},
    {"name": "Great Ball-Hisui", "gen": 8, "exclusive_to": "LA, HOME"},
    {"name": "Ultra Ball-Hisui", "gen": 8, "exclusive_to": "LA, HOME"},
    {"name": "Feather Ball-Hisui", "gen": 8, "exclusive_to": "LA, HOME"},
    {"name": "Wing Ball-Hisui", "gen": 8, "exclusive_to": "LA, HOME"},
    {"name": "Jet Ball-Hisui", "gen": 8, "exclusive_to": "LA, HOME"},
    {"name": "Heavy Ball-Hisui", "gen": 8, "exclusive_to": "LA, HOME"},
    {"name": "Leaden Ball-Hisui", "gen": 8, "exclusive_to": "LA, HOME"},
    {"name": "Gigaton Ball-Hisui", "gen": 8, "exclusive_to": "LA, HOME"},
    {"name": "Origin Ball-Hisui", "gen": 8, "exclusive_to": "LA, HOME"}
]


GAMES_W_BALL_EXCLUSIVES = ["LA"]

# Certain img types only apply to certain balls
# If lambda evaluates to True, will be excluded
POKEBALL_IMG_EXCLUSIONS = {
    # Universal
    "ball_intoductory_gen_should_be_less_than_or_equal_to_img_type_gen": lambda ball_info, img_type_info: img_type_info["gen"] != -1 and img_type_info["gen"] < ball_info["gen"],
    "game_exclusive_balls_should_only_have_img_types_with_those_games_in_it": lambda ball_info, img_type_info: ball_info["exclusive_to"] is not None and not any(platform in img_type_info["name"] for platform in ball_info["exclusive_to"].split(", ")),
    "non_game_exclusive_balls_should_not_be_included_in_exclusionary_games_except_strange_ball": lambda ball_info, img_type_info: ball_info["exclusive_to"] == None and any(game in img_type_info["name"] for game in GAMES_W_BALL_EXCLUSIVES) and ball_info["name"] != "Strange Ball",
    "no_HOME_bag_sprites_for_pokeballs_introduced_before_gen8": lambda ball_info, img_type_info: ball_info["gen"] < 8 and img_type_info["name"] == "Bag_HOME",
    "no_PGL_dream_imgs_after_discontinued_in_gen_7": lambda ball_info, img_type_info: ball_info["gen"] > 7 and img_type_info["name"] == "PGL",

    # Image types
    "gen4_bag_sprites_only_for_gen_4_diifferences": lambda ball_info, img_type_info: img_type_info["name"] == "Bag_Gen4" and ball_info["name"] not in ("Lure Ball", "Park Ball"),
    "gen5_summary_only_for_balls_w_gen_4_diifferences": lambda ball_info, img_type_info: img_type_info["name"] == "Gen5_Summary" and ball_info["name"] not in ("Lure Ball", "Park Ball"),
    "gen7_battle_only_for_beast_ball": lambda ball_info, img_type_info: img_type_info["name"] == "Gen7" and ball_info["name"] != "Beast Ball",

    # Balls
    # Putting this here so I dont have to make it game exclusive and add a new game every time one releases, since this ball is probably sticking around
    # Also excluded older games for the same reason, so a newer game doesn't have to be explicitly added
    "strange_ball_img_exclusions": lambda ball_info, img_type_info: ball_info["name"] == "Strange Ball" and img_type_info["name"] in ("Bag")
}


# TODO: Add gen2 images?
# Gen refers to when img_sprite was introduced, balls should be less than or equal to this in order to have that sprite
# Gen -1 means it applies to all balls regardless of generation
POKEBALL_IMG_TYPES = [
    {"name": "Bag", "gen": -1},
    {"name": "Bag_Gen4", "gen": 4},   # This is for some gen4 exlusive differences (lure ball, park ball)
    {"name": "Bag_HOME", "gen": 8}, # So far this only applies to exclusively gen 8 balls (I assume the rest were recycled into home via game bag sprites)
    {"name": "Bag_BDSP", "gen": -1},
    {"name": "Bag_LA", "gen": 8},
    {"name": "Bag_SV", "gen": -1},

    {"name": "PGL", "gen": -1}, # Pokemon global link (Dream)
    {"name": "Drawn", "gen": -1}, # Drawn (Sugimori)

    {"name": "Gen3", "gen": 3},
    {"name": "Gen4_Battle", "gen": 4},
    {"name": "Gen4_Summary", "gen": 4},
    {"name": "Gen5_Summary", "gen": 5},    # Only for pokeballs that had differences in gen 4
    # Frames of Gen5_Battle-Animated
    {"name": "Gen5_Battle-Static_0", "gen": 5},
    {"name": "Gen5_Battle-Static_1", "gen": 5},
    {"name": "Gen5_Battle-Static_2", "gen": 5},
    {"name": "Gen5_Battle-Static_3", "gen": 5},
    {"name": "Gen5_Battle-Static_4", "gen": 5},
    {"name": "Gen5_Battle-Static_5", "gen": 5},
    {"name": "Gen5_Battle-Static_6", "gen": 5},
    {"name": "Gen5_Battle-Static_7", "gen": 5},
    {"name": "Gen5_Battle-Static_8", "gen": 5},
    {"name": "Gen5_Battle-Animated", "gen": 5},
    {"name": "Gen6", "gen": 6},
    {"name": "Gen7", "gen": 7},  # Only for beast ball since introduced in gen7
    {"name": "Gen8", "gen": 8},
    {"name": "LA_Summary", "gen": 8},
    {"name": "HOME", "gen": -1}, # Setting home to gen1 so it will apply to all pokeballs

]