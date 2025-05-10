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


POKEBALL_IMG_TYPE_APPLICABILITY = {
    "Bag_Gen4": ["Lure Ball", "Park Ball"],  # This is for some gen4 exlusive differences (lure ball, park ball)
    "Gen5_Summary": ["Lure Ball"],  # Only for pokeballs that had differences in gen 4
    "Gen7_Battle": ["Beast Ball"],  # Beast Ball introduced in gen7, didn't follow 3ds naming convention for gen6 battles
    "LA_Summary": ["Strange Ball", "Poke Ball-Hisui", "Great Ball-Hisui", "Ultra Ball-Hisui", "Feather Ball", "Wing Ball", "Jet Ball", "Heavy Ball-Hisui", "Leaden Ball", "Gigaton Ball", "Origin Ball"]    # Only pokeballs in LA
}


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
    "gen7_battle_only_for_beast_ball": lambda ball_info, img_type_info: img_type_info["name"] == "Gen7_Battle" and ball_info["name"] != "Beast Ball",

    # Balls
    # Putting this here so I dont have to make it game exclusive and add a new game every time one releases, since this ball is probably sticking around
    # Also excluded older games for the same reason, so a newer game doesn't have to be explicitly added
    "strange_ball_img_exclusions": lambda ball_info, img_type_info: ball_info["name"] == "Strange Ball" and img_type_info["name"] in ("Bag")
}
def should_exclude_pokeball_img(ball_info, img_type_info):
    for reason, exclusion in POKEBALL_IMG_EXCLUSIONS.items():
        if exclusion(ball_info, img_type_info): return True
    return False


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
    {"name": "Gen5_Battle", "gen": 5},
    {"name": "Gen5_Battle-Animated", "gen": 5},
    {"name": "Gen6_Battle", "gen": 6},
    {"name": "Gen7_Battle", "gen": 7},  # Only for beast ball since introduced in gen7
    {"name": "Gen8", "gen": 8},
    {"name": "LA_Summary", "gen": 8},
    {"name": "HOME", "gen": -1}, # Setting home to gen1 so it will apply to all pokeballs

]