from translation_utils import EXCLUDE_TRANSLATIONS_MAP

#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     DIRECTORY TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

DIRECTORY_TO_FILENAME_MAP = {
    # Game Sprites
    "Gen 6 XY w Battle Animations": "Gen6 XY_ORAS-Animated",
    "Gen 8 LGPE Front Stills - HIGHER QUALITY": "Gen8 LGPE",
    "Gen 8 LGPE Shiny Front Stills - HIGHER QUALITY": "Gen8 LGPE-Shiny",
    "Gen 8 SwSh Animated - SAME QUALITY CHECK MISSING": "Gen8 SwSh-Animated",
    "Gen 8 SwSh Shiny Animated - SAME QUALITY CHECK MISSING": "Gen8 SwSh-Shiny-Animated",
    "Gen 9 Poke Front Stills - HIGHER QUALITY": "Gen9 SV",
    "Gen 9 Poke Front Shiny Stills - HIGHER QUALITY": "Gen9 SV-Shiny",
    "Gen 9 SV Animated - SAME QUALITY CHECK MISSING": "Gen9 SV-Animated",
    "Gen 9 SV ShinyAnimated - SAME QUALITY CHECK MISSING": "Gen9 SV-Shiny-Animated",
    "Gen 9 SV Shiny Animated - SOME HIGHER QUALITY": "Gen9 SV-Shiny-Animated",

    # HOME
    "HOME": "HOME",
    "HOME Shiny": "HOME-Shiny"
}




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~[     UNIVERSAL FORM TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

DL_UNIVERSAL_FORM_MAP = {
    "root": {
        "-f": "(Female)",
        # NOTE: I did have to modify these since root split them as Mega <poke name> X
        "-Mega_X": "Mega X",
        "-Mega_Y": "Mega Y",
        "-Mega": "Mega ",   # This after X&Y so when looping through Mega wont trigger a form meant to be X or Y
        "-Region_Alola": "(Alola)",
        "-Region_Galar": "(Galar)",
        "-Region_Hisui": "(Hisuian)",
        "-Region_Paldea": "Paldea"  # Covers both Tauros and Wooper, which are formatted differently
    }
}




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~[     SPECIES FORM TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

TYPE_FORM_MAP = {
    "root": {
        "-Form_Normal": "Normal",
        "-Form_Fighting": "Fighting", 
        "-Form_Flying": "Flying", 
        "-Form_Poison": "Poison", 
        "-Form_Ground": "Ground", 
        "-Form_Rock": "Rock", 
        "-Form_Bug": "Bug", 
        "-Form_Ghost": "Ghost", 
        "-Form_Steel": "Steel", 
        "-Form_Fire": "Fire", 
        "-Form_Water": "Water", 
        "-Form_Grass": "Grass", 
        "-Form_Electric": "Electric", 
        "-Form_Psychic": "Psychic", 
        "-Form_Ice": "Ice", 
        "-Form_Dragon": "Dragon", 
        "-Form_Dark": "Dark", 
        "-Form_Fairy": "Fairy", 
    }
}


BULBA_POKE_FORM_TRANSLATION_MAP = {
    # Pikachu
    25: {
        "root": {
            "-Form_Cap_Alola": "(Alola Cap)",
            "-Form_Cap_Hoenn": "(Hoenn Cap)",
            "-Form_Cap_Kalos": "(Kalos Cap)",
            "-Form_Cap_Original": "(Original Cap)",
            "-Form_Cap_Sinnoh": "(Sinnoh Cap)",
            "-Form_Cap_Unova": "(Unova Cap)",
            "-Form_Cap_Partner": "(Partner Cap)",
            "-Form_Cap_World": "(World Cap)"
            # No cosplays past gen 6
        },
        "Drawn": {
            "-Form_Cap_Alola": "-Alola Cap",
            "-Form_Cap_Hoenn": "-Hoenn Cap",
            "-Form_Cap_Kalos": "-Kalos Cap",
            "-Form_Cap_Original": "-Original Cap",
            "-Form_Cap_Partner": "-Partner Cap",
            "-Form_Cap_Sinnoh": "-Sinnoh Cap",
            "-Form_Cap_Unova": "-Unova Cap",
            "-Form_Cap_World": "-World Cap",
            "-Form_Cosplay_Belle": "Belle",
            "-Form_Cosplay_Libre": "-Libre",
            "-Form_Cosplay_PhD": "-PhD",
            "-Form_Cosplay_Pop_Star": "-Pop Star",
            "-Form_Cosplay_Rock_Star": "-Rock Star"
        },
        "Menu": {
            "-Form_Cap_Alola": "-Alola",
            "-Form_Cap_Hoenn": "-Hoenn",
            "-Form_Cap_Kalos": "-Kalos",
            "-Form_Cap_Original": "-Original",
            "-Form_Cap_Partner": "-Partner",
            "-Form_Cap_Sinnoh": "-Sinnoh",
            "-Form_Cap_Unova": "-Unova",
            "-Form_Cap_World": "-World"
        }
    },

    # Tauros (Region Paldea added from universal check)
    128: {
        "root": {
            "-Form_Combat": "Fighting",
            "-Form_Blaze": "Fire",
            "-Form_Aqua": "Water"
        },
        "Drawn": {
            "-Form_Combat": " Combat",
            "-Form_Blaze": " Blaze",
            "-Form_Aqua": " Aqua"
        }
    },

    # No Spiky Eared Pichu past gen 4/HOME

    # Unown
    201: {
        "root": {
            "-Form_A": " A",
            "-Form_B": " B",
            "-Form_C": " C",
            "-Form_D": " D",
            "-Form_E": " E",
            "-Form_F": " F",
            "-Form_G": " G",
            "-Form_H": " H",
            "-Form_I": " I",
            "-Form_J": " J",
            "-Form_K": " K",
            "-Form_L": " L",
            "-Form_M": " M",
            "-Form_N": " N",
            "-Form_O": " O",
            "-Form_P": " P",
            "-Form_Qmark": "(Question)",    # QU before Q because Q form would trigger first and misname file
            "-Form_Q": " Q",
            "-Form_R": " R",
            "-Form_S": " S",
            "-Form_T": " T",
            "-Form_U": " U",
            "-Form_V": " V",
            "-Form_W": " W",
            "-Form_X": " X",
            "-Form_Y": " Y",
            "-Form_Z": " Z",
            "-Form_!": "(Exclamation)"
        },
        "Drawn": {
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

    # Sneasel (f added from universal check)
    215: {
        "root": {"-Region_Hisui": "Hisui"}
    },

    # Castform
    351: {
        "root": {
            "-Form_Rainy": "Rainy",
            "-Form_Snowy": "Snowy",
            "-Form_Sunny": "Sunny"
        }
    },

    # Kyogre & Groudon
    382: {
        "root": {"-Form_Primal": "Primal"}
    },
    383: {
        "root": {"-Form_Primal": "Primal"}
    },

    #Deoxys
    386: {
        "root": {
            "-Form_Attack": "Attack",
            "-Form_Defense": "Defense",
            "-Form_Speed": "Speed"
        }
    },

    # Burmy & Wormadam
    412: {
        "root": {
            "-Form_Plant_Cloak": "Plant",
            "-Form_Sandy_Cloak": "Sandy",
            "-Form_Trash_Cloak": "Trash"
        },
        "Drawn": {
            "-Form_Plant_Cloak": "-Plant",
            "-Form_Sandy_Cloak": "-Sandy",
            "-Form_Trash_Cloak": "-Trash"
        }
    },
    413: {
        "root": {
            "-Form_Plant_Cloak": "Plant",
            "-Form_Sandy_Cloak": "Sandy",
            "-Form_Trash_Cloak": "Trash"
        },
        "Drawn": {
            "-Form_Plant_Cloak": "-Plant",
            "-Form_Sandy_Cloak": "-Sandy",
            "-Form_Trash_Cloak": "-Trash"
        }
    },

    #Cherrim
    421: {
        "root": {
            "-Form_Overcast": "Overcast",
            "-Form_Sunshine": "Sunshine"
        },
        "Drawn": {
            "-Form_Overcast": ""
        }
    },
    
    # Shellos & Gastrodon
    422: {
        "root": {
            "-Form_West": "West",
            "-Form_East": "East"
        },
        "Menu": {
            "-Form_East": "-East",
            "-Form_West": ""
        }
    },
    423: {
        "root": {
            "-Form_West": "West",
            "-Form_East": "East"
        },
        "Menu": {
            "-Form_East": "-East",
            "-Form_West": ""
        }
    },
    
    # Rotom
    479: {
        "root": {
            "-Form_Fan": "Fan",
            "-Form_Frost": "Frost",
            "-Form_Heat": "Heat",
            "-Form_Mow": "Mow",
            "-Form_Wash": "Wash"
        }
    },
    
    # Dialga & Palkia
    483: {
        "root": {"-Form_Origin": "Origin"}
    },
    484: {
        "root": {"-Form_Origin": "Origin"}
    },
    
    # Giratina
    487: {
        "root": {
            "-Form_Altered": "Altered",
            "-Form_Origin": "Origin"
        },
        "Drawn": {
            "-Form_Altered": ""
        }
    },
    
    # Shaymin
    492: {
        "root": {
            "-Form_Land": "Land",
            "-Form_Sky": "Sky"
        },
        "Drawn": {
            "-Form_Land": "" 
        }
    },

    # Arceus
    # ??? form excluded from drawn & menu
    493: {
        "root": TYPE_FORM_MAP["root"],
    },

    # Basculin
    550: {
        "root": {
            "-Form_Red_Striped": "Red",
            "-Form_Blue_Striped": "Blue",
            "-Form_White_Striped": "White"
        },
        "Drawn": {
            "-Form_Red_Striped": "-Red",
            "-Form_Blue_Striped": "-Blue",
            "-Form_White_Striped": "-White"
        },
        "Menu": {
            "-Form_Blue_Striped": "-Blue",
            "-Form_Red_Striped": "",
            "-Form_White_Striped": "-White"
        }
    },

    # Darmanitan
    555: {
        "root": {
            "-Form_Zen": "Zen",     # Standard not always marked, so if not Zen its standard
            "-Form_Standard": ""
        },
        "Drawn": {
            "-Form_Standard": "",
            "-Form_Zen": "-Zen",
            "-Region_Galar-Form_Standard": "-Galar",
            "-Region_Galar-Form_Zen": "-Galar Zen"
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
        "root": {
            "-Form_Spring": "Spring",
            "-Form_Autumn": "Autumn",
            "-Form_Summer": "Summer",
            "-Form_Winter": "Winter"
        },
        "Drawn": {
            "-Form_Spring": ""
        }
    },
    586: {
        "root": {
            "-Form_Spring": "Spring",
            "-Form_Autumn": "Autumn",
            "-Form_Summer": "Summer",
            "-Form_Winter": "Winter"
        },
        "Drawn": {
            "-Form_Spring": ""
        }
    },

    # Forces of Nature
    641: {
        "root": {
            "-Form_Incarnate": "Incarnate",
            "-Form_Therian": "Therian"
        },
        "Drawn": {
            "-Form_Incarnate": ""
        }
    },
    642: {
        "root": {
            "-Form_Incarnate": "Incarnate",
            "-Form_Therian": "Therian"
        },
        "Drawn": {
            "-Form_Incarnate": ""
        }
    },
    645: {
        "root": {
            "-Form_Incarnate": "Incarnate",
            "-Form_Therian": "Therian"
        },
        "Drawn": {
            "-Form_Incarnate": ""
        }
    },

    # Kyurem
    # Overdrive forms excluded from menu
    646: {
        "root": {
            # These are all over the place by game/denoters, easier to just do by hand
            "-Form_Black": "Black",
            "-Form_Black_Overdrive": EXCLUDE_TRANSLATIONS_MAP["DBH"],   #TODO
            "-Form_White": "White",
            "-Form_White_Overdrive": EXCLUDE_TRANSLATIONS_MAP["DBH"]    #TODO
        },
        "Drawn": {
            "-Form_Black_Overdrive": "-Black2",
            "-Form_White_Overdrive": "-White2"
        }
    },

    # Keldeo
    647: {
        "root": {
            "-Form_Ordinary": "Ordinary",
            "-Form_Resolute": "Resolute"
        },
        "Drawn": {
            "-Form_Ordinary": ""
        }
    },

    # Meloetta
    648: {
        "root": {
            "-Form_Aria": "Aria",
            "-Form_Pirouette": "Pirouette"
        },
        "Drawn": {
            "-Form_Aria": ""
        }
    },

    # Genesect
    649: {
        "root": {
            "-Form_Douse_Drive": "Douse",
            "-Form_Burn_Drive": "Burn",
            "-Form_Chill_Drive": "Chill",
            "-Form_Shock_Drive": "Shock"
        },
        "Drawn": {
            "-Form_Douse_Drive": " Douse Dream",
            "-Form_Burn_Drive": " Burn Dream",
            "-Form_Chill_Drive": " Chill Dream",
            "-Form_Shock_Drive": " Shock Dream"
        },
        "Menu": {
            "-Form_Douse_Drive": "Douse",
            "-Form_Burn_Drive": "Burn",
            "-Form_Chill_Drive": "Chill",
            "-Form_Shock_Drive": "Shock"
        }
    },

    # Greninja
    658: {
        "root": {
            "-Form_Ash": "Ash"
        }
    },

    # Vivillon
    666: {
        "root": {
            "-Form_Archipelago": "Archipelago",
            "-Form_Continental": "Continental",
            "-Form_Elegant": "Elegant",
            "-Form_Fancy": "Fancy",
            "-Form_Garden": "Garden",
            "-Form_High_Plains": "High Plains",
            "-Form_Icy_Snow": "Icy Snow",
            "-Form_Jungle": "Jungle",
            "-Form_Marine": "Marine",
            "-Form_Meadow": "Meadow",
            "-Form_Modern": "Modern",
            "-Form_Monsoon": "Monsoon",
            "-Form_Ocean": "Ocean",
            "-Form_Poke_Ball": "Pokeball",
            "-Form_Polar": "Polar",
            "-Form_River": "River",
            "-Form_Sandstorm": "Sandstorm",
            "-Form_Savanna": "Savanna",
            "-Form_Sun": "Sun",
            "-Form_Tundra": "Tundra"
        },
        "Drawn": {
            "-Form_Poke_Ball": "-Pok\u00e9 Ball"
        }
    },

    # Flabebe, Floette, and Florges
    669: {
        "root": {
            "-Form_Red_Flower": "Red",
            "-Form_Blue_Flower": "Blue",
            "-Form_Orange_Flower": "Orange",
            "-Form_White_Flower": "White",
            "-Form_Yellow_Flower": "Yellow"
        },
        "Drawn": {
            "-Form_Red_Flower": " Red Flower XY anime",
            "-Form_Blue_Flower": " Blue Flower XY anime",
            "-Form_Orange_Flower": " Orange Flower XY anime",
            "-Form_White_Flower": " White Flower XY anime",
            "-Form_Yellow_Flower": " Yellow Flower XY anime"
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
        "root": {
            "-Form_Red_Flower": "Red",
            "-Form_Blue_Flower": "Blue",
            "-Form_Orange_Flower": "Orange",
            "-Form_White_Flower": "White",
            "-Form_Yellow_Flower": "Yellow",
            "-Form_Eternal_Flower": "Eternal"
        },
        "Drawn": {
            "-Form_Red_Flower": "-Red XY anime",
            "-Form_Blue_Flower": "-Blue XY anime",
            "-Form_Orange_Flower": "-Orange XY anime",
            "-Form_White_Flower": "-White XY anime",
            "-Form_Yellow_Flower": "-Yellow XY anime",
            "-Form_Eternal_Flower": "DO_BY_HAND"     # Doesn't Follow Naming Convention
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
        "root": {
            "-Form_Red_Flower": "Red",
            "-Form_Blue_Flower": "Blue",
            "-Form_Orange_Flower": "Orange",
            "-Form_White_Flower": "White",
            "-Form_Yellow_Flower": "Yellow"
        },
        "Drawn": {
            "-Form_Red_Flower": " Red Flower XY anime",
            "-Form_Blue_Flower": " Blue Flower XY anime",
            "-Form_Orange_Flower": " Orange Flower XY anime",
            "-Form_White_Flower": " White Flower XY anime",
            "-Form_Yellow_Flower": " Yellow Flower XY anime"
        }
    },

    # Furfrou
    676: {
        "root": {
            "-Form_Dandy_Trim": "Dandy",
            "-Form_Debutante_Trim": "Debutanta",
            "-Form_Diamond_Trim": "Diamond",
            "-Form_Heart_Trim": "Heart",
            "-Form_Kabuki_Trim": "Kabuki",
            "-Form_La_Reine_Trim": "La Reine",
            "-Form_Matron_Trim": "Matron",
            "-Form_Pharaoh_Trim": "Pharaoh",
            "-Form_Star_Trim": "Star"
        },
        "Drawn": {
            "-Form_Dandy_Trim": "-Dandy",
            "-Form_Debutante_Trim": "-Debutante",
            "-Form_Diamond_Trim": "-Diamond",
            "-Form_Heart_Trim": "-Heart",
            "-Form_Kabuki_Trim": "-Kabuki",
            "-Form_La_Reine_Trim": "-La Reine",
            "-Form_Matron_Trim": "-Matron",
            "-Form_Pharaoh_Trim": "-Pharaoh",
            "-Form_Star_Trim": "-Star"
        },
        "Menu": {
            "-Form_Dandy_Trim": "-Dandy",
            "-Form_Debutante_Trim": "-Debutante",
            "-Form_Diamond_Trim": "-Diamond",
            "-Form_Heart_Trim": "-Heart",
            "-Form_Kabuki_Trim": "-Kabuki",
            "-Form_La_Reine_Trim": "-La Reine",
            "-Form_Matron_Trim": "-Matron",
            "-Form_Pharaoh_Trim": "-Pharaoh",
            "-Form_Star_Trim": "-Star"
        }
    },

    # Aegislash
    681: {
        "root": {
            "-Form_Shield": "Shield",
            "-Form_Blade": "Blade"
        },
        "Menu": {
            "-Form_Shield": "",
            "-Form_Blade": "-Blade"
        }
    },

    # Pumpkaboo & Gourgeist
    # Drawn & menu only use Average Size
    710: {
        "root": {
            # TODO: Make the 1 average? Convert my webms?
            # Doesn't have these... I do in webm
            "-Form_Average_Size": EXCLUDE_TRANSLATIONS_MAP["DNE"],
            "-Form_Small_Size": EXCLUDE_TRANSLATIONS_MAP["DNE"],
            "-Form_Large_Size": EXCLUDE_TRANSLATIONS_MAP["DNE"],
            "-Form_Super_Size": EXCLUDE_TRANSLATIONS_MAP["DNE"]
        },
        "Drawn": {
            "-Form_Average_Size": ""
        }
    },
    711: {
        "root": {
            # TODO: Make the 1 average? Convert my webms?
            # Doesn't have these... I do in webm
            "-Form_Average_Size": EXCLUDE_TRANSLATIONS_MAP["DNE"],
            "-Form_Small_Size": EXCLUDE_TRANSLATIONS_MAP["DNE"],
            "-Form_Large_Size": EXCLUDE_TRANSLATIONS_MAP["DNE"],
            "-Form_Super_Size": EXCLUDE_TRANSLATIONS_MAP["DNE"]
        },
        "Drawn": {
            "-Form_Average_Size": ""
        }
    },

    # Xerneas
    716: {
        "root": {
            "-Form_Active": "Active",
            "-Form_Neutral": EXCLUDE_TRANSLATIONS_MAP["DNE"]    # TODO: See if it exists in Gen9 SV, if not do I have webm
        },
        "Drawn": {
            "-Form_Active": ""
        }
    },

    # Zygarde
    718: {
        "root": {
            "-Form_50%": "50",
            "-Form_Complete": "Complete",
            "-Form_10%": "10"
        },
        "Drawn": {
            "-Form_50%": "",
            "-Form_Complete": "-Complete",
            "-Form_10%": "-10Percent"
        },
        "Menu":{
            "-Form_10%": "-10 Percent"
        }
    },

    # Hoopa
    720: {
        "root": {
            "-Form_Confined": "Confined",
            "-Form_Unbound": "Unbound"
        },
        "Drawn": {
            "-Form_Confined": ""
        }
    },

    # Oricorio
    741: {
        "root": {
            "-Form_Baile": "Baile",
            "-Form_Pa'u": "Pa_u",
            "-Form_Pom_Pom": "Pom-Pom",
            "-Form_Sensu": "Sensu"
        },
        "Drawn": {
            "-Form_Baile": "",
            "-Form_Pom_Pom": "-Pom-Pom"
        }
    },

    # Lycanroc
    745: {
        "root": {
            "-Form_Midday": "Midday",
            "-Form_Dusk": "Dusk",
            "-Form_Midnight": "Midnight"
        },
        "Drawn": {
            "-Form_Midday": ""
        }
    },

    # Wishiwashi
    746: {
        "root": {
            "-Form_Solo": "Solo",
            "-Form_School": "School"
        },
        "Drawn": {
            "-Form_Solo": ""
        }
    },

    # Silvally
    773: {
        "root": TYPE_FORM_MAP["root"],
    },

    # Minior
    774: {
        "root": {
            "-Form_Meteor": "Meteor",
            "-Form_Blue_Core": "Blue",
            "-Form_Green_Core": "Green",
            "-Form_Indigo_Core": "Indigo",
            "-Form_Orange_Core": "Orange",
            "-Form_Red_Core": "Red",
            "-Form_Violet_Core": "Violet",
            "-Form_Yellow_Core": "Yellow",
            "-Form_Core": ""   # This is the shiny sprite TODO
        },
        "Drawn": {
            "-Form_Meteor": "",
            "-Form_Blue_Core": "-Blue",
            "-Form_Green_Core": "-Green",
            "-Form_Indigo_Core": "-Indigo",
            "-Form_Orange_Core": "-Orange",
            "-Form_Red_Core": "-Red",
            "-Form_Violet_Core": "-Violet",
            "-Form_Yellow_Core": "-Yellow",
        },
        "Menu": {
            "-Form_Meteor": "",
            "-Form_Blue_Core": "-Blue",
            "-Form_Green_Core": "-Green",
            "-Form_Indigo_Core": "-Indigo",
            "-Form_Orange_Core": "-Orange",
            "-Form_Red_Core": "-Red",
            "-Form_Violet_Core": "-Violet",
            "-Form_Yellow_Core": "-Yellow",
        },
    },

    # Mimikyu
    778: {
        "root": {
            "-Form_Disguised": "Disguised",
            "-Form_Busted": "Busted"
        },
        "Drawn": {
            "-Form_Disguised": "",
            "-Form_Busted": ""
        },
        "Menu": {
            "-Form_Busted": EXCLUDE_TRANSLATIONS_MAP["DNE"]
        }
    },

    # Solgaleo
    # TODO: Dont exist in HOME, Gen9 tho?
    791: {
        "root": {
            "-Form_Radiant_Sun": EXCLUDE_TRANSLATIONS_MAP["DNE"]
        },
        "Drawn": {
            "-Form_Radiant_Sun": "-RadiantSunPhase"
        },
        "Menu": {
            "-Form_Radiant_Sun": EXCLUDE_TRANSLATIONS_MAP["DNE"]
        }
    },

    # Lunala
    #  TODO: Dont exist in HOME, Gen9 tho?
    792: {
        "root": {
            "-Form_Full_Moon": EXCLUDE_TRANSLATIONS_MAP["DNE"]
        },
        "Drawn": {
            "-Form_Full_Moon": "-FullMoonPhase"
        },
        "Menu": {
            "-Form_Full_Moon": EXCLUDE_TRANSLATIONS_MAP["DNE"]
        }
    },

    # Necrozma
    800: {
        "root": {
            "-Form_Dawn_Wings": "Dawn Wings",
            "-Form_Dusk_Mane": "Dusk Mane",
            "-Form_Ultra": "Ultra"
        }
    },

    # Magearna
    801: {
        "root": {
            "-Form_Original_Color": "Original Color"
        },
        "Drawn": {
            "-Form_Original_Color": EXCLUDE_TRANSLATIONS_MAP["DNE"]
        },
        "Menu": {
            "-Form_Original_Color": "-Original Color"
        }
    },

    # Cramorant
    845: {
        "root": {
            "-Form_Gorging": "Gorging",
            "-Form_Gulping": "Gulping"
        }
    },

    # Toxtricity
    849: {
        "root": {
            "-Form_Amped": "Amped",
            "-Form_Low_Key": "Low Key"
        },
        "Menu": {
            "-Form_Amped": ""
        }
    },

    # Sinistea & Polteageist not applicable since their forms only matter to show stamps, which are static only

    # Alcremie
    869: {
        "root": {
            "-Form_Caramel_Swirl_Berry_Sweet": "(Caramel Swirl) (Berry Sweet)",
            "-Form_Caramel_Swirl_Clover_Sweet": "(Caramel Swirl) (Clover Sweet)",
            "-Form_Caramel_Swirl_Flower_Sweet": "(Caramel Swirl) (Flower Sweet)",
            "-Form_Caramel_Swirl_Love_Sweet": "(Caramel Swirl) (Love Sweet)",
            "-Form_Caramel_Swirl_Ribbon_Sweet": "(Caramel Swirl) (Ribbon Sweet)",
            "-Form_Caramel_Swirl_Star_Sweet": "(Caramel Swirl) (Star Sweet)",
            "-Form_Caramel_Swirl_Strawberry_Sweet": "(Caramel Swirl) (Strawberry Sweet)",
            "-Form_Lemon_Cream_Berry_Sweet": "(Lemon Cream) (Berry Sweet)",
            "-Form_Lemon_Cream_Clover_Sweet": "(Lemon Cream) (Clover Sweet)",
            "-Form_Lemon_Cream_Flower_Sweet": "(Lemon Cream) (Flower Sweet)",
            "-Form_Lemon_Cream_Love_Sweet": "(Lemon Cream) (Love Sweet)",
            "-Form_Lemon_Cream_Ribbon_Sweet": "(Lemon Cream) (Ribbon Sweet)",
            "-Form_Lemon_Cream_Star_Sweet": "(Lemon Cream) (Star Sweet)",
            "-Form_Lemon_Cream_Strawberry_Sweet": "(Lemon Cream) (Strawberry Sweet)",
            "-Form_Matcha_Cream_Berry_Sweet": "(Matcha Cream) (Berry Sweet)",
            "-Form_Matcha_Cream_Clover_Sweet": "(Matcha Cream) (Clover Sweet)",
            "-Form_Matcha_Cream_Flower_Sweet": "(Matcha Cream) (Flower Sweet)",
            "-Form_Matcha_Cream_Love_Sweet": "(Matcha Cream) (Love Sweet)",
            "-Form_Matcha_Cream_Ribbon_Sweet": "(Matcha Cream) (Ribbon Sweet)",
            "-Form_Matcha_Cream_Star_Sweet": "(Matcha Cream) (Star Sweet)",
            "-Form_Matcha_Cream_Strawberry_Sweet": "(Matcha Cream) (Strawberry Sweet)",
            "-Form_Mint_Cream_Berry_Sweet": "(Mint Cream) (Berry Sweet)",
            "-Form_Mint_Cream_Clover_Sweet": "(Mint Cream) (Clover Sweet)",
            "-Form_Mint_Cream_Flower_Sweet": "(Mint Cream) (Flower Sweet)",
            "-Form_Mint_Cream_Love_Sweet": "(Mint Cream) (Love Sweet)",
            "-Form_Mint_Cream_Ribbon_Sweet": "(Mint Cream) (Ribbon Sweet)",
            "-Form_Mint_Cream_Star_Sweet": "(Mint Cream) (Star Sweet)",
            "-Form_Mint_Cream_Strawberry_Sweet": "(Mint Cream) (Strawberry Sweet)",
            "-Form_Rainbow_Swirl_Berry_Sweet": "(Rainbow Swirl) (Berry Sweet)",
            "-Form_Rainbow_Swirl_Clover_Sweet": "(Rainbow Swirl) (Clover Sweet)",
            "-Form_Rainbow_Swirl_Flower_Sweet": "(Rainbow Swirl) (Flower Sweet)",
            "-Form_Rainbow_Swirl_Love_Sweet": "(Rainbow Swirl) (Love Sweet)",
            "-Form_Rainbow_Swirl_Ribbon_Sweet": "(Rainbow Swirl) (Ribbon Sweet)",
            "-Form_Rainbow_Swirl_Star_Sweet": "(Rainbow Swirl) (Star Sweet)",
            "-Form_Rainbow_Swirl_Strawberry_Sweet": "(Rainbow Swirl) (Strawberry Sweet)",
            "-Form_Ruby_Cream_Berry_Sweet": "(Ruby Cream) (Berry Sweet)",
            "-Form_Ruby_Cream_Clover_Sweet": "(Ruby Cream) (Clover Sweet)",
            "-Form_Ruby_Cream_Flower_Sweet": "(Ruby Cream) (Flower Sweet)",
            "-Form_Ruby_Cream_Love_Sweet": "(Ruby Cream) (Love Sweet)",
            "-Form_Ruby_Cream_Ribbon_Sweet": "(Ruby Cream) (Ribbon Sweet)",
            "-Form_Ruby_Cream_Star_Sweet": "(Ruby Cream) (Star Sweet)",
            "-Form_Ruby_Cream_Strawberry_Sweet": "(Ruby Cream) (Strawberry Sweet)",
            "-Form_Ruby_Swirl_Berry_Sweet": "(Ruby Swirl) (Berry Sweet)",
            "-Form_Ruby_Swirl_Clover_Sweet": "(Ruby Swirl) (Clover Sweet)",
            "-Form_Ruby_Swirl_Flower_Sweet": "(Ruby Swirl) (Flower Sweet)",
            "-Form_Ruby_Swirl_Love_Sweet": "(Ruby Swirl) (Love Sweet)",
            "-Form_Ruby_Swirl_Ribbon_Sweet": "(Ruby Swirl) (Ribbon Sweet)",
            "-Form_Ruby_Swirl_Star_Sweet": "(Ruby Swirl) (Star Sweet)",
            "-Form_Ruby_Swirl_Strawberry_Sweet": "(Ruby Swirl) (Strawberry Sweet)",
            "-Form_Salted_Cream_Berry_Sweet": "(Salted Cream) (Berry Sweet)",
            "-Form_Salted_Cream_Clover_Sweet": "(Salted Cream) (Clover Sweet)",
            "-Form_Salted_Cream_Flower_Sweet": "(Salted Cream) (Flower Sweet)",
            "-Form_Salted_Cream_Love_Sweet": "(Salted Cream) (Love Sweet)",
            "-Form_Salted_Cream_Ribbon_Sweet": "(Salted Cream) (Ribbon Sweet)",
            "-Form_Salted_Cream_Star_Sweet": "(Salted Cream) (Star Sweet)",
            "-Form_Salted_Cream_Strawberry_Sweet": "(Salted Cream) (Strawberry Sweet)",
            "-Form_Vanilla_Cream_Berry_Sweet": "(Vanilla Cream) (Berry Sweet)",
            "-Form_Vanilla_Cream_Clover_Sweet": "(Vanilla Cream) (Clover Sweet)",
            "-Form_Vanilla_Cream_Flower_Sweet": "(Vanilla Cream) (Flower Sweet)",
            "-Form_Vanilla_Cream_Love_Sweet": "(Vanilla Cream) (Love Sweet)",
            "-Form_Vanilla_Cream_Ribbon_Sweet": "(Vanilla Cream) (Ribbon Sweet)",
            "-Form_Vanilla_Cream_Star_Sweet": "(Vanilla Cream) (Star Sweet)",
            "-Form_Vanilla_Cream_Strawberry_Sweet": "(Vanilla Cream) (Strawberry Sweet)",
            # Shinies (which have only berry differences)
            "-Form_Berry_Sweet": "(Vanilla Cream) (Berry Sweet)",
            "-Form_Clover_Sweet": "(Vanilla Cream) (Clover Sweet)",
            "-Form_Flower_Sweet": "(Vanilla Cream) (Flower Sweet)",
            "-Form_Love_Sweet": "(Vanilla Cream) (Love Sweet)",
            "-Form_Ribbon_Sweet": "(Vanilla Cream) (Ribbon Sweet)",
            "-Form_Star_Sweet": "(Vanilla Cream) (Star Sweet)",
            "-Form_Strawberry_Sweet": "(Vanilla Cream) (Strawberry Sweet)"
        },
        "Drawn": {
            # Kinda random selection, I guess?
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
        },
        "Menu": {
            # Basically all different creams, with strawberry sweet
            "-Form_Caramel_Swirl_Strawberry_Sweet": "-Caramel",
            "-Form_Lemon_Cream_Strawberry_Sweet": "-Lemon",
            "-Form_Matcha_Cream_Strawberry_Sweet": "-Matcha",
            "-Form_Mint_Cream_Strawberry_Sweet": "-Mint",
            "-Form_Rainbow_Swirl_Strawberry_Sweet": "-Rainbow",
            "-Form_Ruby_Swirl_Strawberry_Sweet": "-Ruby Swirl",
            "-Form_Ruby_Cream_Strawberry_Sweet": "-Ruby",
            "-Form_Salted_Cream_Strawberry_Sweet": "-Salted",
            "-Form_Vanilla_Cream_Strawberry_Sweet": ""
        }
    },

    # Eiscue
    875: {
        "root": {
            "-Form_Ice_Face": "Ice",
            "-Form_Noice_Face": "Noice"
        },
        "Drawn": {
            "-Form_Ice_Face": "",
            "-Form_Noice_Face": "-Noice"
        }
    },

    # Morpeko
    877: {
        "root": {
            "-Form_Full_Belly": "Full Belly",
            "-Form_Hangry": "Hangry"
        },
        "Drawn": {
            "-Form_Full_Belly": "-Full"
        },
        "Menu": {
            "-Form_Full_Belly": ""
        }
    },

    # Zacian & Zamazenta
    888: {
        "root": {
            "-Form_Hero_of_Many_Battles": "Hero of Many Battles",
            "-Form_Crowned_Sword": "Crowned"
        },
        "Drawn": {
            "-Form_Hero_of_Many_Battles": "-Hero",
            "-Form_Crowned_Sword": ""
        },
        "Menu": {
            "-Form_Hero_of_Many_Battles": "",
            "-Form_Crowned_Sword": "-Crowned"
        }
    },
    889: {
        "root": {
            "-Form_Hero_of_Many_Battles": "Hero of Many Battles",
            "-Form_Crowned_Shield": "Crowned"
        },
        "Drawn": {
            "-Form_Hero_of_Many_Battles": "-Hero",
            "-Form_Crowned_Shield": ""
        },
        "Menu": {
            "-Form_Hero_of_Many_Battles": "",
            "-Form_Crowned_Sword": "-Crowned"
        }
    },

    # Eternatus
    890: {
        "root": {
            "-Form_Eternamax": EXCLUDE_TRANSLATIONS_MAP["DNE"]
        },
        "Drawn": {
            "-Form_Eternamax": EXCLUDE_TRANSLATIONS_MAP["DNE"]
        }
    },
    
    # Urshifu
    892: {
        "root": {
            "-Form_Single_Strike": "Single Strike",
            "-Form_Rapid_Strike": "Rapid Strike"
        },
        "Drawn": {
            "-Form_Single_Strike": " Single Strike",
            "-Form_Rapid_Strike": " Rapid Strike"
        },
        "Menu": {
            # Doesn't have either form???
            "-Form_Single_Strike": EXCLUDE_TRANSLATIONS_MAP["DNE"],
            "-Form_Rapid_Strike": EXCLUDE_TRANSLATIONS_MAP["DNE"]
        }
    },

    # Zarude
    893: {
        "root": {
            "-Form_Dada": "Dada"
        }
    },

    # Calyrex
    898: {
        "root": {
            "-Form_Ice_Rider": "Ice",
            "-Form_Shadow_Rider": "Shadow"
        }
    },

    # Ursaluna
    901: {
        "root": {
            "-Form_Bloodmoon": "Blood Moon"
        }
    },

    # Enamorus
    905: {
        "root": {
            "-Form_Incarnate": "Incarnate",
            "-Form_Therian": "Therian"
        },
        "Drawn": {
            "-Form_Incarnate": ""
        }
    },

    # Maushold
    925: {
        "root": {
            "-Form_Family_of_Three": "Three",
            "-Form_Family_of_Four": "Four"
        },
        "Drawn": {
            "-Form_Family_of_Three": "",
            "-Form_Family_of_Four": " Dream - Four"
        },
        "Menu": {
            "-Form_Family_of_Three": "-Three",
            "-Form_Family_of_Four": ""
        }
    },

    # Squawkabilly
    931: {
        "root": {
            "-Form_Blue_Plumage": "Blue",
            "-Form_Green_Plumage": "Green",
            "-Form_White_Plumage": "White",
            "-Form_Yellow_Plumage": "Yellow"
        },
        "Drawn": {
            "-Form_Blue_Plumage": "-Blue", 
            "-Form_Green_Plumage": "",
            "-Form_White_Plumage": "-White", 
            "-Form_Yellow_Plumage": "-Yellow"
        },
        "Menu": {
            "-Form_Blue_Plumage": "-Blue", 
            "-Form_Green_Plumage": "",
            "-Form_White_Plumage": "-White", 
            "-Form_Yellow_Plumage": "-Yellow"
        }
    },

    # Palafin
    964: {
        "root": {
            "-Form_Zero": "Zero",
            "-Form_Hero": "Hero"
        },
        "Drawn": {
            "-Form_Zero": ""
        }
    },
    
    # Tatsugiri
    978: {
        "root": {
            "-Form_Curly": "Curly",
            "-Form_Droopy": "Droopy",
            "-Form_Stretchy": "Stretchy"
        },
        "Drawn": {
            "-Form_Curly": ""
        }
    },

    # Dudunsparce
    982: {
        "root": {
            "-Form_Two_Segment": "Two",
            "-Form_Three_Segment": "Three"
        },
        "Drawn": {
            "-Form_Two_Segment": "",
            "-Form_Three_Segment": ""
        },
        "Game": {
            "-Form_Two_Segment": "",
            "-Form_Three_Segment": EXCLUDE_TRANSLATIONS_MAP["DNE"]
        },
    },

    # Gimmighoul
    999: {
        "root": {
            # Chest form not denoted
            "-Form_Roaming": "Roaming"
        },
        "Drawn": {
            "-Form_Chest": ""
        }
    },

    # Poltchageist & Sinistcha not applicable since only forms used for stamps, which aren't animated

    # Ogerpon
    1017: {
        "root": {
            "-Form_Cornerstone_Mask": "Cobblestone",
            "-Form_Hearthflame_Mask": "Hearthflame",
            "-Form_Teal_Mask": "Teal",
            "-Form_Wellspring_Mask": "Wellspring"
        },
        "Drawn": {
            "-Form_Teal_Mask": ""
        }
    },

    # Terapagos
    1024: {
        "root": {
            "-Form_Normal": "Normal",
            "-Form_Terastal": "Terastal",
            "-Form_Stellar": "Stellar"  # TODO: Check Gen9, not in HOME
        },
        "Drawn": {
            "-Form_Normal": ""
        }
    }
}