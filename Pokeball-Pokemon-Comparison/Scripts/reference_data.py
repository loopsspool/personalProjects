# TODO: Put all these mappings in a seperate file, with static dicts and whatnot from db_utils
# TODO: Also put db_utils exclusions and exceptions into a seperate file
############################# BULBA TRANSLATORS #############################
BULBA_GAME_MAP = {
    # Gen included so Gold doesn't trigger Golduck, Yellow trigger Yellow Core Minior, etc
    "Gen1 Red_Blue": "1b",
    "Gen1 Red_Green": "1g",
    "Gen1 Yellow": "1y",
    "Gen2 Crystal": "2c",
    "Gen2 Gold": "2g",
    "Gen2 Silver": "2s",
    "Gen3 Emerald": "3e",
    "Gen3 FRLG": "3f",
    "Gen3 Ruby_Sapphire": "3r",
    "Gen4 Diamond_Pearl": "4d",
    "Gen4 HGSS": "4h",
    "Gen4 Platinum": "4p",
    "Gen5 BW_B2W2": "5b",   # TODO: 5b2 may exist? Check on any missing after
    "Gen6 XY_ORAS": "6x",   # TODO: 6o may exist? Check on any missing after
    "Gen7 SM_USUM": "7s",
    "Gen7 LGPE": "7p",
    "Gen8 SwSh": "8s",
    # Doesn't look like bulba has any BDSP sprites... Can confirm by checking pokes unavailable in SwSh & LA
    "Gen8 LA": "8a"
}


BULBA_DOUBLE_FORM_MAP = {
    6: ({"-Mega"}, ["-Mega_X", "-Mega_Y"]),  # Charizard has two mega forms
    128: ({"-Region_Paldea", "-Form_Combat", "-Form_Blaze", "-Form_Aqua"}, ["-Region_Paldea-Form_Combat", "-Region_Paldea-Form_Blaze", "-Region_Paldea-Form_Aqua"]),     # Only Paldean Tauros has misc forms
    150: ({"-Mega"}, ["-Mega_X", "-Mega_Y"]),  # Mewtwo has two mega forms
    215: (set(), ["-Region_Hisui-f"]),   # *Just adding* Sneasel's female Hisuian form 
    555: ({"-Region_Galar"}, ["-Region_Galar-Form_Standard", "-Region_Galar-Form_Zen"]),     # Galarian Darmanitan has his misc forms too
    892: ({"-Gigantamax"}, ["-Gigantamax-Form_Single_Strike", "-Gigantamax-Form_Rapid_Strike"])     # Urshifu forms impact gigantamax appearance
    }


BULBA_FORM_MAP = {
    "-Mega": "M",
    # MegaX&Y
    "-Gigantamax": "Gi",
    "-Region_Alola": "A",
    "-Ragion_Galar": "G",
    # Region Hisui, Paldea
}