POKEBALLS = [
    {"name": "Poke Ball", "gen": 1, "LA_only": False},
    {"name": "Great Ball", "gen": 1, "LA_only": False},
    {"name": "Ultra Ball", "gen": 1, "LA_only": False},
    {"name": "Master Ball", "gen": 1, "LA_only": False},
    {"name": "Safari Ball", "gen": 1, "LA_only": False},
    {"name": "Fast Ball", "gen": 2, "LA_only": False},
    {"name": "Level Ball", "gen": 2, "LA_only": False},
    {"name": "Lure Ball", "gen": 2, "LA_only": False},
    {"name": "Heavy Ball", "gen": 2, "LA_only": False},
    {"name": "Love Ball", "gen": 2, "LA_only": False},
    {"name": "Friend Ball", "gen": 2, "LA_only": False},
    {"name": "Moon Ball", "gen": 2, "LA_only": False},
    {"name": "Sport Ball", "gen": 2, "LA_only": False},
    {"name": "Net Ball", "gen": 3, "LA_only": False},
    {"name": "Dive Ball", "gen": 3, "LA_only": False},
    {"name": "Nest Ball", "gen": 3, "LA_only": False},
    {"name": "Repeat Ball", "gen": 3, "LA_only": False},
    {"name": "Timer Ball", "gen": 3, "LA_only": False},
    {"name": "Luxury Ball", "gen": 3, "LA_only": False},
    {"name": "Premier Ball", "gen": 3, "LA_only": False},
    {"name": "Dusk Ball", "gen": 4, "LA_only": False},
    {"name": "Heal Ball", "gen": 4, "LA_only": False},
    {"name": "Quick Ball", "gen": 4, "LA_only": False},
    {"name": "Cherish Ball", "gen": 4, "LA_only": False},
    {"name": "Park Ball", "gen": 4, "LA_only": False},
    {"name": "Dream Ball", "gen": 5, "LA_only": False},
    {"name": "Beast Ball", "gen": 7, "LA_only": False},
    {"name": "Strange Ball", "gen": 8, "LA_only": False},
    {"name": "Poke Ball-Hisui", "gen": 8, "LA_only": True},
    {"name": "Great Ball-Hisui", "gen": 8, "LA_only": True},
    {"name": "Ultra Ball-Hisui", "gen": 8, "LA_only": True},
    {"name": "Feather Ball", "gen": 8, "LA_only": True},
    {"name": "Wing Ball", "gen": 8, "LA_only": True},
    {"name": "Jet Ball", "gen": 8, "LA_only": True},
    {"name": "Heavy Ball-Hisui", "gen": 8, "LA_only": True},
    {"name": "Leaden Ball", "gen": 8, "LA_only": True},
    {"name": "Gigaton Ball", "gen": 8, "LA_only": True},
    {"name": "Origin Ball", "gen": 8, "LA_only": True}
]

# TODO: Adjust to how you want named, will do bulba translation later
POKEBALL_IMG_TYPES = [
    # For bag sprites, gen is referring to how far back the balls go 
    {"name": "Bag", "gen": 1},
    {"name": "Bag IV", "gen": 4},   # This is for some gen4 exlusive differences (lure ball, park ball)
    {"name": "HOME Bag", "gen": 8}, # So far this only applies to exclusively gen 8 balls (I assume the rest were recycled into home via game bag sprites)
    {"name": "BDSP Bag", "gen": 1},
    {"name": "LA Bag", "gen": 8},
    {"name": "SV Bag", "gen": 1},

    {"name": "Dream", "gen": 1}, # Pokemon global link
    {"name": "Sugimori", "gen": 1}, # Drawn

    {"name": "III", "gen": 3},  # TODO: Ultra ball different in FRLG & Em than R_S, figure out
    {"name": "battle IV", "gen": 4},
    {"name": "summary IV", "gen": 4},
    {"name": "summary V", "gen": 5},    # Only for pokeballs that had differences in gen 4
    {"name": "battle V", "gen": 5},
    {"name": "battle 3DS", "gen": 6},
    {"name": "VIII", "gen": 8},
    {"name": "HOME", "gen": 1}, # Setting home to gen1 so it will apply to all pokeballs

]