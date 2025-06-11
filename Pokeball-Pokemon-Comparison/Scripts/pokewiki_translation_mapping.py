from translation_utils import UNIVERSAL_FORMS, EXCLUDE_TRANSLATIONS_MAP, extract_gen_num_from_my_filename

#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     FORM DENOTERS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

# Pokewiki uses the same denoter on all forms
# NOTE: Can go up to arbitrary amount, but will throw error if less used than shared regional forms for a poke (Meowth has Alola, Galar, so this dict must go to at least "b")
POKEWIKI_FORM_DENOTER = {
    "Default": "",
    "1st Variant": "a",
    "2nd Variant": "b",
    "3rd Variant": "c",
    "4th Variant": "d",
    "5th Variant": "e",
    "6th Variant": "f",
    "7th Variant": "g",
    "8th Variant": "h",
    "9th Variant": "i",
    "10th Variant": "j",
    "11th Variant": "k",
    "12th Variant": "l",
    "13th Variant": "m",
    "14th Variant": "n",
    "15th Variant": "o",
    "16th Variant": "p",
    "17th Variant": "q",
    "18th Variant": "r",
    "19th Variant": "s"
}




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     EXCLUSIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

# NOTE: Just because you don't see the sprites on the respective game list DOES NOT MEAN THEY DON'T EXIST -- check URL generated, they may just not be linked properly
    # Helpful as well: https://www.pokewiki.de/Kategorie:Pok%C3%A9monsprite
POKEWIKI_DOESNT_HAVE_IMGS_FOR = {
    "only scraping LGPE and above": lambda my_filename: extract_gen_num_from_my_filename(my_filename) < 7,   # I scraped bulba and wikidex previously, which filled in everything below LGPE. This can be commented out to scrape everything

    "no LGPE animated": lambda my_filename: " LGPE" in my_filename and "-Animated" in my_filename,
    "no LA animated or back sprites": lambda my_filename: " LA" in my_filename and any(sprite_type in my_filename for sprite_type in ("-Animated", "-Back")),
    "no BDSP animated or back sprites": lambda my_filename: " BDSP" in my_filename and any(sprite_type in my_filename for sprite_type in ("-Animated", "-Back")),
    "no gen8 back sprites": lambda my_filename: " Gen8" in my_filename and "-Back" in my_filename,  # Technically it does have SwSh back sprites for new galar forms, gigantamax, and gen8 pokes, but these were already scraped for
    "no gen9 back sprites": lambda my_filename: " Gen9" in my_filename and "-Back" in my_filename,
    "no home animated": lambda my_filename: " HOME" in my_filename and "-Animated" in my_filename
}




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     UNIVERSAL FORMS DATA     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

UNIVERSAL_FORMS_EXCLUDING_REGIONALS = [form for form in UNIVERSAL_FORMS if "-Region" not in form]
UNIVERSAL_FORMS_EXCLUDING_REGIONALS.extend(["-Gigantamax-Form_Single_Strike", "-Gigantamax-Form_Rapid_Strike"])   # Since I check for equality, "-Gigantamax" wont filter these
REGIONAL_FORMS = [form for form in UNIVERSAL_FORMS if "-Region" in form]    # Chronological earliest -> latest




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     GAME TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

# NOTE: If older gen back sprites are ever needed, pokewiki does combine games so a seperate translation mapping dict will be needed
POKEWIKI_GAME_MAP = {
    "Gen1 Red_Blue": "RB",
    "Gen1 Red_Green": "RG",
    "Gen1 Yellow": "Gelb",
    "Gen2 Crystal": "Kristall",
    "Gen2 Gold": "Gold",
    "Gen2 Silver": "Silber",
    "Gen3 Emerald": "Smaragd",
    "Gen3 FRLG": "FRBG",
    "Gen3 Ruby_Sapphire": "RS",
    "Gen4 Diamond_Pearl": "DP",
    "Gen4 HGSS": "HGSS",
    "Gen4 Platinum": "Platin",
    "Gen5 BW_B2W2": "SW",
    "Gen6 XY_ORAS": "XY",
    "Gen7 SM_USUM": "SoMo",
    "Gen7 LGPE": "LGPE",
    "Gen8 SwSh": "SWSH",
    "Gen8 LA": "PLA",
    "Gen8 BDSP": "SDLP",
    "Gen9 SV": "KAPU"
}


POKEWIKI_ALT_GAME_MAP = {
    "BW_B2W2": "S2W2",
    "XY_ORAS": "ORAS",
    "SM_USUM": "USUM"
}




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~[     SPECIES FORM TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

POKEWIKI_TYPE_FORM_MAP = {
    "-Form_Normal": POKEWIKI_FORM_DENOTER["Default"],  # Normal form considered default: so does not have a letter denoter
    "-Form_Fighting": POKEWIKI_FORM_DENOTER["1st Variant"], 
    "-Form_Flying": POKEWIKI_FORM_DENOTER["2nd Variant"], 
    "-Form_Poison": POKEWIKI_FORM_DENOTER["3rd Variant"], 
    "-Form_Ground": POKEWIKI_FORM_DENOTER["4th Variant"], 
    "-Form_Rock": POKEWIKI_FORM_DENOTER["5th Variant"], 
    "-Form_Bug": POKEWIKI_FORM_DENOTER["6th Variant"], 
    "-Form_Ghost": POKEWIKI_FORM_DENOTER["7th Variant"], 
    "-Form_Steel": POKEWIKI_FORM_DENOTER["8th Variant"], 
    "-Form_Fire": POKEWIKI_FORM_DENOTER["9th Variant"], 
    "-Form_Water": POKEWIKI_FORM_DENOTER["10th Variant"], 
    "-Form_Grass": POKEWIKI_FORM_DENOTER["11th Variant"], 
    "-Form_Electric": POKEWIKI_FORM_DENOTER["12th Variant"], 
    "-Form_Psychic": POKEWIKI_FORM_DENOTER["13th Variant"], 
    "-Form_Ice": POKEWIKI_FORM_DENOTER["14th Variant"], 
    "-Form_Dragon": POKEWIKI_FORM_DENOTER["15th Variant"], 
    "-Form_Dark": POKEWIKI_FORM_DENOTER["16th Variant"], 
    "-Form_Fairy": POKEWIKI_FORM_DENOTER["17th Variant"], 
    "-Form_Qmark": POKEWIKI_FORM_DENOTER["18th Variant"]
}


POKEWIKI_POKE_FORM_TRANSLATION_MAP = {
    # Pikachu
    25: {
        "-Form_Cap_Alola": POKEWIKI_FORM_DENOTER["12th Variant"],
        "-Form_Cap_Hoenn": POKEWIKI_FORM_DENOTER["8th Variant"],
        "-Form_Cap_Kalos": POKEWIKI_FORM_DENOTER["11th Variant"],
        "-Form_Cap_Original": POKEWIKI_FORM_DENOTER["7th Variant"],
        "-Form_Cap_Sinnoh": POKEWIKI_FORM_DENOTER["9th Variant"],
        "-Form_Cap_Unova": POKEWIKI_FORM_DENOTER["10th Variant"],
        "-Form_Cap_Partner": POKEWIKI_FORM_DENOTER["13th Variant"],
        # Partner Pikachu in LGPE is 14th
        "-Form_Cap_World": POKEWIKI_FORM_DENOTER["15th Variant"],

        "-Form_Cosplay": POKEWIKI_FORM_DENOTER["6th Variant"],
        "-Form_Cosplay_Belle": POKEWIKI_FORM_DENOTER["2nd Variant"],
        "-Form_Cosplay_Libre": POKEWIKI_FORM_DENOTER["5th Variant"],
        "-Form_Cosplay_PhD": POKEWIKI_FORM_DENOTER["4th Variant"],
        "-Form_Cosplay_Pop_Star": POKEWIKI_FORM_DENOTER["3rd Variant"],
        "-Form_Cosplay_Rock_Star": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Tauros
    128: {
        "-Form_Combat": POKEWIKI_FORM_DENOTER["1st Variant"],
        "-Form_Blaze": POKEWIKI_FORM_DENOTER["2nd Variant"],
        "-Form_Aqua": POKEWIKI_FORM_DENOTER["3rd Variant"]
    },

    # Pichu
    172: {
        "-Form_Spiky_Eared": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    201: {
        "-Form_A": "",
        "-Form_B": "b",
        "-Form_C": "c",
        "-Form_D": "d",
        "-Form_E": "e",
        "-Form_F": "f",
        "-Form_G": "g",
        "-Form_H": "h",
        "-Form_I": "i",
        "-Form_J": "j",
        "-Form_K": "k",
        "-Form_L": "l",
        "-Form_M": "m",
        "-Form_N": "n",
        "-Form_O": "o",
        "-Form_P": "p",
        "-Form_Q": "q",
        "-Form_R": "r",
        "-Form_S": "s",
        "-Form_T": "t",
        "-Form_U": "u",
        "-Form_V": "v",
        "-Form_W": "w",
        "-Form_X": "x",
        "-Form_Y": "y",
        "-Form_Z": "z",
        "-Form_!": "aa",
        "-Form_Qmark": "ab",
    },

    # Sneasel
    215: {
        "-Region_Hisui-f": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Castform
    351: {
        "-Form_Rainy": POKEWIKI_FORM_DENOTER["2nd Variant"],
        "-Form_Snowy": POKEWIKI_FORM_DENOTER["3rd Variant"],
        "-Form_Sunny": 	POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Kyogre & Groudon
    382: { "-Form_Primal": POKEWIKI_FORM_DENOTER["1st Variant"] },
    383: { "-Form_Primal": POKEWIKI_FORM_DENOTER["1st Variant"] },

    # Deoxys
    386: {
        "-Form_Attack": POKEWIKI_FORM_DENOTER["1st Variant"],
        "-Form_Defense": POKEWIKI_FORM_DENOTER["2nd Variant"],
        "-Form_Speed": POKEWIKI_FORM_DENOTER["3rd Variant"]
    },

    # Burmy & Wormadam
    412: {
        "-Form_Plant_Cloak": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Sandy_Cloak": POKEWIKI_FORM_DENOTER["1st Variant"],
        "-Form_Trash_Cloak": POKEWIKI_FORM_DENOTER["2nd Variant"]
    },
    413: {
        "-Form_Plant_Cloak": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Sandy_Cloak": POKEWIKI_FORM_DENOTER["1st Variant"],
        "-Form_Trash_Cloak": POKEWIKI_FORM_DENOTER["2nd Variant"]
    },

    # Cherrim
    421: {
        "-Form_Overcast": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Sunshine": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Shellos & Gastrodon
    422: {
        "-Form_West": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_East": POKEWIKI_FORM_DENOTER["1st Variant"]
    },
    423: {
        "-Form_West": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_East": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Rotom
    479: {
        "-Form_Fan": POKEWIKI_FORM_DENOTER["4th Variant"],
        "-Form_Frost": POKEWIKI_FORM_DENOTER["3rd Variant"],
        "-Form_Heat": POKEWIKI_FORM_DENOTER["1st Variant"],
        "-Form_Mow": POKEWIKI_FORM_DENOTER["5th Variant"],
        "-Form_Wash": POKEWIKI_FORM_DENOTER["2nd Variant"]
    },

    # Dialga & Palkia
    483: { "-Form_Origin": POKEWIKI_FORM_DENOTER["1st Variant"] },
    484: { "-Form_Origin": POKEWIKI_FORM_DENOTER["1st Variant"] },

    # Giratina
    487: {
        "-Form_Altered": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Origin": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Shaymin
    492: {
        "-Form_Land": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Sky": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Arceus
    493: POKEWIKI_TYPE_FORM_MAP,

    #  Basculin
    550: {
        "-Form_Red_Striped": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Blue_Striped": POKEWIKI_FORM_DENOTER["1st Variant"],
        "-Form_White_Striped": POKEWIKI_FORM_DENOTER["2nd Variant"]
    },

    # Darmanitan
    555: {
        "-Form_Standard": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Zen": POKEWIKI_FORM_DENOTER["1st Variant"],
        "-Region_Galar-Form_Standard": POKEWIKI_FORM_DENOTER["2nd Variant"],
        "-Region_Galar-Form_Zen": POKEWIKI_FORM_DENOTER["3rd Variant"]
    },

    # Deerling & Sawsbuck
    585: {
        "-Form_Spring": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Autumn": POKEWIKI_FORM_DENOTER["2nd Variant"],
        "-Form_Summer": POKEWIKI_FORM_DENOTER["1st Variant"],
        "-Form_Winter": POKEWIKI_FORM_DENOTER["3rd Variant"]
    },
    586: {
        "-Form_Spring": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Autumn": POKEWIKI_FORM_DENOTER["2nd Variant"],
        "-Form_Summer": POKEWIKI_FORM_DENOTER["1st Variant"],
        "-Form_Winter": POKEWIKI_FORM_DENOTER["3rd Variant"]
    },

    # Forces of nature
    641: {
        "-Form_Incarnate": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Therian": POKEWIKI_FORM_DENOTER["1st Variant"]
    },
    642: {
        "-Form_Incarnate": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Therian": POKEWIKI_FORM_DENOTER["1st Variant"]
    },
    645: {
        "-Form_Incarnate": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Therian": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Kyurem
    646: {
        "-Form_Black": EXCLUDE_TRANSLATIONS_MAP["DBH"],
        "-Form_Black_Overdrive": EXCLUDE_TRANSLATIONS_MAP["DBH"],
        "-Form_White": EXCLUDE_TRANSLATIONS_MAP["DBH"],
        "-Form_White_Overdrive": EXCLUDE_TRANSLATIONS_MAP["DBH"]
    },

    # Keldeo
    647: {
        "-Form_Ordinary": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Resolute": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Meloetta
    648: {
        "-Form_Aria": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Pirouette": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Genesect
    649: {
        "-Form_Douse_Drive": POKEWIKI_FORM_DENOTER["1st Variant"],
        "-Form_Burn_Drive": POKEWIKI_FORM_DENOTER["3rd Variant"],
        "-Form_Chill_Drive": POKEWIKI_FORM_DENOTER["4th Variant"],
        "-Form_Shock_Drive": POKEWIKI_FORM_DENOTER["2nd Variant"]
    },

    # Greninja
    658: { "-Form_Ash": POKEWIKI_FORM_DENOTER["2nd Variant"] }, # Dunno why its not 1st variant here...

    # Vivillon
    666: {
        "-Form_Meadow": POKEWIKI_FORM_DENOTER["6th Variant"],
        "-Form_Archipelago": POKEWIKI_FORM_DENOTER["9th Variant"],
        "-Form_Continental": POKEWIKI_FORM_DENOTER["3rd Variant"],
        "-Form_Elegant": POKEWIKI_FORM_DENOTER["5th Variant"],
        "-Form_Garden": POKEWIKI_FORM_DENOTER["4th Variant"],
        "-Form_High_Plains": POKEWIKI_FORM_DENOTER["10th Variant"],
        "-Form_Icy_Snow": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Jungle": POKEWIKI_FORM_DENOTER["17th Variant"],
        "-Form_Marine": POKEWIKI_FORM_DENOTER["8th Variant"],
        "-Form_Modern": POKEWIKI_FORM_DENOTER["7th Variant"],
        "-Form_Monsoon": POKEWIKI_FORM_DENOTER["13th Variant"],
        "-Form_Ocean": POKEWIKI_FORM_DENOTER["16th Variant"],
        "-Form_Polar": POKEWIKI_FORM_DENOTER["1st Variant"],
        "-Form_River": POKEWIKI_FORM_DENOTER["12th Variant"],
        "-Form_Sandstorm": POKEWIKI_FORM_DENOTER["11th Variant"],
        "-Form_Savanna": POKEWIKI_FORM_DENOTER["14th Variant"],
        "-Form_Sun": POKEWIKI_FORM_DENOTER["15th Variant"],
        "-Form_Tundra": POKEWIKI_FORM_DENOTER["2nd Variant"],
        "-Form_Poke_Ball": POKEWIKI_FORM_DENOTER["19th Variant"],
        "-Form_Fancy": POKEWIKI_FORM_DENOTER["18th Variant"]
    },

    # Flabebe, Floette, and Florges
    669: {
        "-Form_Red_Flower": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Blue_Flower": POKEWIKI_FORM_DENOTER["3rd Variant"],
        "-Form_Orange_Flower": POKEWIKI_FORM_DENOTER["2nd Variant"],
        "-Form_White_Flower": POKEWIKI_FORM_DENOTER["4th Variant"],
        "-Form_Yellow_Flower": POKEWIKI_FORM_DENOTER["1st Variant"]
    },
    670: {
        "-Form_Red_Flower": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Blue_Flower": POKEWIKI_FORM_DENOTER["3rd Variant"],
        "-Form_Orange_Flower": POKEWIKI_FORM_DENOTER["2nd Variant"],
        "-Form_White_Flower": POKEWIKI_FORM_DENOTER["4th Variant"],
        "-Form_Yellow_Flower": POKEWIKI_FORM_DENOTER["1st Variant"],
        "-Form_Eternal_Flower": POKEWIKI_FORM_DENOTER["5th Variant"]
    },
    671: {
        "-Form_Red_Flower": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Blue_Flower": POKEWIKI_FORM_DENOTER["3rd Variant"],
        "-Form_Orange_Flower": POKEWIKI_FORM_DENOTER["2nd Variant"],
        "-Form_White_Flower": POKEWIKI_FORM_DENOTER["4th Variant"],
        "-Form_Yellow_Flower": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Furfrou
    676: {
        "-Form_Dandy_Trim": POKEWIKI_FORM_DENOTER["6th Variant"],
        "-Form_Debutante_Trim": POKEWIKI_FORM_DENOTER["4th Variant"],
        "-Form_Diamond_Trim": POKEWIKI_FORM_DENOTER["3rd Variant"],
        "-Form_Heart_Trim": POKEWIKI_FORM_DENOTER["1st Variant"],
        "-Form_Kabuki_Trim": POKEWIKI_FORM_DENOTER["8th Variant"],
        "-Form_La_Reine_Trim": POKEWIKI_FORM_DENOTER["7th Variant"],
        "-Form_Matron_Trim": POKEWIKI_FORM_DENOTER["5th Variant"],
        "-Form_Pharaoh_Trim": POKEWIKI_FORM_DENOTER["9th Variant"],
        "-Form_Star_Trim": POKEWIKI_FORM_DENOTER["2nd Variant"]
    },

    # Aegislash
    681: {
        "-Form_Shield": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Blade": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Pumpkaboo and Gourgeist
    710: {
        "-Form_Average_Size": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Small_Size": POKEWIKI_FORM_DENOTER["1st Variant"],
        "-Form_Large_Size": POKEWIKI_FORM_DENOTER["2nd Variant"],
        "-Form_Super_Size": POKEWIKI_FORM_DENOTER["3rd Variant"]
    },
    711: {
        "-Form_Average_Size": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Small_Size": POKEWIKI_FORM_DENOTER["1st Variant"],
        "-Form_Large_Size": POKEWIKI_FORM_DENOTER["2nd Variant"],
        "-Form_Super_Size": POKEWIKI_FORM_DENOTER["3rd Variant"]
    },

    # Xerneas
    716: {
        "-Form_Active": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Neutral": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Zygarde
    718: {
        "-Form_50%": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Complete": POKEWIKI_FORM_DENOTER["4th Variant"], # No idea why this is 4th and not 2nd
        "-Form_10%": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Hoopa
    720: {
        "-Form_Confined": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Unbound": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Oricorio
    741: {
        "-Form_Baile": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Pa'u": POKEWIKI_FORM_DENOTER["2nd Variant"],
        "-Form_Pom_Pom": POKEWIKI_FORM_DENOTER["1st Variant"],
        "-Form_Sensu": POKEWIKI_FORM_DENOTER["3rd Variant"]
    },

    # Lycanroc
    745: {
        "-Form_Midday": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Dusk": POKEWIKI_FORM_DENOTER["2nd Variant"],
        "-Form_Midnight": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Wishiwashi
    746: {
        "-Form_Solo": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_School": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Silvally
    773: POKEWIKI_TYPE_FORM_MAP,

    # Minior
    774: {
        "-Form_Meteor": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Blue_Core": POKEWIKI_FORM_DENOTER["5th Variant"],
        "-Form_Green_Core": POKEWIKI_FORM_DENOTER["4th Variant"],
        "-Form_Indigo_Core": POKEWIKI_FORM_DENOTER["6th Variant"],
        "-Form_Orange_Core": POKEWIKI_FORM_DENOTER["2nd Variant"],
        "-Form_Red_Core": POKEWIKI_FORM_DENOTER["1st Variant"],
        "-Form_Violet_Core": POKEWIKI_FORM_DENOTER["7th Variant"],
        "-Form_Yellow_Core": POKEWIKI_FORM_DENOTER["3rd Variant"],
        "-Form_Core": POKEWIKI_FORM_DENOTER["1st Variant"]  # Shiny form
    },

    # Mimikyu
    778: {
        "-Form_Disguised": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Busted": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Solgaleo
    791: { "-Form_Radiant_Sun": EXCLUDE_TRANSLATIONS_MAP["DNE"] },

    # Lunala
    792: { "-Form_Full_Moon": EXCLUDE_TRANSLATIONS_MAP["DNE"] },

    # Necrozma
    800: {
        "-Form_Dawn_Wings": POKEWIKI_FORM_DENOTER["2nd Variant"],
        "-Form_Dusk_Mane": POKEWIKI_FORM_DENOTER["1st Variant"],
        "-Form_Ultra": POKEWIKI_FORM_DENOTER["3rd Variant"]
    },

    # Magearna
    801: { "-Form_Original_Color": POKEWIKI_FORM_DENOTER["1st Variant"] },

    # Cramorant
    845: {
        "-Form_Gorging": POKEWIKI_FORM_DENOTER["2nd Variant"],
        "-Form_Gulping": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Toxtricity
    849: {
        "-Form_Amped": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Low_Key": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Sinistea & Polteageist
    # Only used by HOME for the show stamp sprites. All other images (since identical) are default form
    # Pokewiki doesn't have show stamp sprites... Bulba does
    854: {
        "-Form_Phony": EXCLUDE_TRANSLATIONS_MAP["DNE"],
        "-Form_Antique": EXCLUDE_TRANSLATIONS_MAP["DNE"]
    },
    855: {
        "-Form_Phony": EXCLUDE_TRANSLATIONS_MAP["DNE"],
        "-Form_Antique": EXCLUDE_TRANSLATIONS_MAP["DNE"]
    },

    # Alcremie
    869: {
        "-Form_Caramel_Swirl_Berry_Sweet": "hb",
        "-Form_Caramel_Swirl_Clover_Sweet": "he",
        "-Form_Caramel_Swirl_Flower_Sweet": "hf",
        "-Form_Caramel_Swirl_Love_Sweet": "hc",
        "-Form_Caramel_Swirl_Ribbon_Sweet": "hg",
        "-Form_Caramel_Swirl_Star_Sweet": "hd",
        "-Form_Caramel_Swirl_Strawberry_Sweet": "ha",
        "-Form_Lemon_Cream_Berry_Sweet": "eb",
        "-Form_Lemon_Cream_Clover_Sweet": "ee",
        "-Form_Lemon_Cream_Flower_Sweet": "ef",
        "-Form_Lemon_Cream_Love_Sweet": "ec",
        "-Form_Lemon_Cream_Ribbon_Sweet": "eg",
        "-Form_Lemon_Cream_Star_Sweet": "ed",
        "-Form_Lemon_Cream_Strawberry_Sweet": "ea",
        "-Form_Matcha_Cream_Berry_Sweet": "cb",
        "-Form_Matcha_Cream_Clover_Sweet": "ce",
        "-Form_Matcha_Cream_Flower_Sweet": "cf",
        "-Form_Matcha_Cream_Love_Sweet": "cc",
        "-Form_Matcha_Cream_Ribbon_Sweet": "cg",
        "-Form_Matcha_Cream_Star_Sweet": "cd",
        "-Form_Matcha_Cream_Strawberry_Sweet": "ca",
        "-Form_Mint_Cream_Berry_Sweet": "db",
        "-Form_Mint_Cream_Clover_Sweet": "de",
        "-Form_Mint_Cream_Flower_Sweet": "df",
        "-Form_Mint_Cream_Love_Sweet": "dc",
        "-Form_Mint_Cream_Ribbon_Sweet": "dg",
        "-Form_Mint_Cream_Star_Sweet": "dd",
        "-Form_Mint_Cream_Strawberry_Sweet": "da",
        "-Form_Rainbow_Swirl_Berry_Sweet": "ib",
        "-Form_Rainbow_Swirl_Clover_Sweet": "ie",
        "-Form_Rainbow_Swirl_Flower_Sweet": "if",
        "-Form_Rainbow_Swirl_Love_Sweet": "ic",
        "-Form_Rainbow_Swirl_Ribbon_Sweet": "ig",
        "-Form_Rainbow_Swirl_Star_Sweet": "id",
        "-Form_Rainbow_Swirl_Strawberry_Sweet": "ia",
        "-Form_Ruby_Cream_Berry_Sweet": "bb",
        "-Form_Ruby_Cream_Clover_Sweet": "be",
        "-Form_Ruby_Cream_Flower_Sweet": "bf",
        "-Form_Ruby_Cream_Love_Sweet": "bc",
        "-Form_Ruby_Cream_Ribbon_Sweet": "bg",
        "-Form_Ruby_Cream_Star_Sweet": "bd",
        "-Form_Ruby_Cream_Strawberry_Sweet": "ba",
        "-Form_Ruby_Swirl_Berry_Sweet": "gb",
        "-Form_Ruby_Swirl_Clover_Sweet": "ge",
        "-Form_Ruby_Swirl_Flower_Sweet": "gf",
        "-Form_Ruby_Swirl_Love_Sweet": "gc",
        "-Form_Ruby_Swirl_Ribbon_Sweet": "gg",
        "-Form_Ruby_Swirl_Star_Sweet": "gd",
        "-Form_Ruby_Swirl_Strawberry_Sweet": "ga",
        "-Form_Salted_Cream_Berry_Sweet": "fb",
        "-Form_Salted_Cream_Clover_Sweet": "fe",
        "-Form_Salted_Cream_Flower_Sweet": "ff",
        "-Form_Salted_Cream_Love_Sweet": "fc",
        "-Form_Salted_Cream_Ribbon_Sweet": "fg",
        "-Form_Salted_Cream_Star_Sweet": "fd",
        "-Form_Salted_Cream_Strawberry_Sweet": "fa",
        "-Form_Vanilla_Cream_Berry_Sweet": "ab",
        "-Form_Vanilla_Cream_Clover_Sweet": "ae",
        "-Form_Vanilla_Cream_Flower_Sweet": "af",
        "-Form_Vanilla_Cream_Love_Sweet": "ac",
        "-Form_Vanilla_Cream_Ribbon_Sweet": "ag",
        "-Form_Vanilla_Cream_Star_Sweet": "ad",
        "-Form_Vanilla_Cream_Strawberry_Sweet": "aa",
        # Pokewiki has these shiny forms for all creams, but they're all the same, so using vanilla cream
        "-Form_Berry_Sweet": "ab",
        "-Form_Clover_Sweet": "ae",
        "-Form_Flower_Sweet": "af",
        "-Form_Love_Sweet": "ac",
        "-Form_Ribbon_Sweet": "ag",
        "-Form_Star_Sweet": "ad",
        "-Form_Strawberry_Sweet": "aa"
    },

    # Eiscue
    875: {
        "-Form_Ice_Face": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Noice_Face": POKEWIKI_FORM_DENOTER["1st Variation"]
    },

    # Morpeko
    877: {
        "-Form_Full_Belly": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Hangry": POKEWIKI_FORM_DENOTER["1st Variation"]
    },

    # Zacian & Zamazenta
    888: {
        "-Form_Hero_of_Many_Battles": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Crowned_Sword": POKEWIKI_FORM_DENOTER["1st Variation"]
    },
    889: {
        "-Form_Hero_of_Many_Battles": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Crowned_Shield": POKEWIKI_FORM_DENOTER["1st Variation"]
    },

    # Eternatus
    890: { "-Form_Eternamax": POKEWIKI_FORM_DENOTER["1st Variation"] },

    # Urshifu
    892: {
        "-Form_Single_Strike": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Rapid_Strike": POKEWIKI_FORM_DENOTER["1st Variation"]
    },

    # Zarude
    893: { "-Form_Dada": POKEWIKI_FORM_DENOTER["1st Variation"] },

    # Calyrex
    898: {
        "-Form_Ice_Rider": POKEWIKI_FORM_DENOTER["1st Variation"],
        "-Form_Shadow_Rider": POKEWIKI_FORM_DENOTER["2nd Variation"]
    },

    # Ursaluna
    901: { "-Form_Bloodmoon": POKEWIKI_FORM_DENOTER["1st Variation"] },

    # Enamorus
    905: {
        "-Form_Incarnate": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Therian": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Maushold
    925: {
        "-Form_Family_of_Three": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Family_of_Four": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Squawkabilly
    931: {
        "-Form_Blue_Plumage": POKEWIKI_FORM_DENOTER["1st Variant"],
        "-Form_Green_Plumage": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_White_Plumage": POKEWIKI_FORM_DENOTER["3rd Variant"],
        "-Form_Yellow_Plumage": POKEWIKI_FORM_DENOTER["2nd Variant"]
    },

    # Palafin
    964: {
        "-Form_Zero": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Hero": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Tatsugiri
    978: {
        "-Form_Curly": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Droopy": POKEWIKI_FORM_DENOTER["1st Variant"],
        "-Form_Stretchy": POKEWIKI_FORM_DENOTER["2nd Variant"]
    },

    # Dudunsparce
    982: {
        "-Form_Two_Segment": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Three_Segment": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Gimmighoul
    999: {
        "-Form_Chest": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Roaming": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Poltchageist & Sinistcha
    # Pokewiki doesn't have show stamp sprites... Bulba does
    1012: {
        "-Form_Artisan": EXCLUDE_TRANSLATIONS_MAP["DNE"],
        "-Form_Counterfeit": EXCLUDE_TRANSLATIONS_MAP["DNE"]
    },
    1013: {
        "-Form_Masterpiece": EXCLUDE_TRANSLATIONS_MAP["DNE"],
        "-Form_Unremarkable": EXCLUDE_TRANSLATIONS_MAP["DNE"]
    },

    # Ogerpon
    1017: {
        "-Form_Cornerstone_Mask": POKEWIKI_FORM_DENOTER["3rd Variant"],
        "-Form_Hearthflame_Mask": POKEWIKI_FORM_DENOTER["2nd Variant"],
        "-Form_Teal_Mask": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Wellspring_Mask": POKEWIKI_FORM_DENOTER["1st Variant"]
    },

    # Terapagos
    1024: {
        "-Form_Normal": POKEWIKI_FORM_DENOTER["Default"],
        "-Form_Terastal": POKEWIKI_FORM_DENOTER["1st Variant"],
        "-Form_Stellar": POKEWIKI_FORM_DENOTER["2nd Variant"]
    }
}