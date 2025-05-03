# TODO: Put all these mappings in a seperate file, with static dicts and whatnot from db_utils
# TODO: Also put db_utils exclusions and exceptions into a seperate file
############################# BULBA TRANSLATORS #############################
# These will be excluded if tried to run through the game sprite image downloader
BULBA_DOESNT_HAVE_GAME_IMGS_FOR = ["Gen9 SV", "Gen9_SV", "Gen8 BDSP", "Gen8_BDSP"]

# Only allows male denoter on bulba translated file if these strings not in my filename
# MUST KEEP SPACE AND UNDERSCORE -- No easy way to get gen when calling this, and dont want gen1 to filter gen10
MALE_DENOTER_EXCLUSION_GENS = ["Gen1 ", "Gen1_", "Gen2 ", "Gen2_", "Gen3 ", "Gen3_"]

# Allows universal forms (regions, mega, etc) to be paired w female forms (See Hisuian Sneasel)
FEMALE_DENOTER_UNIVERSAL_FORM_EXCEPTION_POKEMON = ["0215"]

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



# NOTE: If poke num here, cannot also be in BULBA_GAMES_SPECIFIC_FORM_MAP
# NOTE: If there's spaces, replace them with an underscore for the url
BULBA_GAME_INCONSISTENCIES = {
    # Just an example for formatting, will try to find which image exists between A, -A, and ""
    #201: { "-Form_A": ["A", "-A", ""]}
}


# This is to filter out specific forms when building bulba filename
# The exceptions that have a universal AND specific form (See 555 Galarian Darmanitan Zen form) have their own unique form id generated in db_utils > FORM_EXCEPTION_POKEMON
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


# NOTE: Gigantamax pulled out due to Urshifu bulba names, where forms are put before gigantamax
BULBA_GAMES_UNIVERSAL_FORM_MAP = {
    "-Mega_X": "MX",
    "-Mega_Y": "MY",
    "-Mega": "M",   # This after X&Y so when looping through Mega wont trigger a form meant to be X or Y
    "-Region_Alola": "A",
    "-Region_Galar": "G",
    "-Region_Hisui": "H",
    "-Region_Paldea": "P"
}


BULBA_TYPE_FORM_MAP = {
    "-Form_Normal": "",  # Normal form considered default: so does not have a letter denoter
    "-Form_Fighting": "-Fighting", 
    "-Form_Flying": "-Flying", 
    "-Form_Poison": "-Poison", 
    "-Form_Ground": "-Ground", 
    "-Form_Rock": "-Rock", 
    "-Form_Bug": "-Bug", 
    "-Form_Ghost": "-Ghost", 
    "-Form_Steel": "-Steel", 
    "-Form_Fire": "-Fire", 
    "-Form_Water": "-Water", 
    "-Form_Grass": "-Grass", 
    "-Form_Electric": "-Electric", 
    "-Form_Psychic": "-Psychic", 
    "-Form_Ice": "-Ice", 
    "-Form_Dragon": "-Dragon", 
    "-Form_Dark": "-Dark", 
    "-Form_Fairy": "-Fairy", 
    "-Form_Qmark": "-Unknown"
}


# TODO: Before actually downloading, make sure you have all these, cross reference w poke info spreadsheet
BULBA_GAMES_SPECIFIC_FORM_MAP = {
    #Pikachu
    25: {
        "-Form_Cap_Alola": "A",
        "-Form_Cap_Hoenn": "H",
        "-Form_Cap_Kalos": "K",
        "-Form_Cap_Original": "O",
        "-Form_Cap_Sinnoh": "S",
        "-Form_Cap_Unova": "U",
        "-Form_Cap_Partner": "P",
        "-Form_Cap_World": "W",
        
        # These aren't actually in bulba, I just don't want them to pull the default by returning an empty string
        "-Form_Cosplay_Belle": "B",
        "-Form_Cosplay_Libre": "L",
        "-Form_Cosplay_PhD": "PhD",
        "-Form_Cosplay_Pop_Star": "Pop",
        "-Form_Cosplay_Rock_Star": "Ro"
    },

    # Tauros
    128: {
        "-Form_Combat": "C", 
        "-Form_Blaze": "B", 
        "-Form_Aqua": "A"
    },

    # Pichu
    172: {"-Form_Spiky_Eared": "N"},

    # Unown
    # Hyphens and one-off differences handled in bulba_scraping_utils where needed
    201: {
        "-Form_A": "",
        "-Form_B": "B",
        "-Form_C": "C",
        "-Form_D": "D",
        "-Form_E": "E",
        "-Form_F": "F",
        "-Form_G": "G",
        "-Form_H": "H",
        "-Form_I": "I",
        "-Form_J": "J",
        "-Form_K": "K",
        "-Form_L": "L",
        "-Form_M": "M",
        "-Form_N": "N",
        "-Form_O": "O",
        "-Form_P": "P",
        "-Form_Qmark": "QU",    # QU before Q because Q form would trigger first and misname file
        "-Form_Q": "Q",
        "-Form_R": "R",
        "-Form_S": "S",
        "-Form_T": "T",
        "-Form_U": "U",
        "-Form_V": "V",
        "-Form_W": "W",
        "-Form_X": "X",
        "-Form_Y": "Y",
        "-Form_Z": "Z",
        "-Form_!": "EX"
    },

    # Sneasel
    # Needs to be included here because its not a universal form (it has its own form id in whole (-Region_Hisui-f))
    # So translator will come into this dict and if a value isn't found, will change it to "FORM_NOT_IN_MAP_SET"
    # Consequently not downloading it
    215: {
        "-Region_Hisui-f": ""
    },

    # Castform Weathers
    351: {
        "-Form_Rainy": "R",
        "-Form_Snowy": "H",
        "-Form_Sunny": "S"
    },

    # Primal Kyogre & Groudon
    382: {"-Form_Primal": "P"},
    383: {"-Form_Primal": "P"},

    # Deoxys
    386: {
        "-Form_Attack": "A",
        "-Form_Defense": "D",
        "-Form_Speed": "S"
    },

    # Burmy & Wormadam Cloaks
    412: {
        "-Form_Plant_Cloak": "",    # Plant Cloak considered default, so does not have a letter denoter
        "-Form_Sandy_Cloak": "G",
        "-Form_Trash_Cloak": "S"
    },
    413: {
        "-Form_Plant_Cloak": "",    # Plant Cloak considered default, so does not have a letter denoter
        "-Form_Sandy_Cloak": "G",
        "-Form_Trash_Cloak": "S"
    },

    # Cherrim
    421: {
        "-Form_Overcast": "",   # Overcast form considered default: so does not have a letter denoter
        "-Form_Sunshine": "S"
    },

    # Shellos & Gastrodon East/West
    422: {
        "-Form_West": "",   # West form considered default: so does not have a letter denoter
        "-Form_East": "E"
    },
    423: {
        "-Form_West": "",   # West form considered default: so does not have a letter denoter
        "-Form_East": "E"
    },

    # Rotom Appliances
    479: {
        "-Form_Fan": "F",
        "-Form_Frost": "R",
        "-Form_Heat": "O",
        "-Form_Mow": "L",
        "-Form_Wash": "W"
    },

    # Dialga & Palkia
    483: {"-Form_Origin": "O"},
    484: {"-Form_Origin": "O"},

    # Giratina
    487: {
        "-Form_Altered": "",    # Altered form considered default: so does not have a letter denoter
        "-Form_Origin": "O"
    },

    # Shaymin
    492: {
        "-Form_Land": "",   # Land form considered default: so does not have a letter denoter
        "-Form_Sky": "S"
    },

    # Arceus Types
    493: BULBA_TYPE_FORM_MAP,

    # Basculin Stripes
    550: {
        "-Form_Red_Striped": "",    # Red Striped form considered default: so does not have a letter denoter
        "-Form_Blue_Striped": "B",
        "-Form_White_Striped": "W"
    },

    # Darmanitan Modes
    555: {
        "-Form_Standard": "",   # Standard form considered default: so does not have a letter denoter
        "-Form_Zen": "Z"
    },

    # Deerling & Sawsbuck Seasons
    585: {
        "-Form_Spring": "", # Spring form considered default: so does not have a letter denoter
        "-Form_Autumn": "A",
        "-Form_Summer": "S",
        "-Form_Winter": "W"
    },
    586: {
        "-Form_Spring": "", # Spring form considered default: so does not have a letter denoter
        "-Form_Autumn": "A",
        "-Form_Summer": "S",
        "-Form_Winter": "W"
    },

    # Forces of nature forms
    641: {
        "-Form_Incarnate": "",  # Incarnate form considered default: so does not have a letter denoter
        "-Form_Therian": "T"
    },
    642: {
        "-Form_Incarnate": "",  # Incarnate form considered default: so does not have a letter denoter
        "-Form_Therian": "T"
    },
    645: {
        "-Form_Incarnate": "",  # Incarnate form considered default: so does not have a letter denoter
        "-Form_Therian": "T"
    },

    # Kyurem
    646: {
        "-Form_Black": "DO_BY_HAND",
        "-Form_Black_Overdrive": "DO_BY_HAND",
        "-Form_White": "DO_BY_HAND",
        "-Form_White_Overdrive": "DO_BY_HAND",
    },
    
    # Keldeo
    647: {
        "-Form_Ordinary": "",   # Ordinary form considered default: so does not have a letter denoter
        "-Form_Resolute": "R"
    },

    # Meloetta
    648: {
        "-Form_Aria": "",
        "-Form_Pirouette": "P"
    },

    # Genesect
    649: {
        "-Form_Douse_Drive": "B",
        "-Form_Burn_Drive": "R",
        "-Form_Chill_Drive": "W",
        "-Form_Shock_Drive": "Y"
    },

    # Ash Greninja
    658: {"-Form_Ash": "A"},

    # Vivillon Patterns
    666: {
        "-Form_Meadow": "",  # Meadow form considered default: so does not have a letter denoter
        "-Form_Archipelago": "Arc",
        "-Form_Continental": "Con",
        "-Form_Elegant": "Ele",
        "-Form_Garden": "Gar",
        "-Form_High_Plains": "Hig",
        "-Form_Icy_Snow": "Icy",
        "-Form_Jungle": "Jun",
        "-Form_Marine": "Mar",
        "-Form_Modern": "Mod",
        "-Form_Monsoon": "Mon",
        "-Form_Ocean": "Oce",
        "-Form_Polar": "Pol",
        "-Form_River": "Riv",
        "-Form_Sandstorm": "San",
        "-Form_Savanna": "Sav",
        "-Form_Sun": "Sun",
        "-Form_Tundra": "Tun",
        "-Form_Poke_Ball": "Pok",
        "-Form_Fancy": "Fan"
    },
    
    # Flabebe: Floette: and Florges colors
    669: {
        "-Form_Red_Flower": "", # Red Flower form considered default: so does not have a letter denoter
        "-Form_Blue_Flower": "B",
        "-Form_Orange_Flower": "O",
        "-Form_White_Flower": "W",
        "-Form_Yellow_Flower": "Y"
    },
    670: {
        "-Form_Red_Flower": "", # Red Flower form considered default: so does not have a letter denoter
        "-Form_Blue_Flower": "B",
        "-Form_Orange_Flower": "O",
        "-Form_White_Flower": "W",
        "-Form_Yellow_Flower": "Y",
        "-Form_Eternal_Flower": "E"
    },
    671: {
        "-Form_Red_Flower": "", # Red Flower form considered default: so does not have a letter denoter
        "-Form_Blue_Flower": "B",
        "-Form_Orange_Flower": "O",
        "-Form_White_Flower": "W",
        "-Form_Yellow_Flower": "Y"
    },

    # Furfrou Trims
    676: {
        "-Form_Dandy_Trim": "Da",
        "-Form_Debutante_Trim": "De",
        "-Form_Diamond_Trim": "Di",
        "-Form_Heart_Trim": "He",
        "-Form_Kabuki_Trim": "Ka",
        "-Form_La_Reine_Trim": "La",
        "-Form_Matron_Trim": "Ma",
        "-Form_Pharaoh_Trim": "Ph",
        "-Form_Star_Trim": "St"
    },

    # Aegislash
    681: {
        "-Form_Shield": "", # Shield form considered default: so does not have a letter denoter
        "-Form_Blade": "B"
    },

    # Pumpkaboo and Gourgeist Sizes
    710: {
        "-Form_Average_Size": "", # Average Size form considered default: so does not have a letter denoter
        "-Form_Small_Size": "Sm",
        "-Form_Large_Size": "La",
        "-Form_Super_Size": "Su"
    },
    711: {
        "-Form_Average_Size": "", # Average Size form considered default: so does not have a letter denoter
        "-Form_Small_Size": "Sm",
        "-Form_Large_Size": "La",
        "-Form_Super_Size": "Su"
    },

    # Xerneas
    716: {
        "-Form_Active": "", # Active form considered default: so does not have a letter denoter
        "-Form_Neutral": "N"
    },

    # Zygarde
    718: {
        "-Form_50%": "",    # 50% form considered default: so does not have a letter denoter
        "-Form_Complete": "C",
        "-Form_10%": "T"
    },

    # Hoopa
    720: {
        "-Form_Confined": "",   # Confined form considered default: so does not have a letter denoter
        "-Form_Unbound": "U"
    },

    # Oricorio
    741: {
        "-Form_Baile": "",   # Baile form considered default: so does not have a letter denoter
        "-Form_Pa'u": "Pa",
        "-Form_Pom_Pom": "Po",
        "-Form_Sensu": "Se"
    },

    # Lycanroc
    745: {
        "-Form_Midday": "", # Midday form considered default: so does not have a letter denoter
        "-Form_Dusk": "D",
        "-Form_Midnight": "Mn"
    },

    # Wishiwashi
    746: {
        "-Form_Solo": "",   # Solo form considered default: so does not have a letter denoter
        "-Form_School": "Sc"
    },

    # Silvally Types
    773: BULBA_TYPE_FORM_MAP,

    # Minior
    774: {
        "-Form_Meteor": "", # Meteor form considered default: so does not have a letter denoter
        "-Form_Blue_Core": "B",
        "-Form_Green_Core": "G",
        "-Form_Indigo_Core": "I",
        "-Form_Orange_Core": "O",
        "-Form_Red_Core": "R",
        "-Form_Violet_Core": "V",
        "-Form_Yellow_Core": "Y",
        "-Form_Core": "R"   # This is the shiny sprite, which bulba has labeled for Red
    },

    # Mimikyu
    778: {
        "-Form_Disguised": "",  # Disguised form considered default: so does not have a letter denoter
        "-Form_Busted": "B"
    },

    # Solgaleo
    791: {"-Form_Radiant_Sun": "R"},

    # Lunala
    792: {"-Form_Full_Moon": "F"},

    # Necrozma
    800: {
        "-Form_Dawn_Wings": "DW",
        "-Form_Dusk_Mane": "DM",
        "-Form_Ultra": "U"
    },

    # Magearna
    801: {"-Form_Original_Color": "O"},
    
    # Cramorant
    845: {
        "-Form_Gorging": "Go",
        "-Form_Gulping": "Gu"
    },
    
    # Toxtricity
    849: {
        "-Form_Amped": "",   # Amped form considered default: so does not have a letter denoter
        "-Form_Low_Key": "L"
    },

    # Sinistea & Polteageist
    854 : {
        "-Form_Phony": "",  # Phony form considered default: so does not have a letter denoter
        "-Form_Antique": "A",
        "-Show_Stamp": "DO_BY_HAND" # Just putting here so it doesn't download default
    },
    855 : {
        "-Form_Phony": "",  # Phony form considered default: so does not have a letter denoter
        "-Form_Antique": "A",
        "-Show_Stamp": "DO_BY_HAND" # Just putting here so it doesn't download default
    },

    # Alcremie Creams & Sweets
    869: {
        "-Form_Caramel_Swirl_Berry_Sweet": "CaSB",
        "-Form_Caramel_Swirl_Clover_Sweet": "CaSC",
        "-Form_Caramel_Swirl_Flower_Sweet": "CaSF",
        "-Form_Caramel_Swirl_Love_Sweet": "CaSL",
        "-Form_Caramel_Swirl_Ribbon_Sweet": "CaSR",
        "-Form_Caramel_Swirl_Star_Sweet": "CaSS",
        "-Form_Caramel_Swirl_Strawberry_Sweet": "CaS",
        "-Form_Lemon_Cream_Berry_Sweet": "LeCB",
        "-Form_Lemon_Cream_Clover_Sweet": "LeCC",
        "-Form_Lemon_Cream_Flower_Sweet": "LeCF",
        "-Form_Lemon_Cream_Love_Sweet": "LeCL",
        "-Form_Lemon_Cream_Ribbon_Sweet": "LeCR",
        "-Form_Lemon_Cream_Star_Sweet": "LeCS",
        "-Form_Lemon_Cream_Strawberry_Sweet": "LeC",
        "-Form_Matcha_Cream_Berry_Sweet": "MaCB",
        "-Form_Matcha_Cream_Clover_Sweet": "MaCC",
        "-Form_Matcha_Cream_Flower_Sweet": "MaCF",
        "-Form_Matcha_Cream_Love_Sweet": "MaCL",
        "-Form_Matcha_Cream_Ribbon_Sweet": "MaCR",
        "-Form_Matcha_Cream_Star_Sweet": "MaCS",
        "-Form_Matcha_Cream_Strawberry_Sweet": "MaC",
        "-Form_Mint_Cream_Berry_Sweet": "MiCB",
        "-Form_Mint_Cream_Clover_Sweet": "MiCC",
        "-Form_Mint_Cream_Flower_Sweet": "MiCF",
        "-Form_Mint_Cream_Love_Sweet": "MiCL",
        "-Form_Mint_Cream_Ribbon_Sweet": "MiCR",
        "-Form_Mint_Cream_Star_Sweet": "MiCS",
        "-Form_Mint_Cream_Strawberry_Sweet": "MiC",
        "-Form_Rainbow_Swirl_Berry_Sweet": "RaSB",
        "-Form_Rainbow_Swirl_Clover_Sweet": "RaSC",
        "-Form_Rainbow_Swirl_Flower_Sweet": "RaSF",
        "-Form_Rainbow_Swirl_Love_Sweet": "RaSL",
        "-Form_Rainbow_Swirl_Ribbon_Sweet": "RaSR",
        "-Form_Rainbow_Swirl_Star_Sweet": "RaSS",
        "-Form_Rainbow_Swirl_Strawberry_Sweet": "RaS",
        "-Form_Ruby_Cream_Berry_Sweet": "RaCB",
        "-Form_Ruby_Cream_Clover_Sweet": "RaCC",
        "-Form_Ruby_Cream_Flower_Sweet": "RaCF",
        "-Form_Ruby_Cream_Love_Sweet": "RaCL",
        "-Form_Ruby_Cream_Ribbon_Sweet": "RaCR",
        "-Form_Ruby_Cream_Star_Sweet": "RaCS",
        "-Form_Ruby_Cream_Strawberry_Sweet": "RaC",
        "-Form_Ruby_Swirl_Berry_Sweet": "RuSB",
        "-Form_Ruby_Swirl_Clover_Sweet": "RuSC",
        "-Form_Ruby_Swirl_Flower_Sweet": "RuSF",
        "-Form_Ruby_Swirl_Love_Sweet": "RuSL",
        "-Form_Ruby_Swirl_Ribbon_Sweet": "RuSR",
        "-Form_Ruby_Swirl_Star_Sweet": "RuSS",
        "-Form_Ruby_Swirl_Strawberry_Sweet": "RuS",
        "-Form_Salted_Cream_Berry_Sweet": "SaCB",
        "-Form_Salted_Cream_Clover_Sweet": "SaCC",
        "-Form_Salted_Cream_Flower_Sweet": "SaCF",
        "-Form_Salted_Cream_Love_Sweet": "SaCL",
        "-Form_Salted_Cream_Ribbon_Sweet": "SaCR",
        "-Form_Salted_Cream_Star_Sweet": "SaCS",
        "-Form_Salted_Cream_Strawberry_Sweet": "SaC",
        # Vanilla Cream considered default Cream, so no letter denoter
        "-Form_Vanilla_Cream_Berry_Sweet": "B",
        "-Form_Vanilla_Cream_Clover_Sweet": "C",
        "-Form_Vanilla_Cream_Flower_Sweet": "F",
        "-Form_Vanilla_Cream_Love_Sweet": "L",
        "-Form_Vanilla_Cream_Ribbon_Sweet": "R",
        "-Form_Vanilla_Cream_Star_Sweet": "S",
        # Strawberry Sweet considered default Sweet, so no letter denoter
        "-Form_Vanilla_Cream_Strawberry_Sweet": "",
        # Shinies (which have only berry differences)
        "-Form_Berry_Sweet": "B",
        "-Form_Clover_Sweet": "C",
        "-Form_Flower_Sweet": "F",
        "-Form_Love_Sweet": "L",
        "-Form_Ribbon_Sweet": "R",
        "-Form_Star_Sweet": "S",
        "-Form_Strawberry_Sweet": "",
    },

    # Eiscue
    875: {
        "-Form_Ice_Face": "",   # Ice Face form considered default: so does not have a letter denoter
        "-Form_Noice_Face": "N"
    },
    
    # Morpeko
    877: {
        "-Form_Full_Belly": "", # Full Belly form considered default: so does not have a letter denoter
        "-Form_Hangry": "H"
    },

    # Zacian
    888: {
        "-Form_Hero_of_Many_Battles": "",   # Hero form considered default: so does not have a letter denoter
        "-Form_Crowned_Sword": "C"
    },

    # Zamazenta
    889: {
        "-Form_Hero_of_Many_Battles": "",   # Hero form considered default: so does not have a letter denoter
        "-Form_Crowned_Shield": "C"
    },

    # Eternatus Eternamax
    890: {"-Form_Eternamax": "E"},

    # Urshifu
    892: {
        "-Form_Single_Strike": "",  # Single strike form considered default: so does not have a letter denoter
        "-Form_Rapid_Strike": "R"
    },

    # Zarude
    893: {"-Form_Dada": "D"},

    # Calyrex Ridings
    898: {
        "-Form_Ice_Rider": "I",
        "-Form_Shadow_Rider": "R"
    },

    # Ursaluna
    901: {"-Form_Bloodmoon": "B",},

    # Enamorus
    905: {
        "-Form_Incarnate": "",  # Incarnate form considered default: so does not have a letter denoter
        "-Form_Therian": "T"
    },

    # Maushold
    925: {
        "-Form_Family_of_Three": "T",
        "-Form_Family_of_Four": ""  # Family of Four considered default: so does not have a letter denoter
    },

    # Squawkabilly
    931: {
        "-Form_Blue_Plumage": "B", 
        "-Form_Green_Plumage": "",  # Green form considered default: so does not have a letter denoter
        "-Form_White_Plumage": "W", 
        "-Form_Yellow_Plumage": "Y"
    },

    # Palafin
    964: {
        "-Form_Zero": "",   # Zero form considered default: so does not have a letter denoter
        "-Form_Hero": "H"
    },

    # Tatsugiri
    978 :{
        "-Form_Curly": "",  # Curly form considered default: so does not have a letter denoter
        "-Form_Droopy": "D", 
        "-Form_Stretchy" : "S"
    },

    # Dudunsparce
    982 : {
        "-Form_Two_Segment": "",    # Two Segment form considered default: so does not have a letter denoter
        "-Form_Three_Segment": "Th"
    },

    # Gimmighoul
    999: {
        "-Form_Chest": "",  # Chest form considered default: so does not have a letter denoter
        "-Form_Roaming": "R"
    },

    # Poltchageist
    1012: {
        "-Form_Artisan": "A", 
        "-Form_Counterfeit": "",     # Counterfeit form considered default: so does not have a letter denoter
        "-Show_Stamp": "DO_BY_HAND" # Just putting here so it doesn't download default
    },

    # Sinistcha
    1013: {
        "-Form_Masterpiece": "M", 
        "-Form_Unremarkable" : "",   # Unremarkable form considered default: so does not have a letter denoter
        "-Show_Stamp": "DO_BY_HAND" # Just putting here so it doesn't download default
    },

    # Ogerpon
    1017: {
        "-Form_Cornerstone_Mask": "C", 
        "-Form_Hearthflame_Mask": "H", 
        "-Form_Teal_Mask": "",      # Teal Mask form considered default: so does not have a letter denoter
        "-Form_Wellspring_Mask": "W"
    },

    # Terapagos
    1024: {
        "-Form_Normal": "",     # Normal form considered default: so does not have a letter denoter
        "-Form_Terastal": "T", 
        "-Form_Stellar": "S"
    }
}


def drawn_dream_translation(form):
    dream_translation = f" {form} Dream"
    return dream_translation


BULBA_DRAWN_DREAM_TYPE_MAP = {k.replace("Form_", ""): drawn_dream_translation(v.replace("-","")) for k,v in BULBA_TYPE_FORM_MAP.items()}

# NOTE: Unlike game sprites, drawn Urshifu has Giganta before forms, so gigantamax can be included here
DRAWN_IMAGES_UNIVERSAL_FORMS_MAP = {
    "-Mega_X": "-Mega X",
    "-Mega_Y": "-Mega Y",
    # The below are unchanged, but I have protection for missing forms, so if I omit them they wont get downloaded
    "-Mega": "-Mega",   # This after X&Y so when looping through Mega wont trigger a form meant to be X or Y
    "-Alola": "-Alola",
    "-Galar": "-Galar",
    "-Hisui": "-Hisui",
    "-Paldea": "-Paldea",
    "-Gigantamax": "-Gigantamax"
}


# NOTE: If a form is omitted below, it means my filename tags are the same as bulbas, as such only file naming differences are listed below
# NOTE: Technically my underscores dont match up with their spaces, but all spaces get converted to underscores when becoming a URL, anyways
# my_filename_format: bulba_filename_format
DRAWN_IMAGES_SPECIES_FORMS_MAP = {
    # Pikachu
    25: {
        "-Cap_Alola": "-Alola Cap",
        "-Cap_Hoenn": "-Hoenn Cap",
        "-Cap_Kalos": "-Kalos Cap",
        "-Cap_Original": "-Original Cap",
        "-Cap_Partner": "-Partner Cap",
        "-Cap_Sinnoh": "-Sinnoh Cap",
        "-Cap_Unova": "-Unova Cap",
        "-Cap_World": "-World Cap",
        "-Cosplay_Belle": "Belle",
        "-Cosplay_Libre": "-Libre",
        "-Cosplay_PhD": "-PhD",
        "-Cosplay_Pop_Star": "-Pop Star",
        "-Cosplay_Rock_Star": "-Rock Star"
    },

    # Tauros
    128: {
        "-Combat": " Combat", 
        "-Blaze": " Blaze", 
        "-Aqua": " Aqua"
    },

    # Pichu Spiky Eared doesn't have any official artwork following naming conventions

    # Unown
    # Hyphens and one-off differences handled in bulba_scraping_utils where needed
    # TODO: Create Dream converter function that will return { {form} Dream}
    201: {
        "-A": drawn_dream_translation("A"),
        "-B": drawn_dream_translation("B"),
        "-C": drawn_dream_translation("C"),
        "-D": drawn_dream_translation("D"),
        "-E": drawn_dream_translation("E"),
        "-F": drawn_dream_translation("F"),
        "-G": drawn_dream_translation("G"),
        "-H": drawn_dream_translation("H"),
        "-I": drawn_dream_translation("I"),
        "-J": drawn_dream_translation("J"),
        "-K": drawn_dream_translation("K"),
        "-L": drawn_dream_translation("L"),
        "-M": drawn_dream_translation("M"),
        "-N": drawn_dream_translation("N"),
        "-O": drawn_dream_translation("O"),
        "-P": drawn_dream_translation("P"),
        "-Qmark": drawn_dream_translation("Question"),    # QU before Q because Q form would trigger first and misname file
        "-Q": drawn_dream_translation("Q"),
        "-R": drawn_dream_translation("R"),
        "-S": drawn_dream_translation("S"),
        "-T": drawn_dream_translation("T"),
        "-U": drawn_dream_translation("U"),
        "-V": drawn_dream_translation("V"),
        "-W": drawn_dream_translation("W"),
        "-X": drawn_dream_translation("X"),
        "-Y": drawn_dream_translation("Y"),
        "-Z": drawn_dream_translation("Z"),
        "-!": drawn_dream_translation("Exclamation")
    },

    # Burmy & Wormadam
    412: {
        "Plant_Cloak": "-Plant",
        "Sandy_Cloak": "-Sandy",
        "Trash_Cloak": "-Trash",
    },
    413: {
        "Plant_Cloak": "-Plant",
        "Sandy_Cloak": "-Sandy",
        "Trash_Cloak": "-Trash",
    },

    # Cherrim
    421: {"-Overcast": ""},    # Overcast form considered default: so does not have a letter denoter

    # Giratina
    487: {"-Altered": ""},  # Altered form considered default: so does not have a letter denoter

    # Shaymin
    492: {"-Land": ""},   # Land form considered default: so does not have a letter denoter

    # Arceus Types
    493: BULBA_DRAWN_DREAM_TYPE_MAP,

    # Basculin Stripes
    550: {
        "-Red_Striped": "-Red",
        "-Blue_Striped": "-Blue",
        "-White_Striped": "-White",
    },

    # TODO: Check
    # Darmanitan Modes
    555: {
        "-Standard": "",
        "-Zen": "-Zen",
        "-Region_Galar-Standard": "-Galar",
        "-Region_Galar-Zen": "-Galar Zen"
    },

    # Deerling & Sawsbuck Seasons
    # Spring form considered default: so does not have a letter denoter
    585: {"-Spring": ""},   
    586: {"-Spring": ""},

    # Forces of nature forms
    # Incarnate form considered default: so does not have a letter denoter
    641: {"-Incarnate": ""},
    642: {"-Incarnate": ""},
    645: {"-Incarnate": ""},

    # Kyurem
    646: {
        "-Black_Overdrive": "-Black2",
        "-White_Overdrive": "-White2",
    },
    
    # Keldeo
    647: {"-Ordinary": ""}, # Ordinary form considered default: so does not have a letter denoter

    # Meloetta
    648: {"-Aria": ""},

    # Genesect
    649: {
        "-Douse_Drive": drawn_dream_translation("Douse"),
        "-Burn_Drive": drawn_dream_translation("Burn"),
        "-Chill_Drive": drawn_dream_translation("Chill"),
        "-Shock_Drive": drawn_dream_translation("Shock")
    },

    # Vivillon Patterns
    666: {"-Poke_Ball": "-Pok\u00e9 Ball"},
    
    # Flabebe: Floette: and Florges colors
    669: {
        "-Red_Flower": " Red Flower XY anime",
        "-Blue_Flower": " Blue Flower XY anime",
        "-Orange_Flower": " Orange Flower XY anime",
        "-White_Flower": " White Flower XY anime",
        "-Yellow_Flower": " Yellow Flower XY anime"
    },
    670: {
        "-Red_Flower": "-Red XY anime",
        "-Blue_Flower": "-Blue XY anime",
        "-Orange_Flower": "-Orange XY anime",
        "-White_Flower": "-White XY anime",
        "-Yellow_Flower": "-Yellow XY anime",
        "-Eternal_Flower": "DO_BY_HAND" # Doesn't Follow Naming Convention
    },
    671: {
        "-Red_Flower": " Red Flower XY anime",
        "-Blue_Flower": " Blue Flower XY anime",
        "-Orange_Flower": " Orange Flower XY anime",
        "-White_Flower": " White Flower XY anime",
        "-Yellow_Flower": " Yellow Flower XY anime"
    },

    # Furfrou Trims
    676: {
        "-Form_Dandy_Trim": drawn_dream_translation("Dandy"),
        "-Form_Debutante_Trim": drawn_dream_translation("Debutante"),
        "-Form_Diamond_Trim": drawn_dream_translation("Diamond"),
        "-Form_Heart_Trim": drawn_dream_translation("Heart"),
        "-Form_Kabuki_Trim": drawn_dream_translation("Kabuki"),
        "-Form_La_Reine_Trim": drawn_dream_translation("La Reine"),
        "-Form_Matron_Trim": drawn_dream_translation("Matron"),
        "-Form_Pharaoh_Trim": drawn_dream_translation("Pharaoh"),
        "-Form_Star_Trim": drawn_dream_translation("Star")
    },

    # Pumpkaboo and Gourgeist
    710: {"-Form_Average_Size": ""},
    711: {"-Form_Average_Size": ""},

    # Xerneas
    716: {"-Form_Active": ""},   # Active form considered default: so does not have a letter denoter

    # Zygarde
    718: {
        "-Form_50%": "",    # 50% form considered default: so does not have a letter denoter
        "-Form_Complete": "-Complete",
        "-Form_10%": "-10Percent"
    },

    # Hoopa
    720: {"-Form_Confined": ""},

    # Oricorio
    741: {
        "-Form_Baile": "",   # Baile form considered default: so does not have a letter denoter
        "-Form_Pom_Pom": "-Pom-Pom"
    },

    # Lycanroc
    745: {"-Form_Midday": ""},

    # Wishiwashi
    746: {"-Form_Solo": ""},

    # Silvally Types
    773: BULBA_DRAWN_DREAM_TYPE_MAP,

    # Minior
    774: {
        "-Form_Meteor": drawn_dream_translation(""), # Meteor form considered default: so does not have a letter denoter
        "-Form_Blue_Core": drawn_dream_translation("Blue"),
        "-Form_Green_Core": drawn_dream_translation("Green"),
        "-Form_Indigo_Core": drawn_dream_translation("Indigo"),
        "-Form_Orange_Core": drawn_dream_translation("Orange"),
        "-Form_Red_Core": drawn_dream_translation("Red"),
        "-Form_Violet_Core": drawn_dream_translation("Violet"),
        "-Form_Yellow_Core": drawn_dream_translation("Yellow"),
    },

    # Mimikyu
    778: {
        "-Form_Disguised": "",  # Disguised form considered default: so does not have a letter denoter
        "-Form_Busted": drawn_dream_translation("Busted")
    },

    # Solgaleo
    791: {"-Form_Radiant_Sun": "-RadiantSunPhase"},

    # Lunala
    792: {"-Form_Full_Moon": "-FullMoonPhase"},

    # Magearna
    801: {"-Form_Original_Color": "-DOESNT_EXIST"},

    # Alcremie Creams & Sweets
    # Non commented is all bulba had, commented so I wouldn't have to write them all again
    869: {
        # "-Form_Caramel_Swirl_Berry_Sweet": "CaSB",
        # "-Form_Caramel_Swirl_Clover_Sweet": "CaSC",
        "-Form_Caramel_Swirl_Flower_Sweet": " Dream - Caramel Swirl",
        # "-Form_Caramel_Swirl_Love_Sweet": "CaSL",
        # "-Form_Caramel_Swirl_Ribbon_Sweet": "CaSR",
        # "-Form_Caramel_Swirl_Star_Sweet": "CaSS",
        # "-Form_Caramel_Swirl_Strawberry_Sweet": "CaS",
        # "-Form_Lemon_Cream_Berry_Sweet": "LeCB",
        # "-Form_Lemon_Cream_Clover_Sweet": "LeCC",
        # "-Form_Lemon_Cream_Flower_Sweet": "LeCF",
        # "-Form_Lemon_Cream_Love_Sweet": "LeCL",
        "-Form_Lemon_Cream_Ribbon_Sweet": " Dream - Lemon Cream",
        # "-Form_Lemon_Cream_Star_Sweet": "LeCS",
        # "-Form_Lemon_Cream_Strawberry_Sweet": "LeC",
        # "-Form_Matcha_Cream_Berry_Sweet": "MaCB",
        # "-Form_Matcha_Cream_Clover_Sweet": "MaCC",
        "-Form_Matcha_Cream_Flower_Sweet": " Dream - Matcha Cream",
        # "-Form_Matcha_Cream_Love_Sweet": "MaCL",
        # "-Form_Matcha_Cream_Ribbon_Sweet": "MaCR",
        # "-Form_Matcha_Cream_Star_Sweet": "MaCS",
        # "-Form_Matcha_Cream_Strawberry_Sweet": "MaC",
        # "-Form_Mint_Cream_Berry_Sweet": "MiCB",
        # "-Form_Mint_Cream_Clover_Sweet": "MiCC",
        # "-Form_Mint_Cream_Flower_Sweet": "MiCF",
        # "-Form_Mint_Cream_Love_Sweet": "MiCL",
        # "-Form_Mint_Cream_Ribbon_Sweet": "MiCR",
        # "-Form_Mint_Cream_Star_Sweet": "MiCS",
        "-Form_Mint_Cream_Strawberry_Sweet": " Dream - Mint Cream",
        # "-Form_Rainbow_Swirl_Berry_Sweet": "RaSB",
        # "-Form_Rainbow_Swirl_Clover_Sweet": "RaSC",
        # "-Form_Rainbow_Swirl_Flower_Sweet": "RaSF",
        # "-Form_Rainbow_Swirl_Love_Sweet": "RaSL",
        # "-Form_Rainbow_Swirl_Ribbon_Sweet": "RaSR",
        # "-Form_Rainbow_Swirl_Star_Sweet": "RaSS",
        "-Form_Rainbow_Swirl_Strawberry_Sweet": " Dream - Rainbow Swirl",
        # "-Form_Ruby_Cream_Berry_Sweet": "RaCB",
        "-Form_Ruby_Cream_Clover_Sweet": " Dream - Ruby Cream",
        # "-Form_Ruby_Cream_Flower_Sweet": "RaCF",
        # "-Form_Ruby_Cream_Love_Sweet": "RaCL",
        # "-Form_Ruby_Cream_Ribbon_Sweet": "RaCR",
        # "-Form_Ruby_Cream_Star_Sweet": "RaCS",
        # "-Form_Ruby_Cream_Strawberry_Sweet": "RaC",
        # "-Form_Ruby_Swirl_Berry_Sweet": "RuSB",
        # "-Form_Ruby_Swirl_Clover_Sweet": "RuSC",
        # "-Form_Ruby_Swirl_Flower_Sweet": "RuSF",
        # "-Form_Ruby_Swirl_Love_Sweet": "RuSL",
        # "-Form_Ruby_Swirl_Ribbon_Sweet": "RuSR",
        "-Form_Ruby_Swirl_Star_Sweet": " Dream - Ruby Swirl",
        # "-Form_Ruby_Swirl_Strawberry_Sweet": "RuS",
        # "-Form_Salted_Cream_Berry_Sweet": "SaCB",
        # "-Form_Salted_Cream_Clover_Sweet": "SaCC",
        # "-Form_Salted_Cream_Flower_Sweet": "SaCF",
        "-Form_Salted_Cream_Love_Sweet": " Dream - Salted Cream",
        # "-Form_Salted_Cream_Ribbon_Sweet": "SaCR",
        # "-Form_Salted_Cream_Star_Sweet": "SaCS",
        # "-Form_Salted_Cream_Strawberry_Sweet": "SaC",
        # Vanilla Cream considered default Cream, so no letter denoter
        "-Form_Vanilla_Cream_Berry_Sweet": " Dream - Vanilla Cream",
        # "-Form_Vanilla_Cream_Clover_Sweet": "C",
        # "-Form_Vanilla_Cream_Flower_Sweet": "F",
        # "-Form_Vanilla_Cream_Love_Sweet": "L",
        # "-Form_Vanilla_Cream_Ribbon_Sweet": "R",
        # "-Form_Vanilla_Cream_Star_Sweet": "S",
        # Strawberry Sweet considered default Sweet, so no letter denoter
        "-Form_Vanilla_Cream_Strawberry_Sweet": "",
        # Shinies (which have only berry differences)
        # "-Form_Berry_Sweet": "B",
        # "-Form_Clover_Sweet": "C",
        # "-Form_Flower_Sweet": "F",
        # "-Form_Love_Sweet": "L",
        # "-Form_Ribbon_Sweet": "R",
        # "-Form_Star_Sweet": "S",
        # "-Form_Strawberry_Sweet": "",
    },

    # Eiscue
    875: {
        "-Form_Ice_Face": "",   # Ice Face form considered default: so does not have a letter denoter
        "-Form_Noice_Face": "-Noice"
    },
    
    # Morpeko
    877: {"-Form_Full_Belly": "Full"},

    # Zacian
    888: {
        "-Form_Hero_of_Many_Battles": "-Hero",
        "-Form_Crowned_Sword": ""
    },

    # Zamazenta
    889: {
        "-Form_Hero_of_Many_Battles": "-Hero",
        "-Form_Crowned_Shield": ""
    },

    # Eternatus Eternamax
    890: {"-Form_Eternamax": "-DNE"},

    # Urshifu
    892: {
        "-Form_Single_Strike": " Single Strike",
        "-Form_Rapid_Strike": " Rapid Strike"
    },

    # Enamorus
    905: {"-Form_Incarnate": ""},

    # Maushold
    925: {
        "-Form_Family_of_Three": drawn_dream_translation(""),
        "-Form_Family_of_Four": " Dream - Four"  # Family of Four considered default: so does not have a letter denoter
    },

    # Squawkabilly
    931: {
        "-Form_Blue_Plumage": drawn_dream_translation("Blue"), 
        "-Form_Green_Plumage": drawn_dream_translation("Green"),
        "-Form_White_Plumage": drawn_dream_translation("White"), 
        "-Form_Yellow_Plumage": drawn_dream_translation("Yellow")
    },

    # Palafin
    964: {"-Form_Zero": ""},

    # Tatsugiri
    978 :{"-Form_Curly": ""},

    # Dudunsparce
    982 : {
        "-Form_Two_Segment": drawn_dream_translation("2"),    # Two Segment form considered default: so does not have a letter denoter
        "-Form_Three_Segment": drawn_dream_translation("3")
    },

    # Gimmighoul
    999: {"-Form_Chest": ""},

    # Ogerpon
    1017: {"-Form_Teal_Mask": ""},

    # Terapagos
    # Stellar has dream form, but it has a background...
    1024: {"-Form_Normal": ""},
}


# Used for HOME menu imgs where drawn forms have a dream translation or fringe case, and the HOME menu image needs a different tag
# Otherwise, HOME menu imgs use drawn translations
HOME_MENU_IMGS_SPECIES_FORMS_MAP = {
    # Pikachu
    25: {
        "-Cap_Alola": "-Alola",
        "-Cap_Hoenn": "-Hoenn",
        "-Cap_Kalos": "-Kalos",
        "-Cap_Original": "-Original",
        "-Cap_Partner": "-Partner",
        "-Cap_Sinnoh": "-Sinnoh",
        "-Cap_Unova": "-Unova",
        "-Cap_World": "-World"
    },

    # Unown
    201: {
        "-Form_A": "",
        "-Form_B": "-B",
        "-Form_C": "-C",
        "-Form_D": "-D",
        "-Form_E": "-E",
        "-Form_F": "-F",
        "-Form_G": "-G",
        "-Form_H": "-H",
        "-Form_I": "-I",
        "-Form_J": "-J",
        "-Form_K": "-K",
        "-Form_L": "-L",
        "-Form_M": "-M",
        "-Form_N": "-N",
        "-Form_O": "-O",
        "-Form_P": "-P",
        "-Form_Qmark": "-Question",    # QU before Q because Q form would trigger first and misname file
        "-Form_Q": "-Q",
        "-Form_R": "-R",
        "-Form_S": "-S",
        "-Form_T": "-T",
        "-Form_U": "-U",
        "-Form_V": "-V",
        "-Form_W": "-W",
        "-Form_X": "-X",
        "-Form_Y": "-Y",
        "-Form_Z": "-Z",
        "-Form_!": "-Exclamation"
    },

    # Shellos & Gastrodon
    422: {
        "-Form_East": "-East",
        "-Form_West": ""
    },
    423: {
        "-Form_East": "-East",
        "-Form_West": ""
    },

    # Arceus
    493: BULBA_TYPE_FORM_MAP,

    # Basculin
    550: {
        "-Form_Blue_Striped": "-Blue",
        "-Form_Red_Striped": "",
        "-Form_White_Striped": "-White",
    },

    # Darmanitan
    555: {
        "-Form_Standard": "",
        "-Region_Galar-Form_Standard": "-Galar",
        "-Form_Zen": "-Zen",
        "-Region_Galar-Form_Zen": "-Zen Galar",
    },

    # Genesect
    649: {
        "-Form_Burn_Drive": "-Burn",
        "-Form_Chill_Drive": "-Chill",
        "-Form_Douse_Drive": "-Douse",
        "-Form_Shock_Drive": "-Shock"
    },

    # Flabebe, Floette, and Florges
    669: {
        "-Form_Blue_Flower": "-Blue",
        "-Form_Orange_Flower": "-Orange",
        "-Form_Red_Flower": "",
        "-Form_White_Flower": "-White",
        "-Form_Yellow_Flower": "-Yellow"
    },
    670: {
        "-Form_Eternal_Flower": "-Eternal",
        "-Form_Blue_Flower": "-Blue",
        "-Form_Orange_Flower": "-Orange",
        "-Form_Red_Flower": "",
        "-Form_White_Flower": "-White",
        "-Form_Yellow_Flower": "-Yellow"
    },
    669: {
        "-Form_Blue_Flower": "-Blue",
        "-Form_Orange_Flower": "-Orange",
        "-Form_Red_Flower": "",
        "-Form_White_Flower": "-White",
        "-Form_Yellow_Flower": "-Yellow"
    },

    # Furfrou
    # 676: {

    # }
}

# Used for HOME menu imgs where drawn forms have a dream translation or fringe case, and the HOME menu image needs a different tag
# Otherwise, HOME menu imgs use drawn translations
HOME_MENU_POKE_EXCLSUIONS_FROM_DRAWN_TRANSLATIONS = set(HOME_MENU_IMGS_SPECIES_FORMS_MAP.keys())


# TODO: Add any important comments from existing individual dicts
# TODO: Finish adding Menu forms & Finish commenting names (left off at same place)
# TODO: Alter implementation in bulba_scraping_utils
BULBA_TRANSLATION_MAP = {
    # Pikachu
    25: {
        "Game": {
            "-Form_Cap_Alola": "A",
            "-Form_Cap_Hoenn": "H",
            "-Form_Cap_Kalos": "K",
            "-Form_Cap_Original": "O",
            "-Form_Cap_Sinnoh": "S",
            "-Form_Cap_Unova": "U",
            "-Form_Cap_Partner": "P",
            "-Form_Cap_World": "W",
            "-Form_Cosplay_Belle": "B",
            "-Form_Cosplay_Libre": "L",
            "-Form_Cosplay_PhD": "PhD",
            "-Form_Cosplay_Pop_Star": "Pop",
            "-Form_Cosplay_Rock_Star": "Ro"
        },
        "Drawn": {
            "-Cap_Alola": "-Alola Cap",
            "-Cap_Hoenn": "-Hoenn Cap",
            "-Cap_Kalos": "-Kalos Cap",
            "-Cap_Original": "-Original Cap",
            "-Cap_Partner": "-Partner Cap",
            "-Cap_Sinnoh": "-Sinnoh Cap",
            "-Cap_Unova": "-Unova Cap",
            "-Cap_World": "-World Cap",
            "-Cosplay_Belle": "Belle",
            "-Cosplay_Libre": "-Libre",
            "-Cosplay_PhD": "-PhD",
            "-Cosplay_Pop_Star": "-Pop Star",
            "-Cosplay_Rock_Star": "-Rock Star"
        },
        "Menu": {
            "-Cap_Alola": "-Alola",
            "-Cap_Hoenn": "-Hoenn",
            "-Cap_Kalos": "-Kalos",
            "-Cap_Original": "-Original",
            "-Cap_Partner": "-Partner",
            "-Cap_Sinnoh": "-Sinnoh",
            "-Cap_Unova": "-Unova",
            "-Cap_World": "-World"
        }
    },

    # Tauros
    128: {
        "Game": {
            "-Form_Combat": "C",
            "-Form_Blaze": "B",
            "-Form_Aqua": "A"
        },
        "Drawn": {
            "-Combat": " Combat",
            "-Blaze": " Blaze",
            "-Aqua": " Aqua"
        }
    },

    # Pichu
    172: {"Game": {"-Form_Spiky_Eared": "N"}},

    # Unown
    201: {
        "Game": {
            "-Form_A": "",
            "-Form_B": "B",
            "-Form_C": "C",
            "-Form_D": "D",
            "-Form_E": "E",
            "-Form_F": "F",
            "-Form_G": "G",
            "-Form_H": "H",
            "-Form_I": "I",
            "-Form_J": "J",
            "-Form_K": "K",
            "-Form_L": "L",
            "-Form_M": "M",
            "-Form_N": "N",
            "-Form_O": "O",
            "-Form_P": "P",
            "-Form_Qmark": "QU",
            "-Form_Q": "Q",
            "-Form_R": "R",
            "-Form_S": "S",
            "-Form_T": "T",
            "-Form_U": "U",
            "-Form_V": "V",
            "-Form_W": "W",
            "-Form_X": "X",
            "-Form_Y": "Y",
            "-Form_Z": "Z",
            "-Form_!": "EX"
        },
        "Drawn": {
            "-Form_A": drawn_dream_translation("A"),
            "-Form_B": drawn_dream_translation("B"),
            "-Form_C": drawn_dream_translation("C"),
            "-Form_D": drawn_dream_translation("D"),
            "-Form_E": drawn_dream_translation("E"),
            "-Form_F": drawn_dream_translation("F"),
            "-Form_G": drawn_dream_translation("G"),
            "-Form_H": drawn_dream_translation("H"),
            "-Form_I": drawn_dream_translation("I"),
            "-Form_J": drawn_dream_translation("J"),
            "-Form_K": drawn_dream_translation("K"),
            "-Form_L": drawn_dream_translation("L"),
            "-Form_M": drawn_dream_translation("M"),
            "-Form_N": drawn_dream_translation("N"),
            "-Form_O": drawn_dream_translation("O"),
            "-Form_P": drawn_dream_translation("P"),
            "-Form_Qmark": drawn_dream_translation("Question"),    # QU before Q because Q form would trigger first and misname file
            "-Form_Q": drawn_dream_translation("Q"),
            "-Form_R": drawn_dream_translation("R"),
            "-Form_S": drawn_dream_translation("S"),
            "-Form_T": drawn_dream_translation("T"),
            "-Form_U": drawn_dream_translation("U"),
            "-Form_V": drawn_dream_translation("V"),
            "-Form_W": drawn_dream_translation("W"),
            "-Form_X": drawn_dream_translation("X"),
            "-Form_Y": drawn_dream_translation("Y"),
            "-Form_Z": drawn_dream_translation("Z"),
            "-Form_!": drawn_dream_translation("Exclamation")
        },
        "Menu": {
            "-Form_A": "",
            "-Form_B": "-B",
            "-Form_C": "-C",
            "-Form_D": "-D",
            "-Form_E": "-E",
            "-Form_F": "-F",
            "-Form_G": "-G",
            "-Form_H": "-H",
            "-Form_I": "-I",
            "-Form_J": "-J",
            "-Form_K": "-K",
            "-Form_L": "-L",
            "-Form_M": "-M",
            "-Form_N": "-N",
            "-Form_O": "-O",
            "-Form_P": "-P",
            "-Form_Qmark": "-Question",
            "-Form_Q": "-Q",
            "-Form_R": "-R",
            "-Form_S": "-S",
            "-Form_T": "-T",
            "-Form_U": "-U",
            "-Form_V": "-V",
            "-Form_W": "-W",
            "-Form_X": "-X",
            "-Form_Y": "-Y",
            "-Form_Z": "-Z",
            "-Form_!": "-Exclamation"
        }
    },

    # Sneasel
    215: {"Game": {"-Region_Hisui-f": ""}},

    # Castform
    351: {
        "Game": {
            "-Form_Rainy": "R",
            "-Form_Snowy": "H",
            "-Form_Sunny": "S"
        }
    },

    # Kyogre & Groudon
    382: {"Game": {"-Form_Primal": "P"}},
    383: {"Game": {"-Form_Primal": "P"}},

    #Deoxys
    386: {
        "Game": {
            "-Form_Attack": "A",
            "-Form_Defense": "D",
            "-Form_Speed": "S"
        }
    },

    # Burmy & Wormadam
    412: {
        "Game": {
            "-Form_Plant_Cloak": "",
            "-Form_Sandy_Cloak": "G",
            "-Form_Trash_Cloak": "S"
        },
        "Drawn": {
            "Plant_Cloak": "-Plant",
            "Sandy_Cloak": "-Sandy",
            "Trash_Cloak": "-Trash"
        }
    },
    413: {
        "Game": {
            "-Form_Plant_Cloak": "",
            "-Form_Sandy_Cloak": "G",
            "-Form_Trash_Cloak": "S"
        },
        "Drawn": {
            "Plant_Cloak": "-Plant",
            "Sandy_Cloak": "-Sandy",
            "Trash_Cloak": "-Trash"
        }
    },

    #Cherrim
    421: {
        "Game": {
            "-Form_Overcast": "",
            "-Form_Sunshine": "S"
        },
        "Drawn": {
            "-Overcast": ""
        }
    },
    
    # Shellos & Gastrodon
    422: {
        "Game": {
            "-Form_West": "",
            "-Form_East": "E"
        },
        "Menu": {
            "-Form_East": "-East",
            "-Form_West": ""
        }
    },
    423: {
        "Game": {
            "-Form_West": "",
            "-Form_East": "E"
        },
        "Menu": {
            "-Form_East": "-East",
            "-Form_West": ""
        }
    },
    
    # Rotom
    479: {
        "Game": {
            "-Form_Fan": "F",
            "-Form_Frost": "R",
            "-Form_Heat": "O",
            "-Form_Mow": "L",
            "-Form_Wash": "W"
        }
    },
    
    # Dialga & Palkia
    483: {"Game": {"-Form_Origin": "O"}},
    484: {"Game": {"-Form_Origin": "O"}},
    
    # Giratina
    487: {
        "Game": {
            "-Form_Altered": "",
            "-Form_Origin": "O"
        },
        "Drawn": {
            "-Altered": ""
        }
    },
    
    # Shaymin
    492: {
        "Game": {
            "-Form_Land": "",
            "-Form_Sky": "S"
        },
        "Drawn": {
            "-Land": "" 
        }
    },

    # Arceus
    493: {
        "Game": BULBA_TYPE_FORM_MAP,
        "Drawn": BULBA_DRAWN_DREAM_TYPE_MAP,
        "Menu": BULBA_TYPE_FORM_MAP
    },

    # Basculin
    550: {
        "Game": {
            "-Form_Red_Striped": "",
            "-Form_Blue_Striped": "B",
            "-Form_White_Striped": "W"
        },
        "Drawn": {
            "-Red_Striped": "-Red",
            "-Blue_Striped": "-Blue",
            "-White_Striped": "-White"
        },
        "Menu": {
            "-Form_Blue_Striped": "-Blue",
            "-Form_Red_Striped": "",
            "-Form_White_Striped": "-White"
        }
    },

    # Darmanitan
    555: {
        "Game": {
            "-Form_Standard": "",
            "-Form_Zen": "Z"
        },
        "Drawn": {
            "-Standard": "",
            "-Zen": "-Zen",
            "-Region_Galar-Standard": "-Galar",
            "-Region_Galar-Zen": "-Galar Zen"
        },
        "Menu": {
            "-Form_Standard": "",
            "-Region_Galar-Form_Standard": "-Galar",
            "-Form_Zen": "-Zen",
            "-Region_Galar-Form_Zen": "-Zen Galar"
        }
    },

    # Deerling & Sawsbuck
    585: {
        "Game": {
            "-Form_Spring": "",
            "-Form_Autumn": "A",
            "-Form_Summer": "S",
            "-Form_Winter": "W"
        },
        "Drawn": {
            "-Spring": ""
        }
    },
    586: {
        "Game": {
            "-Form_Spring": "",
            "-Form_Autumn": "A",
            "-Form_Summer": "S",
            "-Form_Winter": "W"
        },
        "Drawn": {
            "-Spring": ""
        }
    },

    # Forces of Nature
    641: {
        "Game": {
            "-Form_Incarnate": "",
            "-Form_Therian": "T"
        },
        "Drawn": {
            "-Incarnate": ""
        }
    },
    642: {
        "Game": {
            "-Form_Incarnate": "",
            "-Form_Therian": "T"
        },
        "Drawn": {
            "-Incarnate": ""
        }
    },
    645: {
        "Game": {
            "-Form_Incarnate": "",
            "-Form_Therian": "T"
        },
        "Drawn": {
            "-Incarnate": ""
        }
    },

    # Kyurem
    646: {
        "Game": {
            "-Form_Black": "DO_BY_HAND",
            "-Form_Black_Overdrive": "DO_BY_HAND",
            "-Form_White": "DO_BY_HAND",
            "-Form_White_Overdrive": "DO_BY_HAND"
        },
        "Drawn": {
            "-Black_Overdrive": "-Black2",
            "-White_Overdrive": "-White2"
        }
    },

    # Keldeo
    647: {
        "Game": {
            "-Form_Ordinary": "",
            "-Form_Resolute": "R"
        },
        "Drawn": {
            "-Ordinary": ""
        }
    },

    # Meloetta
    648: {
        "Game": {
            "-Form_Aria": "",
            "-Form_Pirouette": "P"
        },
        "Drawn": {
            "-Aria": ""
        }
    },

    # Genesect
    649: {
        "Game": {
            "-Form_Douse_Drive": "B",
            "-Form_Burn_Drive": "R",
            "-Form_Chill_Drive": "W",
            "-Form_Shock_Drive": "Y"
        },
        "Drawn": {
            "-Douse_Drive": " Douse Dream",
            "-Burn_Drive": " Burn Dream",
            "-Chill_Drive": " Chill Dream",
            "-Shock_Drive": " Shock Dream"
        },
        "Menu": {
            "-Form_Burn_Drive": drawn_dream_translation("Burn"),
            "-Form_Chill_Drive": drawn_dream_translation("Chill"),
            "-Form_Douse_Drive": drawn_dream_translation("Douse"),
            "-Form_Shock_Drive": drawn_dream_translation("Shock")
        }
    },

    # Greninja
    658: {
        "Game": {
            "-Form_Ash": "A"
        }
    },

    # Vivillon
    666: {
        "Game": {
            "-Form_Meadow": "",
            "-Form_Archipelago": "Arc",
            "-Form_Continental": "Con",
            "-Form_Elegant": "Ele",
            "-Form_Garden": "Gar",
            "-Form_High_Plains": "Hig",
            "-Form_Icy_Snow": "Icy",
            "-Form_Jungle": "Jun",
            "-Form_Marine": "Mar",
            "-Form_Modern": "Mod",
            "-Form_Monsoon": "Mon",
            "-Form_Ocean": "Oce",
            "-Form_Polar": "Pol",
            "-Form_River": "Riv",
            "-Form_Sandstorm": "San",
            "-Form_Savanna": "Sav",
            "-Form_Sun": "Sun",
            "-Form_Tundra": "Tun",
            "-Form_Poke_Ball": "Pok",
            "-Form_Fancy": "Fan"
        },
        "Drawn": {
            "-Poke_Ball": "-Pok\u00e9 Ball"
        }
    },

    # Flabebe, Floette, and Florges
    669: {
        "Game": {
            "-Form_Red_Flower": "",
            "-Form_Blue_Flower": "B",
            "-Form_Orange_Flower": "O",
            "-Form_White_Flower": "W",
            "-Form_Yellow_Flower": "Y"
        },
        "Drawn": {
            "-Red_Flower": " Red Flower XY anime",
            "-Blue_Flower": " Blue Flower XY anime",
            "-Orange_Flower": " Orange Flower XY anime",
            "-White_Flower": " White Flower XY anime",
            "-Yellow_Flower": " Yellow Flower XY anime"
        },
        "Menu": {
            "-Form_Blue_Flower": "-Blue",
            "-Form_Orange_Flower": "-Orange",
            "-Form_Red_Flower": "",
            "-Form_White_Flower": "-White",
            "-Form_Yellow_Flower": "-Yellow"
        }
    },
    670: {
        "Game": {
            "-Form_Red_Flower": "",
            "-Form_Blue_Flower": "B",
            "-Form_Orange_Flower": "O",
            "-Form_White_Flower": "W",
            "-Form_Yellow_Flower": "Y",
            "-Form_Eternal_Flower": "E"
        },
        "Drawn": {
            "-Red_Flower": "-Red XY anime",
            "-Blue_Flower": "-Blue XY anime",
            "-Orange_Flower": "-Orange XY anime",
            "-White_Flower": "-White XY anime",
            "-Yellow_Flower": "-Yellow XY anime",
            "-Eternal_Flower": "DO_BY_HAND"
        },
        "Menu": {
            "-Form_Eternal_Flower": "-Eternal",
            "-Form_Blue_Flower": "-Blue",
            "-Form_Orange_Flower": "-Orange",
            "-Form_Red_Flower": "",
            "-Form_White_Flower": "-White",
            "-Form_Yellow_Flower": "-Yellow"
        }
    },
    671: {
        "Game": {
            "-Form_Red_Flower": "",
            "-Form_Blue_Flower": "B",
            "-Form_Orange_Flower": "O",
            "-Form_White_Flower": "W",
            "-Form_Yellow_Flower": "Y"
        },
        "Drawn": {
            "-Red_Flower": " Red Flower XY anime",
            "-Blue_Flower": " Blue Flower XY anime",
            "-Orange_Flower": " Orange Flower XY anime",
            "-White_Flower": " White Flower XY anime",
            "-Yellow_Flower": " Yellow Flower XY anime"
        }
    },

    # Furfrou
    676: {
        "Game": {
            "-Form_Dandy_Trim": "Da",
            "-Form_Debutante_Trim": "De",
            "-Form_Diamond_Trim": "Di",
            "-Form_Heart_Trim": "He",
            "-Form_Kabuki_Trim": "Ka",
            "-Form_La_Reine_Trim": "La",
            "-Form_Matron_Trim": "Ma",
            "-Form_Pharaoh_Trim": "Ph",
            "-Form_Star_Trim": "St"
        },
        "Drawn": {
            "-Form_Dandy_Trim": drawn_dream_translation("Dandy"),
            "-Form_Debutante_Trim": drawn_dream_translation("Debutante"),
            "-Form_Diamond_Trim": drawn_dream_translation("Diamond"),
            "-Form_Heart_Trim": drawn_dream_translation("Heart"),
            "-Form_Kabuki_Trim": drawn_dream_translation("Kabuki"),
            "-Form_La_Reine_Trim": drawn_dream_translation("La Reine"),
            "-Form_Matron_Trim": drawn_dream_translation("Matron"),
            "-Form_Pharaoh_Trim": drawn_dream_translation("Pharaoh"),
            "-Form_Star_Trim": drawn_dream_translation("Star")
        }
    },
    681: {
        "Game": {
            "-Form_Shield": "",
            "-Form_Blade": "B"
        }
    },
    710: {
        "Game": {
            "-Form_Average_Size": "",
            "-Form_Small_Size": "Sm",
            "-Form_Large_Size": "La",
            "-Form_Super_Size": "Su"
        },
        "Drawn": {
            "-Form_Average_Size": ""
        }
    },
    711: {
        "Game": {
            "-Form_Average_Size": "",
            "-Form_Small_Size": "Sm",
            "-Form_Large_Size": "La",
            "-Form_Super_Size": "Su"
        },
        "Drawn": {
            "-Form_Average_Size": ""
        }
    },
    716: {
        "Game": {
            "-Form_Active": "",
            "-Form_Neutral": "N"
        },
        "Drawn": {
            "-Form_Active": ""
        }
    },
    718: {
        "Game": {
            "-Form_50%": "",
            "-Form_Complete": "C",
            "-Form_10%": "T"
        },
        "Drawn": {
            "-Form_50%": "",
            "-Form_Complete": "-Complete",
            "-Form_10%": "-10Percent"
        }
    },
    720: {
        "Game": {
            "-Form_Confined": "",
            "-Form_Unbound": "U"
        },
        "Drawn": {
            "-Form_Confined": ""
        }
    },
    741: {
        "Game": {
            "-Form_Baile": "",
            "-Form_Pa'u": "Pa",
            "-Form_Pom_Pom": "Po",
            "-Form_Sensu": "Se"
        },
        "Drawn": {
            "-Form_Baile": "",
            "-Form_Pom_Pom": "-Pom-Pom"
        }
    },
    745: {
        "Game": {
            "-Form_Midday": "",
            "-Form_Dusk": "D",
            "-Form_Midnight": "Mn"
        },
        "Drawn": {
            "-Form_Midday": ""
        }
    },
    746: {
        "Game": {
            "-Form_Solo": "",
            "-Form_School": "Sc"
        },
        "Drawn": {
            "-Form_Solo": ""
        }
    },
    773: {
        "Game": BULBA_TYPE_FORM_MAP,
        "Drawn": BULBA_DRAWN_DREAM_TYPE_MAP
    },
    774: {
        "Game": {
            "-Form_Meteor": "",
            "-Form_Blue_Core": "B",
            "-Form_Green_Core": "G",
            "-Form_Indigo_Core": "I",
            "-Form_Orange_Core": "O",
            "-Form_Red_Core": "R",
            "-Form_Violet_Core": "V",
            "-Form_Yellow_Core": "Y",
            "-Form_Core": "R"
        },
        "Drawn": {
            "-Form_Meteor": drawn_dream_translation(""), # Meteor form considered default: so does not have a letter denoter
            "-Form_Blue_Core": drawn_dream_translation("Blue"),
            "-Form_Green_Core": drawn_dream_translation("Green"),
            "-Form_Indigo_Core": drawn_dream_translation("Indigo"),
            "-Form_Orange_Core": drawn_dream_translation("Orange"),
            "-Form_Red_Core": drawn_dream_translation("Red"),
            "-Form_Violet_Core": drawn_dream_translation("Violet"),
            "-Form_Yellow_Core": drawn_dream_translation("Yellow")
        }
    },
    778: {
        "Game": {
            "-Form_Disguised": "",
            "-Form_Busted": "B"
        },
        "Drawn": {
            "-Form_Disguised": "",
            "-Form_Busted": drawn_dream_translation("Busted")
        }
    },
    791: {
        "Game": {
            "-Form_Radiant_Sun": "R"
        },
        "Drawn": {
            "-Form_Radiant_Sun": "-RadiantSunPhase"
        }
    },
    792: {
        "Game": {
            "-Form_Full_Moon": "F"
        },
        "Drawn": {
            "-Form_Full_Moon": "-FullMoonPhase"
        }
    },
    800: {
        "Game": {
            "-Form_Dawn_Wings": "DW",
            "-Form_Dusk_Mane": "DM",
            "-Form_Ultra": "U"
        }
    },
    801: {
        "Game": {
            "-Form_Original_Color": "O"
        },
        "Drawn": {
            "-Form_Original_Color": "-DOESNT_EXIST"
        }
    },
    845: {
        "Game": {
            "-Form_Gorging": "Go",
            "-Form_Gulping": "Gu"
        }
    },
    849: {
        "Game": {
            "-Form_Amped": "",
            "-Form_Low_Key": "L"
        }
    },
    854: {
        "Game": {
            "-Form_Phony": "",
            "-Form_Antique": "A",
            "-Show_Stamp": "DO_BY_HAND"
        }
    },
    855: {
        "Game": {
            "-Form_Phony": "",
            "-Form_Antique": "A",
            "-Show_Stamp": "DO_BY_HAND"
        }
    },
    869: {
        "Game": {
            "-Form_Caramel_Swirl_Berry_Sweet": "CaSB",
            "-Form_Caramel_Swirl_Clover_Sweet": "CaSC",
            "-Form_Caramel_Swirl_Flower_Sweet": "CaSF",
            "-Form_Caramel_Swirl_Love_Sweet": "CaSL",
            "-Form_Caramel_Swirl_Ribbon_Sweet": "CaSR",
            "-Form_Caramel_Swirl_Star_Sweet": "CaSS",
            "-Form_Caramel_Swirl_Strawberry_Sweet": "CaS",
            "-Form_Lemon_Cream_Berry_Sweet": "LeCB",
            "-Form_Lemon_Cream_Clover_Sweet": "LeCC",
            "-Form_Lemon_Cream_Flower_Sweet": "LeCF",
            "-Form_Lemon_Cream_Love_Sweet": "LeCL",
            "-Form_Lemon_Cream_Ribbon_Sweet": "LeCR",
            "-Form_Lemon_Cream_Star_Sweet": "LeCS",
            "-Form_Lemon_Cream_Strawberry_Sweet": "LeC",
            "-Form_Matcha_Cream_Berry_Sweet": "MaCB",
            "-Form_Matcha_Cream_Clover_Sweet": "MaCC",
            "-Form_Matcha_Cream_Flower_Sweet": "MaCF",
            "-Form_Matcha_Cream_Love_Sweet": "MaCL",
            "-Form_Matcha_Cream_Ribbon_Sweet": "MaCR",
            "-Form_Matcha_Cream_Star_Sweet": "MaCS",
            "-Form_Matcha_Cream_Strawberry_Sweet": "MaC",
            "-Form_Mint_Cream_Berry_Sweet": "MiCB",
            "-Form_Mint_Cream_Clover_Sweet": "MiCC",
            "-Form_Mint_Cream_Flower_Sweet": "MiCF",
            "-Form_Mint_Cream_Love_Sweet": "MiCL",
            "-Form_Mint_Cream_Ribbon_Sweet": "MiCR",
            "-Form_Mint_Cream_Star_Sweet": "MiCS",
            "-Form_Mint_Cream_Strawberry_Sweet": "MiC",
            "-Form_Rainbow_Swirl_Berry_Sweet": "RaSB",
            "-Form_Rainbow_Swirl_Clover_Sweet": "RaSC",
            "-Form_Rainbow_Swirl_Flower_Sweet": "RaSF",
            "-Form_Rainbow_Swirl_Love_Sweet": "RaSL",
            "-Form_Rainbow_Swirl_Ribbon_Sweet": "RaSR",
            "-Form_Rainbow_Swirl_Star_Sweet": "RaSS",
            "-Form_Rainbow_Swirl_Strawberry_Sweet": "RaS",
            "-Form_Ruby_Cream_Berry_Sweet": "RaCB",
            "-Form_Ruby_Cream_Clover_Sweet": "RaCC",
            "-Form_Ruby_Cream_Flower_Sweet": "RaCF",
            "-Form_Ruby_Cream_Love_Sweet": "RaCL",
            "-Form_Ruby_Cream_Ribbon_Sweet": "RaCR",
            "-Form_Ruby_Cream_Star_Sweet": "RaCS",
            "-Form_Ruby_Cream_Strawberry_Sweet": "RaC",
            "-Form_Ruby_Swirl_Berry_Sweet": "RuSB",
            "-Form_Ruby_Swirl_Clover_Sweet": "RuSC",
            "-Form_Ruby_Swirl_Flower_Sweet": "RuSF",
            "-Form_Ruby_Swirl_Love_Sweet": "RuSL",
            "-Form_Ruby_Swirl_Ribbon_Sweet": "RuSR",
            "-Form_Ruby_Swirl_Star_Sweet": "RuSS",
            "-Form_Ruby_Swirl_Strawberry_Sweet": "RuS",
            "-Form_Salted_Cream_Berry_Sweet": "SaCB",
            "-Form_Salted_Cream_Clover_Sweet": "SaCC",
            "-Form_Salted_Cream_Flower_Sweet": "SaCF",
            "-Form_Salted_Cream_Love_Sweet": "SaCL",
            "-Form_Salted_Cream_Ribbon_Sweet": "SaCR",
            "-Form_Salted_Cream_Star_Sweet": "SaCS",
            "-Form_Salted_Cream_Strawberry_Sweet": "SaC",
            "-Form_Vanilla_Cream_Berry_Sweet": "B",
            "-Form_Vanilla_Cream_Clover_Sweet": "C",
            "-Form_Vanilla_Cream_Flower_Sweet": "F",
            "-Form_Vanilla_Cream_Love_Sweet": "L",
            "-Form_Vanilla_Cream_Ribbon_Sweet": "R",
            "-Form_Vanilla_Cream_Star_Sweet": "S",
            "-Form_Vanilla_Cream_Strawberry_Sweet": "",
            "-Form_Berry_Sweet": "B",
            "-Form_Clover_Sweet": "C",
            "-Form_Flower_Sweet": "F",
            "-Form_Love_Sweet": "L",
            "-Form_Ribbon_Sweet": "R",
            "-Form_Star_Sweet": "S",
            "-Form_Strawberry_Sweet": ""
        },
        "Drawn": {
            "-Form_Caramel_Swirl_Flower_Sweet": " Dream - Caramel Swirl",
            "-Form_Lemon_Cream_Ribbon_Sweet": " Dream - Lemon Cream",
            "-Form_Matcha_Cream_Flower_Sweet": " Dream - Matcha Cream",
            "-Form_Mint_Cream_Strawberry_Sweet": " Dream - Mint Cream",
            "-Form_Rainbow_Swirl_Strawberry_Sweet": " Dream - Rainbow Swirl",
            "-Form_Ruby_Cream_Clover_Sweet": " Dream - Ruby Cream",
            "-Form_Ruby_Swirl_Star_Sweet": " Dream - Ruby Swirl",
            "-Form_Salted_Cream_Love_Sweet": " Dream - Salted Cream",
            "-Form_Vanilla_Cream_Berry_Sweet": " Dream - Vanilla Cream",
            "-Form_Vanilla_Cream_Strawberry_Sweet": ""
        }
    },
    875: {
        "Game": {
            "-Form_Ice_Face": "",
            "-Form_Noice_Face": "N"
        },
        "Drawn": {
            "-Form_Ice_Face": "",
            "-Form_Noice_Face": "-Noice"
        }
    },
    877: {
        "Game": {
            "-Form_Full_Belly": "",
            "-Form_Hangry": "H"
        },
        "Drawn": {
            "-Form_Full_Belly": "Full"
        }
    },
    888: {
        "Game": {
            "-Form_Hero_of_Many_Battles": "",
            "-Form_Crowned_Sword": "C"
        },
        "Drawn": {
            "-Form_Hero_of_Many_Battles": "-Hero",
            "-Form_Crowned_Sword": ""
        }
    },
    889: {
        "Game": {
            "-Form_Hero_of_Many_Battles": "",
            "-Form_Crowned_Shield": "C"
        },
        "Drawn": {
            "-Form_Hero_of_Many_Battles": "-Hero",
            "-Form_Crowned_Shield": ""
        }
    },
    890: {
        "Game": {
            "-Form_Eternamax": "E"
        },
        "Drawn": {
            "-Form_Eternamax": "-DNE"
        }
    },
    892: {
        "Game": {
            "-Form_Single_Strike": "",
            "-Form_Rapid_Strike": "R"
        },
        "Drawn": {
            "-Form_Single_Strike": " Single Strike",
            "-Form_Rapid_Strike": " Rapid Strike"
        }
    },
    893: {
        "Game": {
            "-Form_Dada": "D"
        }
    },
    898: {
        "Game": {
            "-Form_Ice_Rider": "I",
            "-Form_Shadow_Rider": "R"
        }
    },
    901: {
        "Game": {
            "-Form_Bloodmoon": "B"
        }
    },
    905: {
        "Game": {
            "-Form_Incarnate": "",
            "-Form_Therian": "T"
        },
        "Drawn": {
            "-Form_Incarnate": ""
        }
    },
    925: {
        "Game": {
            "-Form_Family_of_Three": "T",
            "-Form_Family_of_Four": ""
        },
        "Drawn": {
            "-Form_Family_of_Three": drawn_dream_translation(""),
            "-Form_Family_of_Four": " Dream - Four"
        }
    },
    931: {
        "Game": {
            "-Form_Blue_Plumage": "B",
            "-Form_Green_Plumage": "",
            "-Form_White_Plumage": "W",
            "-Form_Yellow_Plumage": "Y"
        },
        "Drawn": {
            "-Form_Blue_Plumage": drawn_dream_translation("Blue"), 
            "-Form_Green_Plumage": drawn_dream_translation("Green"),
            "-Form_White_Plumage": drawn_dream_translation("White"), 
            "-Form_Yellow_Plumage": drawn_dream_translation("Yellow")
        }
    },
    964: {
        "Game": {
            "-Form_Zero": "",
            "-Form_Hero": "H"
        },
        "Drawn": {
            "-Form_Zero": ""
        }
    },
    978: {
        "Game": {
            "-Form_Curly": "",
            "-Form_Droopy": "D",
            "-Form_Stretchy": "S"
        },
        "Drawn": {
            "-Form_Curly": ""
        }
    },
    982: {
        "Game": {
            "-Form_Two_Segment": "",
            "-Form_Three_Segment": "Th"
        },
        "Drawn": {
            "-Form_Two_Segment": drawn_dream_translation("2"),
            "-Form_Three_Segment": drawn_dream_translation("3")
        }
    },
    999: {
        "Game": {
            "-Form_Chest": "",
            "-Form_Roaming": "R"
        },
        "Drawn": {
            "-Form_Chest": ""
        }
    },
    1012: {
        "Game": {
            "-Form_Artisan": "A",
            "-Form_Counterfeit": "",
            "-Show_Stamp": "DO_BY_HAND"
        }
    },
    1013: {
        "Game": {
            "-Form_Masterpiece": "M",
            "-Form_Unremarkable": "",
            "-Show_Stamp": "DO_BY_HAND"
        }
    },
    1017: {
        "Game": {
            "-Form_Cornerstone_Mask": "C",
            "-Form_Hearthflame_Mask": "H",
            "-Form_Teal_Mask": "",
            "-Form_Wellspring_Mask": "W"
        },
        "Drawn": {
            "-Form_Teal_Mask": ""
        }
    },
    1024: {
        "Game": {
            "-Form_Normal": "",
            "-Form_Terastal": "T",
            "-Form_Stellar": "S"
        },
        "Drawn": {
            "-Form_Normal": ""
        }
    }
}